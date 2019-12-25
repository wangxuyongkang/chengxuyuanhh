from app.libs.redprint import RedPrint
from app import db
from flask import request, jsonify, current_app
from app.models.food import Food, Category
from app.service.url_service import UrlService

api = RedPrint(name='food', description='食品视图')
"""
            banners: [
                {
                    "id": 1,
                    "pic_url": "/images/food.jpg"
                },
                {
                    "id": 2,
                    "pic_url": "/images/food.jpg"
                },
                {
                    "id": 3,
                    "pic_url": "/images/food.jpg"
                }
            ],
            categories: [
                {id: 0, name: "全部"},
                {id: 1, name: "川菜"},
                {id: 2, name: "东北菜"},
            ],
"""


@api.route('/search')
def search():
    resp = {'code': 1, "msg": '成功', 'data': {}}
    foods = Food.query.filter_by(status=1).limit(3).all()
    # 轮播图
    banners = []
    for food in foods:
        temp_food = {}
        temp_food['id'] = food.id
        temp_food['pic_url'] = UrlService.BuildStaticUrl(food.main_image)
        print(temp_food['pic_url'])
        banners.append(temp_food)
    # 分类
    categorys = Category.query.filter_by(status=1).all()
    categories = []
    # 假数据
    categories.append({'id': 0, 'name': '全部'})
    for category in categorys:
        temp_categroy = {}
        temp_categroy['id'] = category.id
        temp_categroy['name'] = category.name
        categories.append(temp_categroy)
    resp['data']['banners'] = banners
    resp['data']['categories'] = categories

    return jsonify(resp)


# import time
@api.route('/all')
def all():
    # time.sleep(5)
    resp = {'code': 1, "msg": '成功', 'data': {}}

    data = request.values

    category_id = data.get('category_id') if 'category_id' in data else "0"
    page = data.get('p') if 'p' in data else "1"

    if not category_id.isdigit():
        resp['code'] = -1
        resp['msg'] = '参数有误'
        return jsonify(resp)

    if not page.isdigit():
        resp['code'] = -1
        resp['msg'] = '参数有误'
        return jsonify(resp)

    category_id = int(category_id)
    page = int(page)

    pagesize = 1  # 每一页返回一条数据

    offset = (page - 1) * pagesize

    foods = Food.query.filter(Food.status == 1).order_by(Food.month_count.desc(), Food.id)
    # 分类
    if category_id > 0:
        foods = foods.filter_by(cat_id=category_id)
    # 分页
    if page > 0:
        foods = foods.offset(offset).limit(pagesize).all()

    goods = []

    for food in foods:
        temp_food = {}
        temp_food['id'] = food.id
        temp_food['name'] = food.name
        temp_food['min_price'] = str(food.price)
        temp_food['price'] = str(food.price)
        temp_food['pic_url'] = UrlService.BuildStaticUrl(food.main_image)
        goods.append(temp_food)

    resp['data']['goods'] = goods

    if len(foods) < pagesize:
        resp['data']['has_more'] = 0
    else:
        resp['data']['has_more'] = 1
    return jsonify(resp)


@api.route('/info')
def info():
    '''
    "info": {
                "id": 1,
                "name": "小鸡炖蘑菇",
                "summary": '<p>多色可选的马甲</p><p><img src="http://www.timeface.cn/uploads/times/2015/07/071031_f5Viwp.jpg"/></p><p><br/>相当好吃了</p>',
                "total_count": 2,
                "comment_count": 2,
                "stock": 2,
                "price": "80.00",
                "main_image": "/images/food.jpg",
                "pics": [ '/images/food.jpg','/images/food.jpg' ]
            },
    :return:
    '''
    resp = {'code': 1, "msg": '成功', 'data': {}}
    data = request.args.get('fid')
    print(data)
    # fid = data.get('fid')
    fid = int(data)
    food = Food.query.filter_by(id = fid).first()

    temp_info = {}
    temp_info['id'] = food.id
    temp_info['name'] = food.name
    temp_info['summary'] = food.summary
    temp_info['total_count'] = food.total_count
    temp_info['stock'] = food.stock
    temp_info['price'] = str(food.price)
    temp_info['main_image'] = UrlService.BuildStaticUrl(food.main_image)
    temp_info['pics'] = [UrlService.BuildStaticUrl(food.main_image)]


    resp['data']['goods'] = temp_info
    return jsonify(resp)

# return jsonify(resp)
