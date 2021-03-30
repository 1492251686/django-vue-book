import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import icons from './icons'
//引入css
import 'tailwindcss/tailwind.css'
import './assets/css/font.css'
router.beforeEach((to, from, next) => {
  /* 路由发生变化修改页面title */
  if (to.meta.title) {
    document.title = to.meta.title;
  }
  next();
});
Vue.config.productionTip = false;

import vuetify from './plugins/vuetify';
import axios from './plugins/axios';
Vue.prototype.$axios = axios; // 修改原型链

new Vue({
  router,
  store,
  icons,
  vuetify,
  render: h => h(App)
}).$mount('#app');
