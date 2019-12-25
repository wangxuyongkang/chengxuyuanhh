# http：请求是没有状态的，是依靠session和cookies维持统一会话
# 什么是cookies?
# 为什么要获取cookies?
# 网站有一些比较重要的信息，只有登陆之后才能访问，登陆网网站
# 成功后，浏览器本地的cookies信息会发生变化（cookie保存着
# 登陆之后的用户信息）,所以要获取cookie,模拟登录用户访问网站

#如何获取cookie？
# 方式一： 在浏览器中登录后从请求头中获取
"""
Cookie: PHPSESSID=0cb6a306d9e9939ade709b4ceee1d273;
 SESSION_HASH=25462ac013a643ec176239644351398562cbae04;
  accessID=20190222105026894821;
   user_access=1

Cookie: _walkthrough-introduction=0;
PHPSESSID=a873e1f8ecbdd5dd83fac1586cf688a0;
main_search:196235559=%7C%7C%7C00;
jy_safe_tips_new=xingfu;
SESSION_HASH=25462ac013a643ec176239644351398562cbae04;
accessID=20190222105026894821;
user_access=1;
save_jy_login_name=18518753265;
stadate1=195235559; myloc=11%7C1101;
 myage=27;
 PROFILE=196235559%3A%25E6%259F%2590%25E6%259F%2590%25E7%2594%25B7%3Af%3Aimages1.jyimg.com%2Fw4%2Fglobal%2Fi%3A0%3A%3A1%3Azwzp_f.jpg%3A1%3A1%3A50%3A10%3A3; mysex=f; myuid=195235559; myincome=30; COMMON_HASH=7594ff36d50b0e564fe66ea49f82efe2; sl_jumper=%26cou%3D17%26omsg%3D0%26dia%3D0%26lst%3D2019-02-22; last_login_time=1550804081; upt=D1XVuL0%2ApHlCRoEDYJn2itEXldss0AWyWoRLjUJ58FaW3NMcAYNf8wXNFcp618JCU7QC34bdlel%2A%2AlO%2ATkhAcA..; user_attr=000000; pop_avatar=1; RAW_HASH=xHeW676HrmaJ5jlsQ8x4ydWusR9H37ahyZ3wMlb9WddzPjmRlqyXCZmRdBDjPMaUbL2mUr7oqFX3z7r0C3YRJosgiZbbrTwjIsg9MVd90HBCLFo.

"""

from urllib import request

# cookie = 'Cookie: _walkthrough-introduction=0; PHPSESSID=a873e1f8ecbdd5dd83fac1586cf688a0; main_search:196235559=%7C%7C%7C00; jy_safe_tips_new=xingfu; SESSION_HASH=25462ac013a643ec176239644351398562cbae04; accessID=20190222105026894821; user_access=1; save_jy_login_name=18518753265; stadate1=195235559; myloc=11%7C1101; myage=27; PROFILE=196235559%3A%25E6%259F%2590%25E6%259F%2590%25E7%2594%25B7%3Af%3Aimages1.jyimg.com%2Fw4%2Fglobal%2Fi%3A0%3A%3A1%3Azwzp_f.jpg%3A1%3A1%3A50%3A10%3A3; mysex=f; myuid=195235559; myincome=30; COMMON_HASH=7594ff36d50b0e564fe66ea49f82efe2; sl_jumper=%26cou%3D17%26omsg%3D0%26dia%3D0%26lst%3D2019-02-22; last_login_time=1550804081; upt=D1XVuL0%2ApHlCRoEDYJn2itEXldss0AWyWoRLjUJ58FaW3NMcAYNf8wXNFcp618JCU7QC34bdlel%2A%2AlO%2ATkhAcA..; user_attr=000000; pop_avatar=1; RAW_HASH=xHeW676HrmaJ5jlsQ8x4ydWusR9H37ahyZ3wMlb9WddzPjmRlqyXCZmRdBDjPMaUbL2mUr7oqFX3z7r0C3YRJosgiZbbrTwjIsg9MVd90HBCLFo.'

url = 'http://www.jiayuan.com/196235559'

# headers = {
#     'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36',
#     'Cookie':'SESSION_HASH=25462ac013a643ec176239644351398562cbae04; accessID=20190222105026894821; user_access=1; save_jy_login_name=18518753265; stadate1=195235559; myloc=11%7C1101; myage=27; PROFILE=196235559%3A%25E6%259F%2590%25E6%259F%2590%25E7%2594%25B7%3Af%3Aimages1.jyimg.com%2Fw4%2Fglobal%2Fi%3A0%3A%3A1%3Azwzp_f.jpg%3A1%3A1%3A50%3A10%3A3; mysex=f; myuid=195235559; myincome=30; COMMON_HASH=7594ff36d50b0e564fe66ea49f82efe2; sl_jumper=%26cou%3D17%26omsg%3D0%26dia%3D0%26lst%3D2019-02-22; last_login_time=1550804081; upt=D1XVuL0%2ApHlCRoEDYJn2itEXldss0AWyWoRLjUJ58FaW3NMcAYNf8wXNFcp618JCU7QC34bdlel%2A%2AlO%2ATkhAcA..; user_attr=000000; PHPSESSID=4d3f40c06b91fb2e9ac2637ca108b90e; main_search:196235559=%7C%7C%7C00; pop_avatar=1; RAW_HASH=xHeW676HrmaJ5jlsQ8x4ydWusR9H37ahyZ3wMlb9WddzPjmRlqyXCZmRdBDjPMaUbL2mUr7oqFX3z7r0C3YRJosgiZbbrTwjIsg9MVd90HBCLFo.; pop_time=1550804132105',
# }
#
# req = request.Request(url,headers=headers)
#
# response = request.urlopen(req)
# if response.status == 200:
#     with open('shijijiayuna.html','w') as file:
#         file.write(response.read().decode('utf-8'))


#方式二：模拟登录

#找到登录的url接口
#https://passport.jiayuan.com/dologin.php?pre_url=http://www.jiayuan.com/usercp
"""
name: 18518753265
password: ljh123456
remem_pass: on
_s_x_id: f9c074ee7cbd3950d1afee41a311ef2b
ljg_login: 1
m_p_l: 1
channel: 
position: 
"""

#自定义opener  保存和使用cookies信息
#cookiejar模块：主要作用是提供用于存储cookie的对象
#HTTPCookieProcessor处理器：主要作用是处理这些cookie对象，并构建handler对象。

"""
CookieJar：管理HTTP cookie值、存储HTTP请求生成的cookie、向传出的HTTP请求添加cookie的对象。整个cookie都存储在内存中，对CookieJar实例进行垃圾回收后cookie也将丢失。
MozillaCookieJar (filename,delayload=None,policy=None)：从FileCookieJar派生而来，创建与Mozilla浏览器 cookies.txt兼容的FileCookieJar实例。
"""

from urllib import request,parse
from http.cookiejar import CookieJar,MozillaCookieJar
import ssl

#管理HTTP cookie值、存储HTTP请求生成的cookie,将cookie信息
#保存在内存中
# cookjar = CookieJar()
filename = 'cookie.txt'
cookjar = MozillaCookieJar(filename=filename)

#创建handler处理器
handle = request.HTTPCookieProcessor(cookjar)

https_handler = request.HTTPSHandler(debuglevel=1,context=ssl._create_unverified_context())

#自定义 opener
opener = request.build_opener(handle,https_handler)

#发起请求
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36',
}

url = 'https://passport.jiayuan.com/dologin.php?pre_url=http://www.jiayuan.com/usercp'

form_data = {
    'name': '18518753265',
    'password': 'ljh123456',
    'remem_pass': 'on',
    '_s_x_id': 'f9c074ee7cbd3950d1afee41a311ef2b',
    'ljg_login': '1',
    'm_p_l': '1',
    'channel': '',
    'position': '',
}

data = parse.urlencode(form_data).encode('utf-8')
req = request.Request(url,data=data,headers=headers)
#发起请求，模拟登录
response = opener.open(req)
# * ignore_discard:  即保存需要被丢弃的cookie。
# * ignore_expires:  即过期的cookie也保存。
#调用save方法，保存cookies信息
cookjar.save(ignore_expires=True,ignore_discard=True)

if response.status == 200:
    cookie_str = ''
    for cookie in cookjar:
        print(cookie.name+'='+cookie.value)
        cookie_str = cookie_str+cookie.name+'='+cookie.value+'; '

    cookie_str = cookie_str[:-2]

    print(cookie_str)


    #个人主页
    url = 'http://www.jiayuan.com/196235559'

    req = request.Request(url,headers=headers)

    response = opener.open(req)

    if response.status == 200:
        with open('jiayuan.html','w') as file:
            file.write(response.read().decode('utf-8'))







