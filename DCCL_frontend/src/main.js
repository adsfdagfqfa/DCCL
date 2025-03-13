import 'tailwindcss/tailwind.css';
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import { createPinia } from 'pinia'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import VueVirtualScroller from 'vue-virtual-scroller'
import 'vue-virtual-scroller/dist/vue-virtual-scroller.css'
const app = createApp(App)

app.use(VueVirtualScroller)

app.use(router)
app.use(ElementPlus)
const pinia = createPinia()
app.use(pinia)

app.mount('#app')
