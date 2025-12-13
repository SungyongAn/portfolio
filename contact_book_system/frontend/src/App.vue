<template>
  <div>
    <UserHeader
      v-if="isLoggedIn && currentUser"
      :current-user="currentUser"
      :page-title="pageTitle"
      :page-icon="pageIcon"
      :show-back-button="showBackButton"
      @logout="handleLogout"
    />

    <!-- 画面を切り替える -->
    <router-view
      :current-user="currentUser"
      @update-title="updateTitle"
      @login="handleLogin"
    />
  </div>
</template>

<script>
import axios from "axios";
import UserHeader from "./components/UserHeader.vue";

export default {
  name: "App",

  components: {
    UserHeader,
  },

  data() {
    return {
      currentUser: null,
      isLoggedIn: false,
      pageTitle: "",
      pageIcon: "",
      showBackButton: false,
    };
  },

  methods: {
    navigateToChat(roomId) {
      this.$router.push(`/chat/${roomId}`);
    },

    handleLogin(userData) {
      console.log("✅ ログイン処理:", userData.role);
      this.currentUser = userData;
      this.isLoggedIn = true;

      sessionStorage.setItem("currentUser", JSON.stringify(userData));
      sessionStorage.setItem("isLoggedIn", "true");

      if (userData.role === "admin") {
        this.$router.push("/account-management");
      } else {
        this.$router.push("/menu");
      }
    },

    handleLogout() {
      console.log("🚪 ログアウト処理");
      this.currentUser = null;
      this.isLoggedIn = false;

      sessionStorage.clear();
      delete axios.defaults.headers.common["Authorization"];

      this.$router.push("/");
    },

    updateTitle({ title, icon, showBackButton }) {
      console.log("📝 タイトル更新:", { title, icon, showBackButton });
      this.pageTitle = title || "";
      this.pageIcon = icon || "";
      this.showBackButton = showBackButton ?? false;
    },
  },

  created() {
    console.log("🎬 App.vue created");
    const storedUser = sessionStorage.getItem("currentUser");
    const loggedIn = sessionStorage.getItem("isLoggedIn");
    const token = sessionStorage.getItem("access_token");

    console.log("📦 sessionStorage確認:", {
      hasUser: !!storedUser,
      loggedIn,
      hasToken: !!token,
    });

    if (storedUser && loggedIn === "true") {
      this.currentUser = JSON.parse(storedUser);
      this.isLoggedIn = true;

      if (token) {
        axios.defaults.headers.common["Authorization"] = `Bearer ${token}`;
      }
      console.log("✅ ユーザー情報復元完了");
    }
  },

  watch: {
    $route(to, from) {
      console.log("🔄 ルート変更:", from?.path, "→", to.path);
      console.log("🔐 認証状態:", this.isLoggedIn);

      // ログインが必要なページで未ログインの場合のみリダイレクト
      const publicPages = ["/"];
      const authRequired = !publicPages.includes(to.path);

      if (authRequired && !this.isLoggedIn) {
        console.log("❌ 未認証アクセス - ログイン画面へリダイレクト");
        this.$router.push("/");
      }
    },
  },
};
</script>
