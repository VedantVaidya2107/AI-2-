import { defineConfig } from 'vite'

export default defineConfig({
  base: process.env.VITE_BASE_PATH || '/',
  root: '.',
  server: {
    port: 5173,
    host: true,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      }
    }
  },
  build: {
    outDir: 'dist',
  }
})
