import { createApp } from "vue";
import App from "./App.vue";

import router from "./router/index.js";

import axios from "axios";
import "bootstrap/dist/css/bootstrap.min.css";
import "@fortawesome/fontawesome-free/css/all.min.css";

window.axios = axios;

const app = createApp(App);
app.config.globalProperties.$axios = axios;

app.use(router); // ★ここでVueにルーターを組み込む

app.mount("#app");
