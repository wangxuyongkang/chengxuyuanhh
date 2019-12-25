#启动停止和恢复mongodb数据库服务
# sudo service mongod(mongodb) stop|restart|start
# mongo  进入客户端

# 查看数据库
# show databases | show dbs
# 切换数据库
# use dbname(数据库名称)
# 删除数据库
# db.dropDatabase()
#创建数据
# use dbname(如果数据库下没有任何内容，则不显示)

#创建集合
# db.createCollection('students')
#不固定大小的集合：
# capped=True，
# size（设置能够存储的最大内容量，单位为字节）
# max （设置集合下能存储的最大的文档数量）
# # 如果size和max都存在，size的优先级更改
# db.createCollection(
#     'students1',
#     {
#         capped:true,
#         size:10000,
#         max:100
#     }
# )

#删除集合
#db.student1.drop()

#查看数据库下所有的集合
# show collections

#关于数据的操作
# 增
# db.dbname.insert({})
# db.dbname.insert([{},{},...])

#查
# db.dbname.find()   查询所有
# db.dbname.find().pretty()   查询所有(格式化输出)

#条件查询
# db.students.find({info:'睡觉'})
# db.students.find({info:'睡觉',name:'zhengchangfeng'})

# 统计集合下的文档数量
# db.students.find().count() => db.students.count()

#删除
# db.students.remove()  #删除所有
# db.students.remove({info:'睡觉'}) 根据条件删除
# db.students.remove({info:'睡觉'},1) 删除一条数据，1表示的是true，0表示false

# 改
# update:
# * upsert : 可选，这个参数的意思是，如果不存在update 的记录，是否插入objNew,true为插入，默认是false，不插 入。
# * multi : 可选，mongodb 默认是false,只更新找到的第 一条记录，如果这个参数为true,就把按条件查出来多条记录 全部更新。
#全文档更新，新的文档覆盖之前的文档，但是 id不变
# db.students.update(
# ... {age:17},
# ... {name:'xyk',age:16,info:'small boy'}
# ... )
#
#局部更新（指点属性更新）
# db.students.update(
# ... {age:16},
# ... {$set:{info:'big boy',age:18}}
# ... )

# #save()同样可以更新数据（全文档更新）
# 如果要跟新的文档存在集合下则进行全文档更新
# 如果不存在集合下，则添加一条新的文档
# db.students.save(
# ... {_id:'123',name:'zhangsan',age:18}
# ... )

#跳过
# skip(num)
# db.students.find().skip(1)

#限制返回
# limit(num)

# db.students.find().limit(1)

# 返回第二条数据
# db.students.find().skip(1).limit(1)
#注意skip()和limit()没有先后顺序

#查询运算符
# 比较运算符
#
# * 等于，默认是等于判断，没有运算符
# * 小于$lt
# * 小于或等于$lte
# * 大于$gt
# * 大于或等于$gte
# * 不等于$ne
# db.students.find({age:{$lt:18}})

#范围运算符
# $in 在某个范围
#db.students.find({age:{$in:[18,17,20]}})
# $nin 不在某个范围
# db.students.find({age:{$nin:[18,17,20]}})

#or and  的使用


#使用正则表达式  查询
# db.students.find({name:/^z/})
# db.students.find({name:{$regex:'^z'}})

#排序
# sort()
# -1 ： 降序  1：升序

#db.students.find().sort({age: -1, salary: 1})

#投影：只获取想要展示的字段
# db.students.find({},{age:1,_id:0})
# db.students.find({},{age:1,name:1,_id:0})

#去重
#distinct()去重
#db.students.distinct('age',{name:'zahngsan'})

#数据的备份和恢复
#mongodump -h 127.0.0.1:27017 -d class1808 -o /Users/ljh/Desktop/mongodbdata
#mongorestore -h 127.0.0.1:27017 -d class1808 --dir /Users/ljh/Desktop/mongodbdata/class1808

def insert_data():
    #数据的插入操作
    document1 = {
        'name':'libai',
        'age':2000,
        'info':'伟大的诗人'
    }
    document2 = {
        'name': 'hushi',
        'age': 200,
        'info': '伟大的现代诗人'
    }

    # col.insert_many()
    # col.insert_one()
    # 插入单挑数据
    # result = col.insert(document1)
    # print(result) #5c762f9dd097cbf08032c7d8 id串
    # result = col.insert_one(document2) #->InsertOneResult
    # from pymongo.results import InsertOneResult
    # print(result.inserted_id)

    # print(result.row)
    #多条数据插入
    # result = col.insert([document1,document2])
    # #[ObjectId('5c76310bd097cbf13f56a13f'), ObjectId('5c76310bd097cbf13f56a140')]
    # print(result)
    result = col.insert_many([document1,document2]) #->InsertManyResult
    print(result.inserted_ids)

def delete_data():
    #remove({}) 删除所有
    #multi=True:删除多条
    #multi=False:删除一条
    # result = col.remove({'name':'libai'},multi=False)
    # print(result)

    # result = col.delete_one({'name':'libai'}) #->DeleteResult object
    # from pymongo.results import DeleteResult
    # print(result.raw_result)
    result = col.delete_many({'name':'hushi'})
    print(result.raw_result)

def update_data():
    #multi=False 表示只修改一条
    #multi=True 表示只修改多条
    # result = col.update({'name':'libai'},{'$set':{'age':100}})
    # print(result)
    # col.update_one()
    # col.update_many()

    # 如果集合不存在该文档，则插入一条新的文档
    # result = col.save({'_id':'34567','name':'laoshe','age':150})
    # print(result)
    #如果集合下存在该文档，则进行全文档更新
    result = col.save(
        {"_id" : ObjectId("5c7632ebd097cbf24cbad3ea"),'name':'save更新数据'}
    )
    print(result)

def find_data():
    #查询数据
    # result = col.find({'name':'libai'}) #->Cursor object
    # print(result)
    # print([i for i in result])
    #skip,limit(跳过前两条，返回后三条)
    result = col.find({}).skip(2).limit(3)
    print([i for i in result])
    #sort排序(1:正序 -1：倒叙)
    result = col.find({}).sort('age',1)
    result = col.find({}).sort([('age1', 1),('age2', -1)])

    for i in result:
        print(i)





# pip3 install pymongo
import pymongo
from bson.objectid import ObjectId

if __name__ == '__main__':

    #创建数据库链接
    """ host=None,
        port=None,
    """
    # mongo_client = pymongo.MongoClient(
    #     host='118.24.255.219',
    #     port=27017
    # )
    # 链接方式一
    mongo_client = pymongo.MongoClient(
        host='127.0.0.1',
        port=27017
    )
    # mongo_client = pymongo.MongoClient(
    #     'mongodb://127.0.0.1:27017/'
    # )
    #获取要操作的数据库
    db = mongo_client['class1808']
    #获取要操作的集合
    col = db['students']

    # insert_data()
    # delete_data()
    # update_data()
    find_data()


