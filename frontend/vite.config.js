import { fileURLToPath, URL } from "node:url";

import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";

serverEndpoint = "127.0.0.1:8000";

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      "@": fileURLToPath(new URL("./src", import.meta.url)),
    },
  },

  server: {
    proxy: {
      "/api": {
        target: `http://${serverEndpoint}`,
        secure: false,
        cors: true, // Enable CORS support
      },
      "/static": {
        target: `http://${serverEndpoint}`,
        changeOrigin: true,
        secure: false,
      },
      "/django-ws": {
        target: `ws://${serverEndpoint}`,
        rewrite: (path) => path.replace(/^\/django-ws/, "/ws"),
        changeOrigin: true,
        secure: false,
      },
    },
  },

  build: {
    target: "esnext",
  },
});
