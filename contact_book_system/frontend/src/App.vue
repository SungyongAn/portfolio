<template>
  <div>
    <UserHeader
      v-if="isLoggedIn && currentUser"
      :current-user="currentUser"
      :page-title="pageTitle"
      :page-icon="pageIcon"
      :show-back-button="showBackButton"
      @logout="handleLogout"
      @back="goBackToMenu"
    />

    <component
      :is="CurrentComponent"
      :current-user="currentUser"
      :results="results"
      :result-type="resultType"
      :result-message="resultMessage"
      :accounts="selectedAccounts"
      :room-id="chatRoomId"
      @navigate-account="currentPage = $event"
      @navigate="setCurrentPage"
      @navigate-yearly="currentPage = $event"
      @back="goBackToMenu"
      @back-to-menu="goBackToMenu"
      @back-to-search="setCurrentPage('account-search')"
      @back-to-results="setCurrentPage('account-search-results')"
      @update-title="updateTitle"
      @show-results="handleSearchResults"
      @select-account="handleSelectAccount"
      @login="handleLogin"
    />
  </div>
</template>

<script>
import axios from "axios";
import UserHeader from "./components/UserHeader.vue";
import LoginForm from "./components/LoginForm.vue";
import MainMenu from "./components/MainMenu.vue";

// AccountManagement
import AccountManagementMenu from "./components/AccountManagement/AccountManagementMenu.vue";
import AccountForm from "./components/AccountManagement/AccountForm.vue";
import AccountSearch from "./components/AccountManagement/AccountSearch.vue";
import AccountSearchResults from "./components/AccountManagement/AccountSearchResults.vue";
import AccountUpdateTable from "./components/AccountManagement/AccountUpdateTable.vue";
import YearlyProcessingMenu from "./components/AccountManagement/YearlyProcessingMenu.vue";

// Renrakucho
import EntryForm from "./components/Renrakucho/EntryForm.vue";
import PastRenrakuchoSearch from "./components/Renrakucho/PastRenrakuchoSearch.vue";
import SubmissionStatus from "./components/Renrakucho/SubmissionStatus.vue";
import ClassEntryRenrakucho from "./components/Renrakucho/ClassEntryRenrakucho.vue";
import ClassPastRenrakucho from "./components/Renrakucho/ClassPastRenrakucho.vue";
import SchoolNurseDashboard from "./components/Renrakucho/SchoolNurseDashboard.vue";

// Chat
import ChatRoomList from "./components/ChatRoomList.vue";
import ChatRoom from "./components/ChatRoom.vue";

// Archive
import ArchiveManagement from "./components/ArchiveManagement.vue";

export default {
  name: "App",
  components: {
    UserHeader,
    LoginForm,
    MainMenu,
    AccountManagementMenu,
    AccountForm,
    AccountSearch,
    AccountSearchResults,
    AccountUpdateTable,
    YearlyProcessingMenu,
    EntryForm,
    PastRenrakuchoSearch,
    SubmissionStatus,
    ClassEntryRenrakucho,
    ClassPastRenrakucho,
    SchoolNurseDashboard,
    ChatRoomList,
    ChatRoom,
    ArchiveManagement,
  },
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
  computed: {
    CurrentComponent() {
      const map = {
        "login-form": LoginForm,
        "main-menu": MainMenu,
        "account-management-menu": AccountManagementMenu,
        "account-form": AccountForm,
        "account-search": AccountSearch,
        "account-search-results": AccountSearchResults,
        "account-update-table": AccountUpdateTable,
        "yearly-processing-menu": YearlyProcessingMenu,
        "entry-form": EntryForm,
        "past-renrakucho-search": PastRenrakuchoSearch,
        "submission-status": SubmissionStatus,
        "class-entry-renrakucho": ClassEntryRenrakucho,
        "class-past-renrakucho": ClassPastRenrakucho,
        "school-nurse-dashboard": SchoolNurseDashboard,
        "chat-room-list": ChatRoomList,
        "chat-room": ChatRoom,
        "archive-management": ArchiveManagement,
      };
      return map[this.currentPage] || LoginForm;
    },
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
      sessionStorage.removeItem("appState");

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
      } else if (this.currentPage === "yearly-processing-menu") {
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
      console.log(
        "✅ ユーザー情報を復元:",
        this.currentUser.lastName,
        this.currentUser.firstName
      );

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
};
</script>
