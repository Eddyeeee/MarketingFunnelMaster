import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import path from "path";
import { fileURLToPath } from 'url';
import runtimeErrorOverlay from "@replit/vite-plugin-runtime-error-modal";

// Moderner Weg für ESM
const __filename = fileURLToPath(import.meta.url);
const rootDir = path.dirname(__filename);

export default defineConfig({
  plugins: [
    react(),
    runtimeErrorOverlay(),
    // Der Rest Ihrer Plugins bleibt unverändert
    ...(process.env.NODE_ENV !== "production" &&
    process.env.REPL_ID !== undefined
      ? [
          await import("@replit/vite-plugin-cartographer").then((m) =>
            m.cartographer(),
          ),
        ]
      : []),
  ],
  // Die `root`-Direktive sagt Vite, dass die Webseite im 'client'-Ordner liegt
  root: path.resolve(rootDir, "client"),
  
  resolve: {
    alias: {
      // Der Alias '@' zeigt jetzt eindeutig auf den Ordner 'client/src'
      "@": path.resolve(rootDir, "client/src"),
      "@shared": path.resolve(rootDir, "shared"),
      "@assets": path.resolve(rootDir, "attached_assets"),
    },
  },

  build: {
    // Das Build-Verzeichnis wird korrekt außerhalb des client-Ordners erstellt
    outDir: path.resolve(rootDir, "dist/public"),
    emptyOutDir: true,
  },

  server: {
    fs: {
      strict: true,
      deny: ["**/.*"],
    },
  },
});