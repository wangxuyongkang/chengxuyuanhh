from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app import create_app
from app import db
import pymysql

pymysql.install_as_MySQLdb()
app = create_app('dev')
Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)




from app.models.lolhero import hero_lol
from flask import jsonify,request
@app.route('/hero')
def hero():
    resp = {'code': 1, "msg": '成功', 'data': {}}
    data = request.values
    page = int(data.get('page')) if 'page' in data else None
    if page:
        # 每页条数
        print(page, '='*100)
        pagesize = 1
        # 偏移量
        offset = (int(page) - 1) * pagesize

        # 分页
        lols = hero_lol.query.limit(pagesize).offset(offset).all()

        lists = []
        for lol in lols:
            temp_list = {}
            temp_list['text'] = lol.name
            temp_list['id'] = lol.id
            temp_list['url'] = lol.image
            lists.append(temp_list)
        resp['data']['lists'] = lists
        if len(lols) < pagesize:
            resp['data']['has_more'] = 0
        else:
            resp['data']['has_more'] = 1
        return jsonify(resp)



if __name__ == '__main__':
    manager.run()

