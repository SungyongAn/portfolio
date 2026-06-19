import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
import { fileURLToPath, URL } from "node:url";

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      "@": fileURLToPath(new URL("./src", import.meta.url)),
    },
  },
  build: {
    target: "esnext",
  },
  server: {
    host: "0.0.0.0",
    port: 5173,
    watch: {
      usePolling: true,
    },
    proxy: {
      "/api/notifications/ws": {
        target: "http://backend:8000",
        changeOrigin: true,
        ws: true,
      },
      "/api": {
        target: "http://backend:8000",
        changeOrigin: true,
      },
    },
  },
});