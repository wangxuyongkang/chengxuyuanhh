// 使用Mock
var Mock = require('mockjs');
var category = require('./mock/categorys')
var hotSearch = require('./mock/hotSearch')
var categorysId = require('./mock/categorys_id')
var goods = require('./mock/goods')
var banners = require('./mock/banner')
var newopro = require('./mock/newopro')
var indexList = require('./mock/seriesList')
var login = require('./mock/login')
var productDetail = require('./mock/productDetail')

Mock.mock('/categorys/', category) // 所有类别
Mock.mock('/hotsearchs/', hotSearch) // 热词
Mock.mock(/\/categorys\/[0-9]+/, categorysId) // 指定类别的菜单列表
Mock.mock(/\/goods\/\?is_new=true/, newopro) // 首页新品newopro
Mock.mock(/\/goods\/[0-9A-Za-z]+/, productDetail) // 商品详情数据
Mock.mock(/\/goods\/.+/, goods) // 列表页商品
Mock.mock('/getBanner/', banners) // 首页banners
Mock.mock('/indexgoods/', indexList) // 首页indexList
Mock.mock('/login/', login) // 登录
Mock.mock('/users/', login) // 注册

Mock.mock('/currentLoc/', // 当前位置
  [
    {
      id: 0,
      name: '首页'
    },
    {
      id: 2,
      name: '酒水饮料'
    },
    {
      id: 21,
      name: '白酒'
    },
    {
      id: 213,
      name: '茅台'
    }
  ]
)
Mock.mock('/priceRange/', // 价格区间
  [
    {
      min: 1,
      max: 25
    },
    {
      min: 25,
      max: 50
    },
    {
      min: 50,
      max: 75
    },
    {
      min: 75,
      max: 100
    }
  ]
)
Mock.mock('/code/', {state: 'ok'}) // 发送短信
Mock.mock(/\/userfavs\/[0-9]+/, 'get', {hasFav: true}) // 是否收藏某商品
Mock.mock('/userfavs/', 'post', {}) // 添加收藏
Mock.mock(/\/userfavs\/[0-9]+/, 'delete', {}) // 取消收藏
Mock.mock('/shopcarts/', 'post', {}) // 某个商品加入购物车
Mock.mock('/shopcarts/', 'get', // 请求购物车列表数据
  [
    {
      goods: {
        id: '23243453',
        image: '../../../static/images/productDetail/images/1_thumb_G_1449024889033.jpg',
        title: '新鲜水果甜蜜香脆单果约800克',
        shop_price: 123
      },
      nums: 1,
      total: 123
    },
    {
      goods: {
        id: '23243454',
        image: '../../../static/images/productDetail/images/21_thumb_G_1448946793103.jpg',
        title: '人头马进口XO',
        shop_price: 123
      },
      nums: 2,
      total: 123
    },
    {
      goods: {
        id: '23243455',
        image: '../../../static/images/productDetail/images/30_thumb_G_1448948662661.jpg',
        title: '菠萝蜜新鲜水果甜蜜保鲜1000克',
        shop_price: 123
      },
      nums: 4,
      total: 123
    }
  ]
)
Mock.mock(/\/shopcarts\/[0-9]+/, 'delete', {}) // 移除购物车某个商品
Mock.mock(/\/shopcarts\/[0-9]+/, 'patch', {}) // 更新购物车商品信息
Mock.mock('/shopcarts/', 'delete', {}) // 清空购物车

Mock.mock(/\/address\/[0-9]+/, 'patch', {}) // 更新收货人信息
Mock.mock(/\/address\/[0-9]+/, 'delete', {}) // 删除收货人信息
Mock.mock('/address/', 'post', {}) // 添加收货人信息
Mock.mock('/address/', // 获得所有配送地址
  [
    {
      id: '222',
      province: '四川省',
      city: '成都市',
      district: '双流区',
      address: '锦绣花园',
      signer_mobile: 18311220453,
      signer_name: '李易峰',
      note: '发顺丰'
    },
    {
      id: '333',
      province: '辽宁省',
      city: '铁岭市',
      district: '清河区',
      address: '象牙山村',
      signer_mobile: 18311220453,
      signer_name: '赵本山',
      note: '发顺丰'
    }
  ]
)
Mock.mock('/orders/', 'post', {alipay_url: '../../../static/alipay.html'}) // 下单
Mock.mock('/orders/', // 获取所有订单
  [
    {
      id: 111,
      order_sn: 122324, // 订单号
      add_time: '2017-07-07 13:48:53', // 下单时间
      order_mount: '123', // 订单总金额
      pay_status: 'paying'
    },
    {
      id: 222,
      order_sn: 122324, // 订单号
      add_time: '2017-07-07 13:48:53', // 下单时间
      order_mount: '123', // 订单总金额
      pay_status: 'TRADE_SUCCESS'
    }
  ]
)
Mock.mock(/\/orders\/[0-9]+/, 'delete', {}) // 取消订单
Mock.mock(/\/orders\/[0-9]+/, // 获取订单详细信息
  {
    order_sn: 201902231458200001,
    // pay_status: 'TRADE_SUCCESS', // 已支付
    pay_status: 'paying', // 待支付
    alipay_url: '../../../static/alipay.html',
    goods: [
      {
        id: 1,
        goods: {
          name: '澳洲进口牛尾巴300g新鲜肥牛肉',
          shop_price: 255
        },
        goods_num: 2
      },
      {
        id: 2,
        goods: {
          name: '爱食派内蒙古呼伦贝尔冷冻生鲜牛腱子肉1000g',
          shop_price: 232
        },
        goods_num: 1
      }
    ],
    signer_name: 'dsdsd',
    address: '地址',
    singer_mobile: 13834442233
  }
)
Mock.mock('/users/1/', 'get', // 获取用户信息
  {
    name: '胡歌',
    birthday: '1982-09-20', // 格式是xxxx-xx-xx
    gender: 'male',
    email: '888888@163.com',
    mobile: '13288888888'
  }
)
Mock.mock('/users/1/', 'patch', {}) // 修改用户信息
Mock.mock('/messages/', 'get', // 获取留言列表
  [
    {
      id: 88,
      message_type: 4,
      subject: '我要退货',
      add_time: '2019-02-24 11:03',
      message: '春节前能穿，春节之后还没洗，衣服就小了，申请7天无理由退货',
      file: '../../../static/images/message/images/O1CN019CJEMT2KRK6yAjOy5.jpg'
    },
    {
      id: 99,
      message_type: 1,
      subject: '送货时间别在晚上',
      add_time: '2019-02-12 08:03',
      message: '单位晚上没人，请白天送货，谢谢！',
      file: '../../../static/images/message/images/3_P_1448945490837.jpg'
    }
  ]
)
Mock.mock(/\/messages\/[0-9]+/, 'delete', {}) // 删除留言
Mock.mock('/messages/', 'post', {}) // 添加留言
