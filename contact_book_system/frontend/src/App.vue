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

    <ChatRoomList @navigate="navigateToChat" />

    <!-- ここでルーターの画面を切り替える -->
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

  components: { UserHeader },

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
    // ルーター履歴で戻る
    goBack() {
      this.$router.back();
    },

    // ログイン処理
    handleLogin(userData) {
      this.currentUser = userData;
      this.isLoggedIn = true;

      sessionStorage.setItem("currentUser", JSON.stringify(userData));
      sessionStorage.setItem("isLoggedIn", "true");

      // ログイン後の遷移
      if (userData.role === "admin") {
        this.$router.push("/account-management");
      } else {
        this.$router.push("/menu");
      }
    },

    // ログアウト
    handleLogout() {
      this.currentUser = null;
      this.isLoggedIn = false;

      sessionStorage.clear();
      delete axios.defaults.headers.common["Authorization"];

      this.$router.push("/");
    },

    // 画面タイトル更新（各コンポーネントから呼べる）
    updateTitle({ title, icon, showBackButton }) {
      this.pageTitle = title || "";
      this.pageIcon = icon || "";
      this.showBackButton = showBackButton ?? false;
    },
  },

  mounted() {
    const storedUser = sessionStorage.getItem("currentUser");
    const loggedIn = sessionStorage.getItem("isLoggedIn");

    if (storedUser && loggedIn === "true") {
      this.currentUser = JSON.parse(storedUser);
      this.isLoggedIn = true;
    } else {
      this.currentUser = null;
      this.isLoggedIn = false;
    }
  },
};
</script>
