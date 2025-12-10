// src/main.js
import { createApp } from "vue";
import App from "./App.vue";
import axios from "axios";
import "bootstrap/dist/css/bootstrap.min.css";
import "@fortawesome/fontawesome-free/css/all.min.css";

// axiosをグローバルに設定（既存のコードとの互換性のため）
window.axios = axios;

// または、Vueのグローバルプロパティとして設定
const app = createApp(App);
app.config.globalProperties.$axios = axios;

app.mount("#app");
