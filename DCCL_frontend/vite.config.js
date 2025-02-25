import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'
import requireTransform from 'vite-plugin-require-transform'; 
// https://vite.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    vueDevTools(),
    //对于需要使用require的模块，需要使用vite-plugin-require-transform插件进行转换
    requireTransform({  
      fileRegex:/.ts$|.tsx$|.vue$/  
    //   fileRegex:/.js$|.jsx$|.vue$/  
    }), 
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    },
  },
  server: {
    proxy: {
      '/flask': {
        target: 'http://127.0.0.1:5000',
        changeOrigin: true,
        
        rewrite: (path) => path.replace(/^\/flask/, '')
      }
    }
  }
})
