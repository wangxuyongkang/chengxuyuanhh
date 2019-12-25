// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
// 全局引入共用CSS
import '../styles/common.css'
// 引入字体样式
import '../styles/fonts/iconfont.css'
// 全局引入路由配置
import router from './router'
// // 引入Mock数据方便测试接口
// import '../mock/mock'
// 全局状态控制引入
import store from './store/store'
// 全局加载ajax拦截器
import './axios'

Vue.config.productionTip = false

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  store,
  components: { App },
  template: '<App/>'
})
