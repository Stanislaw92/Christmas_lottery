import { createRouter, createWebHistory } from '@ionic/vue-router';
import HomeView from '../views/HomeView.vue'
import LotteryDetail from '../views/LotteryDetail.vue'
import LotteryResult from '../views/LotteryResult.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/:uuid',
    name: 'lotteryDetails',
    component: LotteryDetail,
    props: true
  },
  {
    path: '/lotteryResult/:uuid',
    name: 'lotteryResult',
    component: LotteryResult,
    props: true
  },
]

const router = createRouter({
  history: createWebHistory('/'),
  routes
})

export default router
