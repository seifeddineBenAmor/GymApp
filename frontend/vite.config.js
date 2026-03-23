import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  server: {
    host: true,        // needed for Docker
    port: 5173,
    proxy: {
      "/api": {
        target: "http://api:8000",   // docker-compose service name
        changeOrigin: true,
      },
    },
  },
});
