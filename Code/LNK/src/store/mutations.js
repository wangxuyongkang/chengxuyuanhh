import {SET_INFO, SET_SHOPLIST} from './mutation-types'
import cookie from '../../static/js/cookie'
import {getShopCarts} from '../api/api'

export default {
  [SET_INFO] (state) {
    state.userInfo = {
      name: cookie.getCookie('name'),
      token: cookie.getCookie('token')
    }
    console.log(state.userInfo)
  },
  [SET_SHOPLIST] (state) { // 设置购物车数据
    if (cookie.getCookie('token') != null) {
      getShopCarts().then(response => {
        // console.log(response.data)
        // 更新Store数据
        state.goodsList.goods_list = response.data
        var totalPrice = 0
        response.data.forEach(function (entry) {
          totalPrice += entry.goods.shop_price * entry.nums
        })
        state.goodsList.totalPrice = totalPrice
      }).catch(error => {
        console.log(error)
      })
    }
  }
}
