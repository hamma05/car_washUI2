import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  base: '/static/',
  build: {
    outDir: `${import.meta.dirname}/static`,
    emptyOutDir: false,
    manifest: 'manifest.json',
    rollupOptions: {
      input: {
        index: `${import.meta.dirname}/assets/js/main.jsx`,
      },
      output: {
        entryFileNames: 'js/[name]-bundle.js',
        assetFileNames: 'assets/[name][extname]',
      },
    },
  },
});