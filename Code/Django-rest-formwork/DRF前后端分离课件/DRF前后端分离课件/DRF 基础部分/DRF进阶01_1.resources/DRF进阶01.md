---
title: DRF进阶01
tags: 
notebook: Study_and_prepare
---

# 内容回顾 
## 1、开发模式 
- 普通的开发方式(前后端放在一起写)
- 前后端分离(Ajax) 
## 2、后端开发
- 后端为前端提供URL(API/接口的开发)
- 注: 返回HttpResponse(render和redirect就用不上)
### 举例:第一个简单的接口(不依赖任何工具) 
- 创建项目

![微信截图_20190105170805](http://md.100cxy.com/%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_20190105170805.png)

- 配置视图 

![微信截图_20190105171427](http://md.100cxy.com/%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_20190105171427.png)

- 配置路由 

![微信截图_20190105171324](http://md.100cxy.com/%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_20190105171324.png)

- 浏览器效果(可以通过url获取到数据) 

![微信截图_20190105171523](http://md.100cxy.com/%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_20190105171523.png)


## 3、Django的 FBV和CBV
- FBV：Function-base views 基于函数的视图
- CBV：Class-based views 基于类的视图 

![微信截图_20190105172003](http://md.100cxy.com/%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_20190105172003.png)
### 举例:CBV 
- 编写视图

![微信截图_20190105172738](http://md.100cxy.com/%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_20190105172738.png)

- 配置url 

![微信截图_20190105172823](http://md.100cxy.com/%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_20190105172823.png)

- 浏览器效果 

![微信截图_20190105172932](http://md.100cxy.com/%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_20190105172932.png)

- 使用postman伪造请求(post)

![微信截图_20190105173320](http://md.100cxy.com/%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_20190105173320.png)

![微信截图_20190105173401](http://md.100cxy.com/%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_20190105173401.png)

![微信截图_20190105173438](http://md.100cxy.com/%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_20190105173438.png)

![微信截图_20190105173546](http://md.100cxy.com/%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_20190105173546.png)

## 4、列表生成式(伪代码) 
```python 
class Foo:
	pass
			
class Bar:
	pass
		
v = []
for i in [Foo,Bar]:
    # 在这里i后面跟了一个小括号,就相当于实例化了一个对象 
	obj = i()
	v.append(obj) # 最后v里面就装的一个个对象 
		
# 列表生成式 和上面一样  v就是一个对象的列表(就是Foo的对象和Bar的对象)		
v = [item() for item in [Foo,Bar]]
```
## 5、面向对象 
### 封装(主要体现在两个方面) 
- 对同一类方法封装到类中 
```python
# 伪代码
# 跟文件相关操作的类
class File:
	文件增删改查方法

# 跟数据库相关操作的类					
class DB:
	数据库的方法
```

- 将数据封装到对象中
```python
# 伪代码
class File:
	def __init__(self,a1,a2):
		self.a1 = a1 
		self.a2 = a2
	def get:...
	def delete:...
	def update:...
	def add:...
					
obj1 = File(123,666)
obj2 = File(456,999)
```
- 拓展 
```python
class Request(object):
    def __init__(self, obj):
        self.obj = obj

    @property
    def user(self):
        return self.obj.authticate()


class Auth(object):
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def authticate(self):
        return self.name



class APIView(object):
    def dispatch(self):
        self.f2()

    def f2(self):
        a = Auth('wwy', 18)
        b = Auth('goodboys', 18)
        req = Request(b)
        print(req.user)


obj = APIView()
obj.dispatch()
```
## 6、反射
### 6.1、什么是反射 
通过字符串映射object对象的方法或者属性
### 6.2、反射的方法 

#### getattr() 
- 函数用于返回一个对象属性值。

![微信截图_20190105184550](http://md.100cxy.com/%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_20190105184550.png)

#### hasattr() 
- 函数用于判断对象是否包含对应的属性。

![微信截图_20190105193149](http://md.100cxy.com/%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_20190105193149.png)

#### setattr()
- setattr() 函数对应函数 getattr()，用于设置属性值，该属性必须存在。

![微信截图_20190105200309](http://md.100cxy.com/%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_20190105200309.png)


#### delattr()
- delattr 函数用于删除属性。
```
delattr(x, 'foobar') 相等于 del x.foobar。
```
![微信截图_20190105201634](http://md.100cxy.com/%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_20190105201634.png)

![微信截图_20190105201722](http://md.100cxy.com/%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_20190105201722.png)

### 6.3、方法的简单介绍
```python
hasattr(obj,name_str): 判断objec是否有name_str这个方法或者属性
getattr(obj,name_str): 获取object对象中与name_str同名的方法或者函数
setattr(obj,name_str,value): 为object对象设置一个以name_str为名的value方法或者属性
delattr(obj,name_str): 删除object对象中的name_str方法或者属性
```
#### getattr
- 设置一个类 
```python
class User(object):
    def __init__(self, name):
        self.name = name

    def eat(self):
        print('{}:正在吃夜宵'.format(self.name))

    def run(self):
        print("{}:正在跑步".format(self.name))

#  场景: 当用户在操作时,面对用户不同的操作就需要调用不同的函数
#  如果用if,elif语句的话,会存在一个问题,当用户有500个不同的操作,
#  就需要写500次if,elif。这样就会出现代码重复率高,而且还不易维护
#  这时候反射就出现了,通过字符串映射对象或方法
```
![微信截图_20190105202743](http://md.100cxy.com/%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_20190105202743.png)

![微信截图_20190105202912](http://md.100cxy.com/%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_20190105202912.png)

#### setattr
![微信截图_20190105203621](http://md.100cxy.com/%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_20190105203621.png)

![微信截图_20190105204407](http://md.100cxy.com/%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_20190105204407.png)

#### delattr
![微信截图_20190105205117](http://md.100cxy.com/%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_20190105205117.png)

## 7、反射的实际应用场景
在我们做接口自动化的时候,需要通过不同的请求方式,调用不同的函数

![微信截图_20190105205631](http://md.100cxy.com/%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_20190105205631.png)

![微信截图_20190105210150](http://md.100cxy.com/%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_20190105210150.png)

![微信截图_20190105210409](http://md.100cxy.com/%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_20190105210409.png)

# Django视图-CBV基本的使用和源码执行流程
- FBV和CBV其实就是要么写函数要么写类,那么内部原理是怎么实现?
## FBV写法 
```python
def func_view(request):
    "Function views"
    if request.method == "GET":
        return HttpResponse("GET-请求")
    elif request.method == "POST":
        return HttpResponse('POST-请求')
    elif request.method == "PUT":
        return HttpResponse('PUT-请求')
    elif request.method == "DELETE":
        return HttpResponse('DELETE-请求')
    else:
        return HttpResponse("不支持的请求类型")
```
## CBV写法
```python
class MyClassView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse("GET-请求")

    def post(self, request, *args, **kwargs):
        return HttpResponse("POST-请求")

    def put(self, request, *args, **kwargs):
        return HttpResponse("PUT-请求")

    def delete(self, request, *args, **kwargs):
        return HttpResponse("DELETE-请求")
```

## 原理 

- FBV可以直接通过路由，调用到相应的视图函数,那么CBV呢?

![微信截图_20190107211036](http://md.100cxy.com/%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_20190107211036.png)


- 在我们的MyClassViewl里面没有as_view(),所以我们可以去父类找

![微信截图_20190107211509](http://md.100cxy.com/%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_20190107211509.png)

- 父类的as_view()方法

![微信截图_20190107211710](http://md.100cxy.com/%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_20190107211710.png)

- 在as_view()中也返回一个view

![微信截图_20190107212833](http://md.100cxy.com/%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_20190107212833.png)

- 分析as_view()当中的代码,调用了dispatch()方法

![微信截图_20190107213123](http://md.100cxy.com/%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_20190107213123.png)

- 在分析dispatch()方法前,我们先看看,当请求进来,通过URL先执行了as_view()函数,本质还是在执行内部的view()函数,而view()函数内部是执行了dispatch()方法  

![微信截图_20190107213809](http://md.100cxy.com/%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_20190107213809.png)

- 不管什么请求进来,都执行dispatch()

![微信截图_20190107213912](http://md.100cxy.com/%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_20190107213912.png)

- 由于我们MyClassView里面没有dispatch()方法,所以会调用父类的dispatch(),如果我们有,那么会调用我们自己写的dispatch()方法   

![微信截图_20190107214135](http://md.100cxy.com/%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_20190107214135.png)

- postman验证(http://127.0.0.1:8000/myclass_view/) 我们发现调用了我们自己写的dispatch()方法 

![微信截图_20190107214459](http://md.100cxy.com/%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_20190107214459.png)


- 我们可以不看父类如何实现,我们可以自己尝试的写一下

![微信截图_20190107214847](http://md.100cxy.com/%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_20190107214847.png)

- 通过postman验证,发现也完成了这个相同的功能

![微信截图_20190107215246](http://md.100cxy.com/%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_20190107215246.png)

- 修正错误 

![微信截图_20190107215130](http://md.100cxy.com/%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_20190107215130.png)

- postman验证效果

![微信截图_20190107215339](http://md.100cxy.com/%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_20190107215339.png)

- 观察父类的dispatch做什么?(其实本质就是基于反射实现)

![微信截图_20190107215905](http://md.100cxy.com/%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_20190107215905.png)

结论: CBV基于反射实现根据请求方式不同,执行不同方法 

原理总结:
路由url -- > view函数 --> dispatch方法(根据反射来执行:GET/POST/PUT/DELETE等等....)

## 拓展1 

- 调用父类的方法

![微信截图_20190107220506](http://md.100cxy.com/%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_20190107220506.png)

- 原理图 

![微信截图_20190107221520](http://md.100cxy.com/%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_20190107221520.png)

![微信截图_20190107221819](http://md.100cxy.com/%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_20190107221819.png)

## 拓展2 
- 比如有这样一个功能,我们还有一个CBV,或者有更多的CBV都做一个print('before...')操作或者print('after...')操作   

![微信截图_20190107222302](http://md.100cxy.com/%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_20190107222302.png)

- 改进

![微信截图_20190107223139](http://md.100cxy.com/%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_20190107223139.png)

- 验证 

![微信截图_20190107223328](http://md.100cxy.com/%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_20190107223328.png)

- postman验证

![微信截图_20190107223457](http://md.100cxy.com/%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_20190107223457.png)


## 拓展3-解决CSRF问题 

- FBV:去请求体或者Cookie中获取token 

![微信截图_20190107235219](http://md.100cxy.com/%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_20190107235219.png)

![微信截图_20190108001844](http://md.100cxy.com/%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_20190108001844.png)

说明: csrf_protect是对某个视图函数启用CSRF

- CBV 

![微信截图_20190108002139](http://md.100cxy.com/%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_20190108002139.png)

![微信截图_20190108002222](http://md.100cxy.com/%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_20190108002222.png)

![微信截图_20190108002538](http://md.100cxy.com/%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_20190108002538.png)


