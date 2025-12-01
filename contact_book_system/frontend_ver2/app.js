import axios from "axios";

const API_BASE_URL = "https://contact-book-system-bowp.onrender.com";
const WS_BASE_URL = "wss://contact-book-system-bowp.onrender.com";

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
    // ✅ 状態を保存するヘルパーメソッド
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

          // 30分以内の状態のみ復元（タイムアウト対策）
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

    // ログイン処理
    handleLogin(userData) {
      this.currentUser = userData;
      this.isLoggedIn = true;

      if (this.currentUser.role === "admin") {
        this.currentPage = "account-management-menu";
      } else {
        this.currentPage = "main-menu";
      }

      sessionStorage.setItem("currentUser", JSON.stringify(userData));
      sessionStorage.setItem("isLoggedIn", "true");

      // ✅ 状態を保存
      this.saveAppState();

      this.updateTitle({ title: "", icon: "", showBackButton: false });
    },

    // ログアウト処理
    handleLogout() {
      this.currentUser = null;
      this.isLoggedIn = false;
      this.currentPage = "login-form";

      // セッション情報をクリア
      sessionStorage.removeItem("currentUser");
      sessionStorage.removeItem("isLoggedIn");
      sessionStorage.removeItem("access_token");
      sessionStorage.removeItem("appState"); // ✅ 追加

      // axiosのトークンをクリア
      delete axios.defaults.headers.common["Authorization"];

      this.updateTitle({ title: "", icon: "", showBackButton: false });
    },

    // 画面遷移
    setCurrentPage(page) {
      this.currentPage = page;

      // ✅ 画面遷移時に状態を保存
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

      // ✅ 状態を保存
      this.saveAppState();
      this.updateTitle({ title: "", icon: "", showBackButton: false });
    },

    // 検索結果表示
    handleSearchResults({ results, resultType, resultMessage }) {
      this.results = results;
      this.resultType = resultType;
      this.resultMessage = resultMessage;
      this.currentPage = "account-search-results";

      // ✅ 状態を保存
      this.saveAppState();
    },

    // アカウント選択
    handleSelectAccount(account) {
      this.selectedAccounts = [account];
      this.currentPage = "account-update-table";

      // ✅ 状態を保存
      this.saveAppState();
    },

    handleAccountNavigation(page) {
      this.currentPage = page;

      // ✅ 状態を保存
      this.saveAppState();
    },

    // タイトル更新
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

      // ✅ 状態を保存
      this.saveAppState();
    },
  },

  // ✅ マウント時に状態を復元
  mounted() {
    console.log("🚀 アプリケーション起動");

    // トークンを復元
    const storedToken = sessionStorage.getItem("access_token");
    if (storedToken) {
      axios.defaults.headers.common["Authorization"] = `Bearer ${storedToken}`;
      console.log("✅ トークンを復元");
    }

    // ユーザー情報を復元
    const storedUser = sessionStorage.getItem("currentUser");
    const loggedIn = sessionStorage.getItem("isLoggedIn");

    if (storedUser && loggedIn === "true") {
      this.currentUser = JSON.parse(storedUser);
      this.isLoggedIn = true;
      console.log("✅ ユーザー情報を復元:", this.currentUser.fullName);

      // ✅ 保存された状態を復元
      const restored = this.restoreAppState();

      if (!restored) {
        // 状態が復元できなかった場合は、役割に応じた初期画面へ
        if (this.currentUser.role === "admin") {
          this.currentPage = "account-management-menu";
        } else {
          this.currentPage = "main-menu";
        }
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
            <!-- ログイン後は常に上部に表示 -->
            <user-header
                v-if="isLoggedIn && currentUser"
                :current-user="currentUser"
                :page-title="pageTitle"
                :page-icon="pageIcon"
                :show-back-button="showBackButton"
                @logout="handleLogout"
                @back="goBackToMenu">
            </user-header>

            <!-- ログイン画面 -->
            <login-form 
                v-if="currentPage === 'login-form'" 
                @login="handleLogin">
            </login-form>

            <!-- メインメニュー -->
            <main-menu 
                v-else-if="isLoggedIn && currentPage === 'main-menu'"
                :current-user="currentUser"
                @navigate="setCurrentPage">
            </main-menu>

            <!-- 生徒用 -->
            <entry-form
                v-else-if="currentPage === 'entry-form'"
                :current-user="currentUser"
                @back="goBackToMenu"
                @update-title="updateTitle">
            </entry-form>

            <past-renrakucho-search
                v-else-if="currentPage === 'past-renrakucho-search'"
                :current-user="currentUser"
                @back="goBackToMenu"
                @update-title="updateTitle">
            </past-renrakucho-search>

            <!-- 教師用 -->
            <submission-status
                v-else-if="currentPage === 'submission-status'"
                :current-user="currentUser"
                @back="goBackToMenu"
                @update-title="updateTitle">
            </submission-status>

            <class-entry-renrakucho
                v-else-if="currentPage === 'class-entry-renrakucho'"
                :current-user="currentUser"
                @back="goBackToMenu"
                @update-title="updateTitle">
            </class-entry-renrakucho>

            <class-past-renrakucho
                v-else-if="currentPage === 'class-past-renrakucho'"
                :current-user="currentUser"
                @back="goBackToMenu"
                @update-title="updateTitle">
            </class-past-renrakucho>

            <!-- 養護教諭用 -->
            <school-nurse-dashboard
                v-else-if="isLoggedIn && currentPage === 'school-nurse-dashboard'"
                :current-user="currentUser"
                @back="goBackToMenu"
                @update-title="updateTitle">
            </school-nurse-dashboard>

            <!-- 管理者用 -->
            <account-management-menu
                v-else-if="currentPage === 'account-management-menu'"
                @navigate-account="setCurrentPage"
                @back-to-menu="goBackToMenu"
                @update-title="updateTitle">
            </account-management-menu>

            <account-form
                v-else-if="currentPage === 'account-form'"
                :current-user="currentUser"
                @back-to-menu="setCurrentPage('account-management-menu')"
                @update-title="updateTitle">
            </account-form>

            <account-search
                v-else-if="currentPage === 'account-search'"
                :current-user="currentUser"
                @back-to-menu="setCurrentPage('account-management-menu')"
                @show-results="handleSearchResults"
                @update-title="updateTitle">
            </account-search>

            <account-search-results
                v-else-if="currentPage === 'account-search-results'"
                :results="results"
                :result-type="resultType"
                :result-message="resultMessage"
                @select-account="handleSelectAccount"
                @back-to-search="setCurrentPage('account-search')"
                @back-to-menu="setCurrentPage('account-management-menu')"
                @update-title="updateTitle">
            </account-search-results>

            <account-update-table
                v-else-if="currentPage === 'account-update-table'"
                :accounts="selectedAccounts"
                @back-to-search="setCurrentPage('account-search')"
                @back-to-results="setCurrentPage('account-search-results')"
                @update-title="updateTitle">
            </account-update-table>

            <archive-management
                v-else-if="currentPage === 'archive-management'"
                @back-to-menu="setCurrentPage('account-management-menu')"
                @update-title="updateTitle">
            </archive-management>

            <!-- チャット機能 -->
            <chat-room-list 
                v-else-if="currentPage === 'chat-room-list'"
                @navigate="navigateToChat"
                @update-title="updateTitle">
            </chat-room-list>

            <chat-room 
                v-else-if="currentPage === 'chat-room'"
                :room-id="chatRoomId"
                @back="goBackToMenu"
                @update-title="updateTitle">
            </chat-room>

        </div>
    `,
}).mount("#app");
