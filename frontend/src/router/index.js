import { createRouter, createWebHistory } from 'vue-router'
import { useAuth } from '../stores/auth'
import LoginView from '../views/LoginView.vue'
import DashboardView from '../views/DashboardView.vue'

const routes = [
  { path: '/login', name: 'login', component: LoginView },
  { path: '/', name: 'dashboard', component: DashboardView, meta: { requiresAuth: true } }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach(async (to) => {
  const auth = useAuth()
  if (!auth.initialized) {
    await auth.loadSession()
  }

  if (to.meta.requiresAuth && !auth.isAuthenticated.value) {
    return { name: 'login', query: { redirect: to.fullPath } }
  }

  if (to.name === 'login' && auth.isAuthenticated.value) {
    return { name: 'dashboard' }
  }

  return true
})

export default router
