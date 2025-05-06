// vite.config.js
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  base: './',
  plugins: [react()],
  server: {
    port: 3000,
    open: true
  },
  build: {
    outDir: 'dist',
    sourcemap: true
  },
  preview: {
    port: 3000,
    host: true,
    allowedHosts: ['niza-classifier.onrender.com', 'llm-niza-classifier.onrender.com', 'llm-niza-classifier-backend.onrender.com']
  }
});
