import { createRouter, createWebHistory } from 'vue-router'
import Main from '@/views/Main.vue'
import Wallet from '@/views/Wallet.vue'

const routes = [
  {
    path: '/',
    name: 'Добро пожаловать',
    component: Main
  },
  {
    path: '/wallet',
    name: 'Финансы',
    component: Wallet
  },
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
