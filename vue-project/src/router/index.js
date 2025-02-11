import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import SignUp from '../views/SignUp.vue'    // Add direct import
import SignIn from '../views/SignIn.vue'    // Add direct import

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/signup',
      name: 'signup',
      component: SignUp,    // Use direct import instead of lazy loading for now
    },
    {
      path: '/signin',
      name: 'signin',
      component: SignIn,    // Use direct import instead of lazy loading for now
    },
    {
      path: '/dashboard',
      name: 'dashboard',
      component: () => import('../views/StudentDashboard.vue')
    },
    {
      path: '/feedback',
      name: 'feedback',
      component: () => import('../views/FeedbackForm.vue')
    }

  ],
})

// Add navigation guard for debugging
router.beforeEach((to, from, next) => {
  console.log('Navigating to:', to.path)
  next()
})

export default router
