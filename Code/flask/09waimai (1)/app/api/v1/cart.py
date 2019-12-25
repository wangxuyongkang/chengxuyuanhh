from app.libs.redprint import RedPrint
from flask import request, jsonify, g
from app import db
from app.models.cart import MemberCart
from app.models.food import Food
import json
from app.service.url_service import UrlService

api = RedPrint(name='cart', description='购物车视图')


@api.route('/add', methods=['GET', 'POST'])
def add():
    try:
        resp = {'code': 1, "msg": '成功', 'data': {}}
        member = g.member
        if not member:
            resp['code'] = -1
            resp['msg'] = '验证失败'
            return jsonify(resp)

        data = request.values
        fid = int(data.get('fid'))
        num = int(data.get('num'))
        type = int(data.get('type'))
        # buy_now = int(data.get('buy_now')) if 'buy_now' in data else 0

        if not all([fid, num]):
            resp['code'] = -1
            resp['msg'] = '缺少参数'
            return jsonify(resp)

        if fid <= 0:
            resp['code'] = -1
            resp['msg'] = '参数错误'
            return jsonify(resp)
        if type == 0:  # 从加入购物车过来
            if num <= 0:
                resp['code'] = -1
                resp['msg'] = '参数错误'
                return jsonify(resp)
        else:  # 从加减号过来
            if num != 1 and num != -1:
                resp['code'] = -1
                resp['msg'] = '参数错误'
                return jsonify(resp)

        food = Food.query.get(fid)
        if not food:
            resp['code'] = -1
            resp['msg'] = '食品不存在'
            return jsonify(resp)
        if food.status != 1:
            resp['code'] = -1
            resp['msg'] = '食品已下架'
            return jsonify(resp)
        if num > food.stock:
            resp['code'] = -1
            resp['msg'] = '库存不足'
            return jsonify(resp)

        member_cart = MemberCart.query.filter_by(food_id=fid).filter_by(member_id=member.id).first()
        if not member_cart:
            member_cart = MemberCart()
            member_cart.member_id = member.id
            member_cart.food_id = fid
            member_cart.quantity = num
        else:
            if member_cart.quantity  >1 or num >=1:
                member_cart.quantity +=num
                if member_cart.quantity > food.stock:
                    resp['code'] = -1
                    resp['msg'] = '购物车数量大于库存量'
                    return jsonify(resp)
        db.session.add(member_cart)
        db.session.commit()
        # cart_id = member_cart.id
        # resp['msg'] = '传参成功'
        # if buy_now:
        #     resp['data']['cart_id'] = cart_id
        # else:
        #     resp['data']['cart_id'] = 0
        return jsonify(resp)
    except Exception as e:
        resp['code'] = -1
        resp['msg'] = '参数错误'
        return jsonify(resp)

@api.route('/list')
def list():
    # 验证登陆
    # 2检查会员购物车
    # 3根据购物车去查food表
    # 4构建数据(食品数据)
    resp = {'code': 1, "msg": '成功', 'data': {}}
    member = g.member
    if not member:
        resp['code'] = -1
        resp['msg'] = '验证失败'
        return jsonify(resp)
    membercarts = MemberCart.query.filter_by(member_id=member.id).all()
    list = []
    totalPrice = 0
    for mc in membercarts:
        temp_food = {}
        food = Food.query.get(mc.food_id)
        if not food or food.status != 1:
            continue
        temp_food['id'] = mc.id
        temp_food['food_id'] = mc.food_id
        temp_food['pic_url'] = UrlService.BuildStaticUrl(food.main_image)
        temp_food['price'] = str(food.price)
        temp_food['name'] = food.name
        temp_food['active'] = 'true'
        temp_food['number'] = mc.quantity

        totalPrice += mc.quantity * food.price
        list.append(temp_food)
    resp['data']['list'] = list
    resp['data']['totalPrice'] = str(totalPrice)

    return jsonify(resp)


@api.route('/delete', methods=['GET', 'POST'])
def delete():
    resp = {'code': 1, "msg": '成功', 'data': {}}
    member = g.member
    if not member:
        resp['code'] = -1
        resp['msg'] = '验证失败'
        return jsonify(resp)

    ids = request.form.get('ids')
    """
    :return:
    """
    if not ids:
        resp['code'] = -1
        resp['msg'] = '参数有误'
        return jsonify(resp)
    ids = json.loads(ids)
    for id in ids:
        membercart = MemberCart.query.get(id)
        if not membercart:
            continue
        db.session.delete(membercart)
        db.session.commit()
    return jsonify(resp)
    # 删除购物车
