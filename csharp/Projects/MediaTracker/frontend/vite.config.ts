import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

/*
 * Vite is the build tool and development server.
 * It's faster than Create React App (CRA) because it uses native ES modules
 * in development (no bundling needed) and esbuild for production builds.
 *
 * Tradeoff: Vite requires modern browser support (ES modules) in development.
 * For production, it bundles with Rollup for compatibility.
 *
 * In development, Vite proxies /api requests to the backend at localhost:5000.
 * This avoids CORS issues during development.
 * In production (Docker), Nginx handles the proxy (see nginx.conf).
 */
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/api': {
        target: 'http://localhost:5000',
        changeOrigin: true,
      },
    },
  },
})
