// 引入vue
import Vue from 'vue'
// 全局引入vuex
import Vuex from 'vuex'

import mutations from './mutations'
import actions from './actions'
import getters from './getters'

// 全局引用Cookie方法类
import cookie from '../../static/js/cookie'

// 全局注册Vuex
Vue.use(Vuex)

// 要管理的状态
const userInfo = {
  name: cookie.getCookie('name' || ''),
  token: cookie.getCookie('token' || '')
}
const goodsList = {
  totalPrice: '',
  goods_list: []
}

const state = {
  userInfo,
  goodsList
}

// 向外暴露store对象
export default new Vuex.Store({
  state,
  mutations,
  actions,
  getters
})
