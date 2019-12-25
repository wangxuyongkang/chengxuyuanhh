from app.libs.redprint import RedPrint
from flask import request, jsonify, g
from app.models.address import MemberAddress
from app import db

api = RedPrint(name='address', description='订单视图')


@api.route('/set', methods=['POST'])
def set():
    resp = {'code': 1, "msg": '成功', 'data': {}}

    member = g.member

    if not member:
        resp['code'] = -1
        resp['msg'] = '身份验证失败'
        return jsonify(resp)

    nickname = request.form.get('nickname')
    mobile = request.form.get('mobile')
    province_id = request.form.get('province_id')
    province_str = request.form.get('province_str')
    city_id = request.form.get('city_id')
    city_str = request.form.get('city_str')
    area_id = request.form.get('area_id')
    area_str = request.form.get('area_str')
    address = request.form.get('address')
    if not all([nickname, mobile, province_str, city_id]):
        resp['code'] = -1
        resp['msg'] = '参数不全'
        return jsonify(resp)
    memberaddress = MemberAddress()
    memberaddress.nickname = nickname
    memberaddress.mobile = mobile
    memberaddress.province_id = province_id
    memberaddress.province_str = province_str
    memberaddress.city_id = city_id
    memberaddress.area_id = area_id
    memberaddress.area_str = area_str
    memberaddress.address = address
    memberaddress.member_id = member.id
    count = MemberAddress.query.filter_by(member_id=member.id, is_default=1).count()
    if count == 0:
        memberaddress.is_default = 1
    else:
        memberaddress.is_default = 0
    db.session.add(memberaddress)
    db.session.commit()

    return jsonify(resp)


@api.route('/list')
def list():
    resp = {'code': 1, "msg": '成功', 'data': {}}

    member = g.member

    if not member:
        resp['code'] = -1
        resp['msg'] = '身份验证失败'
        return jsonify(resp)
    memberaddress = MemberAddress.query.filter_by(member_id=member.id).all()
    addressList = []

    for addres in memberaddress:
        temp_addres = {}
        temp_addres['id'] = addres.id
        temp_addres['name'] = addres.nickname
        temp_addres['mobile'] = addres.mobile
        temp_addres['isDefault'] = addres.is_default
        temp_addres['detail'] = addres.province_str+addres.city_str +addres.area_str+addres.address

        addressList.append(temp_addres)
    resp['data']['addressList'] = addressList

    return jsonify(resp)
