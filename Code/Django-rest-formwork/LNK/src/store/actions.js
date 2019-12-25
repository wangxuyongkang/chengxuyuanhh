import {SET_INFO, SET_SHOPLIST} from './mutation-types'

// 提交mutation
function makeAction (type) {
  return ({commit}, ...args) => commit(type, ...args)
}

export default {
  setInfo: makeAction(SET_INFO),
  setShopList: makeAction(SET_SHOPLIST)
}
