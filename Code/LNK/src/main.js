// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
// 全局引用公用css
import '../styles/common.css'
// 引入字体样式
import '../styles/fonts/iconfont.css'
// 全局引用路由配置

import router from './router'
import store from './store/store'
// 引入mock数据方便测试
import '../mock/mock'
import './axios'
Vue.config.productionTip = false


/* eslint-disable no-new */
new Vue({
  el: '#app',
  store,
  router,
  components: { App },
  template: '<App/>'
})
