import { createApp } from "vue";
import { createPinia } from "pinia";
import App from "./App.vue";
import router from "./router";
import { useAuthStore } from "@/stores/auth";

// Element Plus
import ElementPlus from "element-plus";
import "element-plus/dist/index.css";
import * as ElementPlusIconsVue from "@element-plus/icons-vue";
import ja from "element-plus/es/locale/lang/ja";

import "@/assets/styles/variables.css";
import "@/assets/styles/typography.css";
import "@/assets/styles/layout.css";
import "@/assets/styles/utilities.css";

const app = createApp(App);
const pinia = createPinia();

app.use(pinia);

// ここを修正
const authStore = useAuthStore(pinia);

await authStore.initAuth();

// Element Plusアイコンを全登録
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component);
}

app.use(router);
app.use(ElementPlus, { locale: ja });

app.mount("#app");
