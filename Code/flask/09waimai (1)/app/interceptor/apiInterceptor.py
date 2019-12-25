from app import app
from flask import request,jsonify,g,current_app
from app.models.member import Member
from app.service.member_service import  MemberService
@app.before_request
def before_request():
    #前端api
    ignore_urls = current_app.config.get('IGNORE_URLS')
    if request.path in ignore_urls:
        return
    #管理后台忽略
    if '/api' not in request.url or '/static' in request.url:
        return
    resp = {'code': 1, "msg": '成功', 'data': {}}
    g.member = None
    # f65fcaf908582872c8f9933ad5dccf2b#13  取到token
    token = request.headers.get('token')  # 发起request请求去headers拿到token值
    # 判断token是否有值
    if not token:
        resp['code'] = -1
        resp['msg'] = '必须登录'
        return jsonify(resp)
    # (f65fcaf908582872c8f9933ad5dccf2b,13)
    tuple_token = token.split('#')  # 以#号分割取到token#后面的用户id

    # 判断是否切割成功
    if len(tuple_token) != 2:
        resp['code'] = -1
        resp['msg'] = 'token错误'
        return jsonify(resp)

    # 查会员
    member = Member.query.get(tuple_token[1])

    # 如果查不到会员
    if not member:
        resp['code'] = -1
        resp['msg'] = '没有找到该用户'
        return jsonify(resp)

    # 根据查到的会员 生成token
    c_token = MemberService.geneAuthCode(member)

    # 根据生成的token跟取到token
    if c_token != tuple_token[0]:
        resp['code'] = -1
        resp['msg'] = 'token错误'
        return jsonify(resp)
    g.member = member
