from app.libs.redprint import RedPrint
from flask import request,jsonify
from app.models.lolhero import hero_lol

api = RedPrint(name='hero', description='英雄视图')


@api.route('/hero')
def hero():
    resp = {'code': 1, "msg": '成功', 'data': {}}
    lols = hero_lol.query.filter_by(id).all()


    '''
    {
                url: 'https://ss0.bdstatic.com/70cFuHSh_Q1YnxGkpoWK1HF6hhy/it/u=8017613,3291049031&fm=26&gp=0.jpg',
                text: '卡牌大师 - 崔斯特',
                id: 3
            },
    '''

    lists = []
    for lol in lols:
        temp_list = {}
        temp_list['id'] = lol.id
        temp_list['text'] = lol.name
        temp_list['url'] = lol.image
        lists.append(temp_list)
    resp['data']['lists'] = lists
    return jsonify(resp)