import json
from flask import jsonify, request, g
from app.libs.redprint import RedPrint
from app.models.address import MemberAddress
from app.models.order import PayOrder
from app.models.comment import MemberComments
from app import db
from app.models.food import Food
from app.service.url_service import UrlService

api = RedPrint(name='comment', description='评价详情')


@api.route('/add', methods=['POST'])
def add():
    try:
        resp = {'code': 1, 'msg': '成功', 'data': {}}

        member = g.member
        if not member:
            resp['code'] = -1
            resp['msg'] = '验证失败'
            return jsonify(resp)

        order_sn = request.form.get('order_sn')
        score = request.form.get('score')
        content = request.form.get('content')

        if not all([order_sn, score, content]):
            resp['code'] = -1
            resp['msg'] = '参数不全'
            return jsonify(resp)

        if score not in ['10', '6', '0']:
            resp['code'] = -1
            resp['msg'] = '分数不对'
            return jsonify(resp)

        payorder = PayOrder.query.filter_by(order_sn=order_sn).first()
        print(payorder)

        # if not payorder:
        #     resp['code'] = -1
        #     resp['msg'] = '订单不存在'
        #     return jsonify(resp)

        membercomments = MemberComments()
        membercomments.pay_order_id = payorder.id
        membercomments.member_id = member.id
        membercomments.score = score
        membercomments.content = content

        db.session.add(membercomments)

        # payorder.status = 1
        # db.session.add(payorder)
        db.session.commit()

        return jsonify(resp)
    except Exception as e:
        print(e)
        resp['code'] = -3
        resp['msg'] = '已成'
        return jsonify(resp)



@api.route('/list1')
def list1():
    resp = {'code': 1, 'msg': '成功', 'data': {}}

    member = g.member
    if not member:
        resp['code'] = -1
        resp['msg'] = '验证失败'
        return jsonify(resp)

    membercomments = MemberComments.query.filter_by(member_id=member.id).all()

    list = []
    for mc in membercomments:
        temp_mc = {}
        temp_mc['date'] = mc.create_time.strftime('%Y-%m-%d')
        temp_mc['order_number'] = mc.pay_order_id
        temp_mc['content'] = mc.content

        list.append(temp_mc)
    resp['data']['list'] = list
    return jsonify(resp)
