from app.libs.redprint import RedPrint
from app import db
from flask import request, jsonify, g
from app.models.member import Member, OauthMemberBind
from app.service.member_service import MemberService
api = RedPrint(name='user', description='用户视图')


@api.route('/login', methods=['GET', 'POST'])
def login():
    resp = {'code': 1, "msg": '成功', 'data': {}}
    code = request.form.get('code')
    nickName = request.form.get('nickName')
    avatarUrl = request.form.get('avatarUrl')
    gender = request.form.get('gender')
    if not all([code, nickName, avatarUrl, gender]):
        resp['code'] = -1
        resp['msg'] = '参数不全'
        return jsonify(resp)
    if len(code) <= 1:
        resp['code'] = '-1'
        resp['msg'] = 'code 不对'
        return jsonify(resp)

    openid = MemberService.getOpenid(code)
    if not openid:
        resp['code'] = -1
        resp['msg'] = '调用微信出错'
        return jsonify(resp)
    # 微信用户的唯一标识
    oauthmemberbind = OauthMemberBind.query.filter_by(openid=openid).first()

    if not oauthmemberbind:
        member = Member()
        member.nickname = nickName
        member.avatar = avatarUrl
        member.gender = gender
        member.salt = MemberService.getSalt()

        db.session.add(member)
        db.session.commit()

        # 关联表
        oauthmemberbind = OauthMemberBind()
        oauthmemberbind.openid = openid
        oauthmemberbind.client_type = '微信'
        oauthmemberbind.type = 1
        oauthmemberbind.member_id = member.id

        db.session.add(oauthmemberbind)
        db.session.commit()

        oauthmemberbind = oauthmemberbind

    member = Member.query.get(oauthmemberbind.member_id)
    token = '%s#%s' % (MemberService.geneAuthCode(member), member.id)
    resp['data'] = {'token': token}
    return jsonify(resp)


@api.route('/cklogin', methods=['GET', 'POST'])
def cklogin():
    resp = {'code': 1, "msg": '成功', 'data': {}}
    code = request.form.get('code')
    if len(code) <= 1:
        resp['code'] = '-2'
        resp['msg'] = 'code 不对'
        return jsonify(resp)

    openid = MemberService.getOpenid(code)  # 微信用户的
    if not openid:
        resp['code'] = -1
        resp['msg'] = '调用微信出错'
        return jsonify(resp)
    oauthmemberbind = OauthMemberBind.query.filter_by(openid=openid).first()

    if not oauthmemberbind:
        resp['code'] = -3
        resp['msg'] = '没有授权'
        return jsonify(resp)
    member = Member.query.get(oauthmemberbind.member_id)
    if not member:
        resp['code'] = -4
        resp['msg'] = '没有查到绑定的会员信息'
        return jsonify(resp)
    token = '%s#%s' % (MemberService.geneAuthCode(member), member.id)
    resp['data'] = {'token': token}
    return jsonify(resp)


@api.route('/info')
def info():
    resp = {'code': 1, "msg": '成功', 'data': {}}

    member = g.member

    if not member:
        resp['code'] = -1
        resp['msg'] = '身份验证失败'
        return jsonify(resp)
    user_info = {}
    user_info['nickname'] = member.nickname
    user_info['avatar_url'] = member.avatar

    resp['data']['user_info'] = user_info

    return jsonify(resp)

