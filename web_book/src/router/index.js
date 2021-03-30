import Vue from 'vue'
import VueRouter from 'vue-router'
import Search from '../views/Search.vue'
import Info from '../views/Info.vue'
import Chapter from '../views/Chapter.vue'
import Home from '../views/Home.vue'

Vue.use(VueRouter);

  const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home,
    meta: {
        title: '我的书架'   // 标题设置
    }
  },
  {
    path: '/search',
    name: 'Search',
    component: Search,
    meta: {
        title: '搜索书籍'   // 标题设置
    }
  },
  {
    path: '/info/:id',
    name: 'Info',
    component: Info,
  },
  {
    path: '/chapter/:id',
    name: 'Chapter',
    component: Chapter
  }
  // {
  //   path: '/about',
  //   name: 'About',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    // component: () => import(/* webpackChunkName: "about" */ '../views/About.vue')
  // }
]

const router = new VueRouter({
  mode: 'hash',
  base: process.env.BASE_URL,
  routes
})

export default router
