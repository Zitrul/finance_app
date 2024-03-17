import { createRouter, createWebHistory } from 'vue-router'
import Main from '@/views/Main.vue'
import Wallet from '@/views/Wallet.vue'
import News from '@/views/News.vue'

const routes = [
  {
    path: '/',
    name: 'Добро пожаловать',
    component: Main
  },
  {
    path: '/wallet',
    name: 'Управление финансами',
    component: Wallet
  },
  {
    path: '/news',
    name: 'Последние новости',
    component: News
  },
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
