// app.js（グローバル axios 対応版）

const API_BASE_URL = "https://contact-book-system-bowp.onrender.com";
const WS_BASE_URL = "wss://contact-book-system-bowp.onrender.com";

// axios 設定
axios.defaults.baseURL = API_BASE_URL;
axios.defaults.headers.common["Content-Type"] = "application/json";

window.WS_BASE_URL = WS_BASE_URL;

Vue.createApp({
  data() {
    return {
      currentPage: "login-form",
      currentUser: null,
      isLoggedIn: false,
      results: [],
      resultType: "success",
      resultMessage: "",
      selectedAccounts: [],
      pageTitle: "",
      pageIcon: "",
      showBackButton: false,
      chatRoomId: null,
    };
  },

  components: {
    "login-form": LoginForm,
    "user-header": UserHeader,
    "main-menu": MainMenu,
    "entry-form": EntryForm,
    "past-renrakucho-search": PastRenrakuchoSearch,
    "class-entry-renrakucho": ClassEntryRenrakucho,
    "class-past-renrakucho": ClassPastRenrakucho,
    "submission-status": SubmissionStatus,
    "account-management-menu": AccountManagementMenu,
    "account-form": AccountForm,
    "account-search": AccountSearch,
    "account-search-results": AccountSearchResults,
    "account-update-table": AccountUpdateTable,
    "school-nurse-dashboard": SchoolNurseDashboard,
    "chat-room-list": ChatRoomList,
    "chat-room": ChatRoom,
    "archive-management": ArchiveManagement,
  },

  methods: {
    saveAppState() {
      const state = {
        currentPage: this.currentPage,
        results: this.results,
        resultType: this.resultType,
        resultMessage: this.resultMessage,
        selectedAccounts: this.selectedAccounts,
        chatRoomId: this.chatRoomId,
        timestamp: Date.now(),
      };
      sessionStorage.setItem("appState", JSON.stringify(state));
    },

    restoreAppState() {
      const savedState = sessionStorage.getItem("appState");
      if (savedState) {
        try {
          const state = JSON.parse(savedState);
          const thirtyMinutes = 30 * 60 * 1000;
          if (Date.now() - state.timestamp < thirtyMinutes) {
            this.currentPage = state.currentPage || "login-form";
            this.results = state.results || [];
            this.resultType = state.resultType || "success";
            this.resultMessage = state.resultMessage || "";
            this.selectedAccounts = state.selectedAccounts || [];
            this.chatRoomId = state.chatRoomId || null;

            console.log("✅ 状態を復元しました:", this.currentPage);
            return true;
          } else {
            console.log("⚠️ セッションタイムアウト（30分経過）");
            sessionStorage.removeItem("appState");
          }
        } catch (error) {
          console.error("❌ 状態の復元に失敗:", error);
          sessionStorage.removeItem("appState");
        }
      }
      return false;
    },

    handleLogin(userData) {
      this.currentUser = userData;
      this.isLoggedIn = true;

      this.currentPage =
        this.currentUser.role === "admin"
          ? "account-management-menu"
          : "main-menu";

      sessionStorage.setItem("currentUser", JSON.stringify(userData));
      sessionStorage.setItem("isLoggedIn", "true");

      this.saveAppState();
      this.updateTitle({ title: "", icon: "", showBackButton: false });
    },

    handleLogout() {
      this.currentUser = null;
      this.isLoggedIn = false;
      this.currentPage = "login-form";

      sessionStorage.removeItem("currentUser");
      sessionStorage.removeItem("isLoggedIn");
      sessionStorage.removeItem("access_token");
      sessionStorage.removeItem("appState");

      delete axios.defaults.headers.common["Authorization"];

      this.updateTitle({ title: "", icon: "", showBackButton: false });
    },

    setCurrentPage(page) {
      this.currentPage = page;
      this.saveAppState();
      if (page === "main-menu" || page === "account-management-menu") {
        this.updateTitle({ title: "", icon: "", showBackButton: false });
      }
    },

    goBackToMenu() {
      if (
        this.currentUser &&
        this.currentUser.role === "admin" &&
        this.currentPage.startsWith("account")
      ) {
        this.currentPage = "account-management-menu";
      } else if (this.currentPage === "chat-room") {
        this.currentPage = "chat-room-list";
        this.chatRoomId = null;
      } else if (this.currentPage === "archive-management") {
        this.currentPage = "account-management-menu";
      } else {
        this.currentPage = "main-menu";
      }

      this.saveAppState();
      this.updateTitle({ title: "", icon: "", showBackButton: false });
    },

    handleSearchResults({ results, resultType, resultMessage }) {
      this.results = results;
      this.resultType = resultType;
      this.resultMessage = resultMessage;
      this.currentPage = "account-search-results";
      this.saveAppState();
    },

    handleSelectAccount(account) {
      this.selectedAccounts = [account];
      this.currentPage = "account-update-table";
      this.saveAppState();
    },

    handleAccountNavigation(page) {
      this.currentPage = page;
      this.saveAppState();
    },

    updateTitle(config) {
      if (typeof config === "string") {
        this.pageTitle = config;
        this.pageIcon = arguments[1] || "";
        this.showBackButton = false;
      } else {
        this.pageTitle = config.title || "";
        this.pageIcon = config.icon || "";
        this.showBackButton = config.showBackButton || false;
      }
    },

    navigateToChat(page, roomId = null) {
      this.currentPage = page;
      this.chatRoomId = roomId;
      this.saveAppState();
    },
  },

  mounted() {
    console.log("🚀 アプリケーション起動");

    const storedToken = sessionStorage.getItem("access_token");
    if (storedToken) {
      axios.defaults.headers.common["Authorization"] = `Bearer ${storedToken}`;
      console.log("✅ トークンを復元");
    }

    const storedUser = sessionStorage.getItem("currentUser");
    const loggedIn = sessionStorage.getItem("isLoggedIn");

    if (storedUser && loggedIn === "true") {
      this.currentUser = JSON.parse(storedUser);
      this.isLoggedIn = true;
      console.log("✅ ユーザー情報を復元:", this.currentUser.fullName);

      const restored = this.restoreAppState();

      if (!restored) {
        this.currentPage =
          this.currentUser.role === "admin"
            ? "account-management-menu"
            : "main-menu";
        console.log("⚠️ デフォルト画面に遷移:", this.currentPage);
      }

      this.updateTitle({ title: "", icon: "", showBackButton: false });
    } else {
      console.log("⚠️ 未ログイン状態");
      this.currentPage = "login-form";
    }
  },

  template: `
    <div>
      <user-header
        v-if="isLoggedIn && currentUser"
        :current-user="currentUser"
        :page-title="pageTitle"
        :page-icon="pageIcon"
        :show-back-button="showBackButton"
        @logout="handleLogout"
        @back="goBackToMenu"
      ></user-header>

      <login-form
        v-if="currentPage === 'login-form'"
        @login="handleLogin"
      ></login-form>

      <main-menu
        v-else-if="isLoggedIn && currentPage === 'main-menu'"
        :current-user="currentUser"
        @navigate="setCurrentPage"
      ></main-menu>

      <!-- 以降、既存のコンポーネント構成はそのまま -->
    </div>
  `,
}).mount("#app");
