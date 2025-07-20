import { createRouter, createWebHistory } from 'vue-router'
import AdminPage from '@/components/AdminPage.vue'
import UserPage from '@/components/UserPage.vue'
import LoginForm from '@/components/LoginForm.vue'
import store from '@/store'

const routes = [
  { path: '/', component: LoginForm },
  { path: '/login', component: LoginForm },
  { path: '/admin', component: AdminPage },
  { path: '/user', component: UserPage },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to, from, next) => {
  const user = store.state.user

  if (to.meta.requiresAuth) {
    if (!user || !user.id) {
      return next('/login')
    }

    if (to.meta.role && to.meta.role !== user.role) {
      return next('/login')
    }
  }

  next()
})

export default router
