import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
import path from "path"; // 追加

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "src"), // @ を src にマッピング
    },
  },
  server: {
    host: "0.0.0.0",
    port: 5173,
    watch: {
      usePolling: true  // Dockerコンテナ内でのファイル変更検知に必要
    }
  }
});
