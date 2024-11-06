// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import TeacherPage from '../views/TeacherPage.vue'
import StudentPage from '../views/StudentPage.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/teachers',
    name: 'Teachers',
    component: TeacherPage
  },
  {
    path: '/students',
    name: 'Students',
    component: StudentPage
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router