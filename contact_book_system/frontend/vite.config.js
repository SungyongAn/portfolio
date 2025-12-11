import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";

export default defineConfig({
  plugins: [vue()],
  server: {
    host: "0.0.0.0",
    port: 5173,
    watch: {
      usePolling: true, // Dockerでのファイル監視用
    },
  },
  optimizeDeps: {
    force: true, // 依存関係の最適化を強制
  },
});
