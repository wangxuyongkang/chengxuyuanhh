import axios from 'axios'

// 全局状态控制引入
import store from '../store/store'

// http request 拦截器
axios.interceptors.request.use(
  config => {
    // 判断是否存在token，如果存在的话
    if (store.state.userInfo.token) {
      // 则每个http header都加上token
      config.headers.Authorization = `JWT ${store.state.userInfo.token}`
    }
    return config
  },
  err => {
    return Promise.reject(err)
  }
)
// http response 拦截器
axios.interceptors.response.use(
  undefined,
  error => {
    let res = error.response
    switch (res.status) {
      case 401:
        console.log('未登录')
        break
      case 403:
        console.log('您没有该操作权限')
        break
      case 500:
        console.log('服务器错误')
        break
    }
    // 返回接口返回的错误信息
    return Promise.reject(error.response.data)
  }
)
