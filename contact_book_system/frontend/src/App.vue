<template>
  <div>
    <UserHeader
      v-if="isLoggedIn && currentUser"
      :current-user="currentUser"
      :page-title="pageTitle"
      :page-icon="pageIcon"
      :show-back-button="showBackButton"
      @logout="handleLogout"
      @back="goBack"
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

  watch: {
    $route(to, from) {
      // ログイン画面に戻った場合、ログアウト状態にする
      if (to.path === "/") {
        this.currentUser = null;
        this.isLoggedIn = false;
        sessionStorage.clear();
        delete axios.defaults.headers.common["Authorization"];
      }
    },
  },

  methods: {
    navigateToChat(roomId) {
      this.$router.push(`/chat/${roomId}`);
    },

    goBack() {
      this.$router.back();
    },

    handleLogin(userData) {
      console.log("ログインユーザー:", userData);
      console.log("role:", userData.role);
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
      this.currentUser = null;
      this.isLoggedIn = false;

      sessionStorage.clear();
      delete axios.defaults.headers.common["Authorization"];

      this.$router.push("/");
    },

    updateTitle({ title, icon, showBackButton }) {
      this.pageTitle = title || "";
      this.pageIcon = icon || "";
      this.showBackButton = showBackButton ?? false;
    },
  },

  mounted() {
    const storedUser = sessionStorage.getItem("currentUser");
    const loggedIn = sessionStorage.getItem("isLoggedIn");
    const token = sessionStorage.getItem("access_token");

    if (storedUser && loggedIn === "true") {
      this.currentUser = JSON.parse(storedUser);
      this.isLoggedIn = true;

      // トークンをaxiosヘッダーに復元
      if (token) {
        axios.defaults.headers.common["Authorization"] = `Bearer ${token}`;
      }

      // ログイン画面にいる場合は適切な画面にリダイレクト
      if (this.$route.path === "/") {
        if (this.currentUser.role === "admin") {
          this.$router.push("/account-management");
        } else {
          this.$router.push("/menu");
        }
      }
    } else {
      this.currentUser = null;
      this.isLoggedIn = false;

      // ログインしていない場合はログイン画面へ
      if (this.$route.path !== "/") {
        this.$router.push("/");
      }
    }
  },
};
</script>
