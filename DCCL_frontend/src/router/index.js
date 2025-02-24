import { createRouter, createWebHistory } from 'vue-router'


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path:'/',
      name:'mainView',
      component:()=>import('../views/mainView.vue')
    },
   
  ],
})

export default router
