from app.libs.redprint import RedPrint
from flask import request, jsonify, g
import json
from app.service.WeChatService import WeChatService
from app.service.order_servcie import OrderService
from app.service.url_service import UrlService
from app.models.cart import MemberCart
from app.models.food import Food
from app.models.address import MemberAddress
from app.models.order import PayOrder, PayOrderItem
from app.models.member import OauthMemberBind
from app import db

api = RedPrint(name='order', description='订单视图')


@api.route('/info', methods=['GET', 'POST'])
def info():
    '''
    goods_list: [
            {
                id:22,
                name: "小鸡炖蘑菇",
                price: "85.00",
                pic_url: "/images/food.jpg",
                number: 1,
            },
            {
                id:22,
                name: "小鸡炖蘑菇",
                price: "85.00",
                pic_url: "/images/food.jpg",
                number: 1,
            }
        ],
          default_address: {
            name: "编程浪子",
            mobile: "12345678901",
            detail: "上海市浦东新区XX",
        },
        yun_price: "1.00",
        pay_price: "85.00",
        total_price: "86.00",
        params: null,
        ids : []
    },
    :return:
    '''
    resp = {'code': 1, "msg": '成功', 'data': {}}
    member = g.member
    if not member:
        resp['code'] = -1
        resp['msg'] = '身份验证失败'
        return jsonify(resp)
    ids = request.form.get('ids')
    if not ids:
        resp['code'] = -1
        resp['msg'] = '参数不全'
        return jsonify(resp)

    ids = json.loads(ids)  # 转换成列表
    goods_list = []
    yun_price = 0
    pay_price = 0

    for id in ids:
        membercart = MemberCart.query.get(id)
        if not membercart:
            continue
        food = Food.query.get(membercart.food_id)
        if not food:
            continue

        temp_food = {}
        temp_food['id'] = food.id
        temp_food['name'] = food.name
        temp_food['price'] = str(food.price)
        temp_food['pic_url'] = UrlService.BuildStaticUrl(food.main_image)
        temp_food['number'] = membercart.quantity

        pay_price += membercart.quantity * food.price
        goods_list.append(temp_food)

        memberaddress = MemberAddress.query.filter_by(member_id=member.id, is_default=1).first()
        default_address = {
            'id': memberaddress.id,
            'name': memberaddress.nickname,
            'mobile': memberaddress.mobile,
            'detail': memberaddress.province_str + memberaddress.city_str + memberaddress.area_str + memberaddress.address
        }
    resp['data']['goods_list'] = goods_list
    resp['data']['default_address'] = default_address
    resp['data']['yun_price'] = str(yun_price)
    resp['data']['pay_price'] = str(pay_price)
    resp['data']['total_price'] = str(yun_price + pay_price)

    return jsonify(resp)



@api.route('/info1', methods=['GET', 'POST'])
def info1():
    resp = {'code': 1, "msg": '成功', 'data': {}}
    member = g.member
    if not member:
        resp['code'] = -1
        resp['msg'] = '身份验证失败'
        return jsonify(resp)
    id = request.form.get('id')
    num = request.form.get('num')
    if not id and num:
        resp['code'] = -1
        resp['msg'] = '参数不全'
        return jsonify(resp)
    id = int(id)
    num = int(num)
    goods_list = []
    yun_price = 0
    pay_price = 0


    food = Food.query.get(id)
    if not food or food.status !=1:
        resp['code'] = -1
        resp['msg'] = '商品不存在'
        return jsonify(resp)

    temp_food = {}
    temp_food['id'] = food.id
    temp_food['name'] = food.name
    temp_food['price'] = str(food.price)
    temp_food['pic_url'] = UrlService.BuildStaticUrl(food.main_image)
    temp_food['number'] = num

    pay_price = num * food.price
    goods_list.append(temp_food)

    memberaddress = MemberAddress.query.filter_by(member_id=member.id, is_default=1).first()
    default_address = {
        'id': memberaddress.id,
        'name': memberaddress.nickname,
        'mobile': memberaddress.mobile,
        'detail': memberaddress.province_str + memberaddress.city_str + memberaddress.area_str + memberaddress.address
    }
    resp['data']['goods_list'] = goods_list
    resp['data']['default_address'] = default_address
    resp['data']['yun_price'] = str(yun_price)
    resp['data']['pay_price'] = str(pay_price)
    resp['data']['total_price'] = str(yun_price + pay_price)

    return jsonify(resp)



@api.route('/create',methods=['POST'])
def create():
    try:
        resp = {'code': 1, 'msg': '成功', 'data': {}}

        member = g.member

        if not member:
            resp['code'] = -1
            resp['msg'] = '验证失败'
            return jsonify(resp)
        ids = request.form.get('ids')
        address_id = request.form.get('address_id')
        note = request.form.get('note')

        if not all([ids, address_id]):
            resp['code'] = -1
            resp['msg'] = '参数错误'
            return jsonify(resp)

        address_id = int(address_id)

        if address_id <= 0:
            resp['code'] = -1
            resp['msg'] = '参数错误'
            return jsonify(resp)

        ids = json.loads(ids)

        pay_price = 0
        yun_price = 0
        goods_id = [] # 商品的ids

        for id in ids:
            membercart = MemberCart.query.get(id)
            goods_id.append(membercart.food_id)
            if not membercart:
                resp['code'] = -1
                resp['msg'] = '购物车不存在'
                return jsonify(resp)

            food = Food.query.get(membercart.food_id)

            if not food:
                resp['code'] = -1
                resp['msg'] = '商品不存在'
                return jsonify(resp)
            if food.status != 1:
                resp['code'] = -1
                resp['msg'] = '商品已下架'
                return jsonify(resp)
            pay_price += food.price * membercart.quantity
        memberaddress = MemberAddress.query.get(address_id)
        if not memberaddress:
            resp['code'] = -1
            resp['msg'] = '地址不存在'
            return jsonify(resp)
        payorder = PayOrder()
        payorder.order_sn = geneOrderSn()
        payorder.total_price = pay_price + yun_price
        payorder.yun_price = yun_price
        payorder.pay_price = pay_price
        payorder.note = note
        payorder.status = -8
        payorder.express_status = -8
        payorder.express_address_id = address_id
        payorder.express_info = memberaddress.province_str + memberaddress.city_str + memberaddress.area_str + memberaddress.address
        payorder.comment_status = -8
        payorder.member_id = member.id

        db.session.add(payorder)
        #悲观锁
        foods = db.session.query(Food).filter(Food.id.in_(goods_id)).with_for_update().all()

        temp_stock = {} # 临时库存
        for food in foods:
            temp_stock[food.id] = food.stock
        for id in ids:
            membercart = MemberCart.query.get(id)
            if membercart.quantity > temp_stock[membercart.food_id]:
                resp['code'] = -1
                resp['msg'] = '库存不足'
                return jsonify(resp)
            food = Food.query.filter(Food.id==membercart.food_id).update({
                'stock':temp_stock[membercart.food_id]-membercart.quantity
            })

            if not food:
                raise Exception('未知错误')

            payorderitem = PayOrderItem()
            payorderitem.quantity = membercart.quantity
            payorderitem.price = Food.query.get(membercart.food_id).price
            payorderitem.note = note
            payorderitem.status = 1
            payorderitem.pay_order_id = payorder.id
            payorderitem.member_id = member.id
            payorderitem.food_id = membercart.food_id
            db.session.add(payorderitem)
        db.session.commit()
        for id in ids:
            membercart = MemberCart.query.get(id)
            db.session.delete(membercart)
            db.session.commit()
        return jsonify(resp)
    except Exception as e:
        db.session.rollback()
        resp['code'] = -2
        resp['msg'] = '未知错误'
        return jsonify(resp)

@api.route('/create1',methods=['POST'])
def create1():
    try:
        resp = {'code': 1, 'msg': '成功', 'data': {}}

        member = g.member

        if not member:
            resp['code'] = -1
            resp['msg'] = '验证失败'
            return jsonify(resp)
        id = request.form.get('id')#食品ID
        address_id = request.form.get('address_id')
        note = request.form.get('note')
        num = request.form.get('num')
        id = int(id)
        num = int(num)
        address_id = int(address_id)

        if not all([id, address_id,num]):
            resp['code'] = -1
            resp['msg'] = '参数错误'
            return jsonify(resp)

        if num <= 0:
            resp['code'] = -1
            resp['msg'] = '参数错误'
            return jsonify(resp)

        if address_id <= 0:
            resp['code'] = -1
            resp['msg'] = '参数错误'
            return jsonify(resp)

        pay_price = 0
        yun_price = 0
        goods_id = [] # 商品的ids

        food = Food.query.get(id)

        if not food:
            resp['code'] = -1
            resp['msg'] = '商品不存在'
            return jsonify(resp)
        if food.status != 1:
            resp['code'] = -1
            resp['msg'] = '商品已下架'
            return jsonify(resp)
        pay_price = food.price * num

        memberaddress = MemberAddress.query.get(address_id)
        if not memberaddress:
            resp['code'] = -1
            resp['msg'] = '地址不存在'
            return jsonify(resp)
        payorder = PayOrder()
        payorder.order_sn = geneOrderSn()
        payorder.total_price = pay_price + yun_price
        payorder.yun_price = yun_price
        payorder.pay_price = pay_price
        payorder.note = note
        payorder.status = -8
        payorder.express_status = -8
        payorder.express_address_id = address_id
        payorder.express_info = memberaddress.province_str + memberaddress.city_str + memberaddress.area_str + memberaddress.address
        payorder.comment_status = -8
        payorder.member_id = member.id

        db.session.add(payorder)
        #悲观锁
        food = db.session.query(Food).filter(Food.id==id).with_for_update().first()

        temp_stock = {} # 临时库存

        temp_stock[food.id] = food.stock

        if num > temp_stock[id]:
            resp['code'] = -1
            resp['msg'] = '库存不足'
            return jsonify(resp)
        food1 = Food.query.filter(Food.id==id).update({
            'stock':temp_stock[id]-num
        })

        if not food1:
            raise Exception('未知错误')

        payorderitem = PayOrderItem()
        payorderitem.quantity = num
        payorderitem.price = food.price
        payorderitem.note = note
        payorderitem.status = 1
        payorderitem.pay_order_id = payorder.id
        payorderitem.member_id = member.id
        payorderitem.food_id = id
        db.session.add(payorderitem)
        db.session.commit()

        return jsonify(resp)
    except Exception as e:
        print(e)
        db.session.rollback()
        resp['code'] = -2
        resp['msg'] = '未知错误'
        return jsonify(resp)


    """
    生成附表扣库存
    """

@api.route('/allorder')
def allorder():
    resp = {'code': 1, 'msg': '成功', 'data': {}}
    try:
        member = g.member

        if not member:
            resp['code'] = -1
            resp['msg'] = '验证失败'
            return jsonify(resp)

        status = request.args.get('status')

        if not status:
            resp['code'] = -1
            resp['msg'] = '参数不全'
            return jsonify(resp)

        status = int(status)
        '''
        order_list: [
                {
					status: -8,
                    status_desc: "待支付",
                    date: "2018-07-01 22:30:23",
                    order_number: "20180701223023001",
                    note: "记得周六发货",
                    total_price: "85.00",
                    goods_list: [
                        {
                            pic_url: "/images/food.jpg"
                        },
                        {
                            pic_url: "/images/food.jpg"
                        }
                    ]
                }
            ]
        '''
        payorders = PayOrder.query.filter_by(status=status).all()

        order_list  = []

        for payorder in payorders:
            temp_payorder = {}
            goods_list = [] # 商品图片
            temp_payorder['status'] = payorder.status
            temp_payorder['status_desc'] = payorder.status_desc
            temp_payorder['date'] = payorder.create_time.strftime('%Y-%m-%d %H:%M:%S')
            temp_payorder['order_sn'] = payorder.order_sn
            temp_payorder['order_number'] =str(payorder.create_time.strftime('%Y%m%d%H%M%S'))+str(payorder.id).zfill(5)
            temp_payorder['note'] = payorder.note
            temp_payorder['total_price'] = str(payorder.total_price)


            payorderitems = PayOrderItem.query.filter_by(pay_order_id=payorder.id).all()

            for payorderitem in payorderitems:
                food = Food.query.get(payorderitem.food_id)
                temp_food = {}
                temp_food['id'] = payorderitem.food_id
                temp_food['pic_url'] = UrlService.BuildStaticUrl(food.main_image)
                goods_list.append(temp_food)
                #goods_list.append(UrlService.BuildStaticUrl(food.main_image))

            temp_payorder['goods_list'] = goods_list
            order_list.append(temp_payorder)
            print(order_list)
        resp['data']['order_list'] = order_list

        return jsonify(resp)
    except Exception as e:
        print(e)
        resp['code'] = -1
        resp['msg'] = '异常错误'
        return jsonify(resp)


@api.route('/pay')
def pay():
    resp = {'code': 200, 'msg': '操作成功~', 'data': {}}
    member_info = g.member_info
    req = request.values
    # 接受参数
    order_sn = req['order_sn'] if 'order_sn' in req else ''
    # 去库找到该订单
    pay_order_info = PayOrder.query.filter_by(order_sn=order_sn, member_id=member_info.id).first()
    if not pay_order_info:
        resp['code'] = -1
        resp['msg'] = "系统繁忙。请稍后再试~"
        return jsonify(resp)
    # 找到该会员的信息
    oauth_bind_info = OauthMemberBind.query.filter_by(member_id=member_info.id).first()
    if not oauth_bind_info:
        resp['code'] = -1
        resp['msg'] = "系统繁忙。请稍后再试~~2"
        return jsonify(resp)

    config_mina = current_app.config['MINA_APP']
    notify_url = current_app.config['APP']['domain'] + config_mina['callback_url']
    # 为了将来推送支付结果
    # http://127.0.0.1:5000/api/v1/order/callback
    target_wechat = WeChatService(merchant_key=config_mina['paykey']) # 商户密钥 目前没有

    data = {
        'appid': config_mina['appid'],# 小程序id
        'mch_id': config_mina['mch_id'], #商户号没有
        'nonce_str': target_wechat.get_nonce_str(),# 随机字符串
        'body': '订餐',  # 商品描述
        'out_trade_no': pay_order_info.order_sn,  # order_sn
        'total_fee': int(pay_order_info.total_price * 100),# 钱  单位是分
        'notify_url': notify_url, # 回调地址
        'trade_type': "JSAPI",# jsai
        'openid': oauth_bind_info.openid,# 开发平台的id
        'spbill_create_ip':'127.0.0.1'# ip地址
    }

    pay_info = target_wechat.get_pay_info(pay_data=data)

    # # 保存prepay_id为了后面发模板消息
    # pay_order_info.prepay_id = pay_info['prepay_id']
    # db.session.add(pay_order_info)
    # db.session.commit()

    resp['data']['pay_info'] = pay_info
    return jsonify(resp)

from flask import current_app
@api.route("/callback", methods=["POST"])
def orderCallback():
    result_data = {
        'return_code': 'SUCCESS',
        'return_msg': 'OK'
    }
    header = {'Content-Type': 'application/xml'}
    config_mina = current_app.config['MINA_APP']
    target_wechat = WeChatService(merchant_key=config_mina['paykey'])
    # 解析微信推送过来的xml 支付结果  改成字典
    callback_data = target_wechat.xml_to_dict(request.data)

    # 取出这里面sign
    sign = callback_data['sign']

    # 在pop掉sign
    callback_data.pop('sign')

    #在把这个字典进行签名 返回一个sign
    gene_sign = target_wechat.create_sign(callback_data) # 在加密
    # 如果取出的sign和加密后的sign不一样
    if sign != gene_sign:
        result_data['return_code'] = result_data['return_msg'] = 'FAIL'
        return target_wechat.dict_to_xml(result_data), header
    # 如果返回的不等于成功
    if callback_data['result_code'] != 'SUCCESS':
        result_data['return_code'] = result_data['return_msg'] = 'FAIL'
        return target_wechat.dict_to_xml(result_data), header
    # 订单号取出来
    order_sn = callback_data['out_trade_no']

    # 根据订单查这个订单的信息
    pay_order_info = PayOrder.query.filter_by(order_sn=order_sn).first()
    if not pay_order_info:
        result_data['return_code'] = result_data['return_msg'] = 'FAIL'
        return target_wechat.dict_to_xml(result_data), header

    # 如果付款的金额和推送过来的支付金额不一样
    if int(pay_order_info.total_price * 100) != int(callback_data['total_fee']):
        result_data['return_code'] = result_data['return_msg'] = 'FAIL'
        return target_wechat.dict_to_xml(result_data), header

    if pay_order_info.status == 1:
        return target_wechat.dict_to_xml(result_data), header

    # 把订单更新待发货
    OrderService.orderSuccess(pay_order_id=pay_order_info.id, params={"pay_sn": callback_data['transaction_id']})
    return target_wechat.dict_to_xml(result_data), header



import hashlib
import time
import random

def geneOrderSn():
    m = hashlib.md5()
    sn = None
    while True:
        str = "%s-%s" % (int(round(time.time() * 1000)), random.randint(0, 9999999))
        m.update(str.encode("utf-8"))
        sn = m.hexdigest()
        if not PayOrder.query.filter_by(order_sn=sn).first():
            break
    return sn