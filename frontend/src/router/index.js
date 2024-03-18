import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    redirect: '/home',
  },
  {
    path: '/editprofile',
    name: 'editprofile',
    component: () => import('../views/Editprofile.vue')
  },
  {
    path: '/home',
    name: 'feed',
    component: () => import('../views/Feed.vue')
  },
  {
    path: '/login',
    name: 'login',
    component: () => import('../views/Login.vue')
  },
  {
    path: '/signup',
    name: 'signup',
    component: () => import('../views/Signup.vue')
  },
  {
    path: '/users/:name',
    name: 'users',
    component: () => import('../views/Users.vue')
  },
  {
    path: '/myaccount',
    name: 'myaccount',
    component: () => import('../views/MyAccount.vue')
  },

  {
    path: '/upload',
    name: 'upload',
    component: () => import('../views/Upload.vue')
  },

]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
