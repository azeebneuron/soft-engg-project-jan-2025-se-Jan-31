import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import SignUp from '../views/SignUp.vue' // Add direct import
import SignIn from '../views/SignIn.vue' // Add direct import
import DeadlineSection from '../views/DeadlineSection.vue'

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
      component: SignUp, // Use direct import instead of lazy loading for now
    },
    {
      path: '/signin',
      name: 'signin',
      component: SignIn, // Use direct import instead of lazy loading for now
    },
    {
      path: '/deadline',
      name: 'deadline',
      component: DeadlineSection, // Use direct import instead of lazy loading for now
    },
    {
      path: '/dashboard',
      name: 'dashboard',
      component: () => import('../views/StudentDashboard.vue'),
    },
    {
      path: '/feedback',
      name: 'feedback',
      component: () => import('../views/FeedbackForm.vue'),
    },
    {
      path: '/instfeedback',
      name: 'instfeedback',
      component: () => import('../views/InstructorFeedback.vue'),
    },
    {
      path: '/chatbot',
      name: 'chatbot',
      component: () => import('../views/ChatInterface.vue'),
    },
    {
      path: '/admindash',
      name: 'admindash',
      component: () => import('../views/AdminDashboard.vue'),
    },
    {
      path: '/instructor',
      name: 'instructor',
      component: () => import('../views/InstructorDashboard.vue'),
    },
    {
      path: '/courseman',
      name: 'courseman',
      component: () => import('../views/CourseMan.vue'),
    },
    {
      path: '/studentresources',
      name: 'studentresources',
      component: () => import('../views/StudentResource.vue'),
    },
    {
      path: '/aisummary',
      name: 'aisummary',
      component: () => import('../views/AISummary.vue'),
    },
    {
      path: '/instructor/insights',
      name: 'instructor-insights',
      component: () => import('../views/InstructorInsightsDashboard.vue'),
    },
    {
      path: '/student/insights',
      name: 'student-insights',
      component: () => import('../views/StudentInsightsDashboard.vue'),
    },
    {
      path: '/student/videochatbot',
      name: 'student-videochatbot',
      component: () => import('../views/VideoChatbot.vue')
    }
  ],
})

// Add navigation guard for debugging
router.beforeEach((to, from, next) => {
  console.log('Navigating to:', to.path)
  next()
})

export default router
