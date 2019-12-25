from __future__ import unicode_literals
import requests
import itchat
import time
import random
from threading import Timer
KEY = '69a172c6b97f4f2e9a715e93b37e6716'
is_statistics = False
l = ['你怎么点到这里来了啊！你点到鬼门关了还不快下线要不我都救不了你了，回去洗个澡烧柱香还能活三十年','你要和我说话？你真的要和我说话？你确定自己想说吗？你一定非说不可吗？那你说吧，这是自动回复。','你好，我是主人的美女秘书，有什么事就跟我说吧，等他回来我会转告他的。','我正在拉磨，没法招呼您，因为我们家毛驴去动物保护协会把我告了，说我剥夺它休产假的权利。','——说不在，就不在！你相不相信我都不在！']
#自动返回内容
def get_news():
    url = "http://open.iciba.com/dsapi"
    r = requests.get(url)
    contents = r.json()['content']
    translation = r.json()['translation']
    return contents, translation

#自动发信消息
def send_news():
    global is_statistics
    try:
        # 登陆你的微信账号，会弹出网页二维码，扫描即可
        itchat.auto_login(hotReload=True)
        if not is_statistics:
            statistics()
            is_statistics = False
        my_friend = itchat.search_friends(name=u'北财学生-徐永康')#获取为小源的好友
        # 获取对应名称的一串数字
        XiaoYuan = my_friend[0]["UserName"]
        # 发送消息
        itchat.send("欢迎来到智能小助手", toUserName=XiaoYuan)
        itchat.send("学AI 到北财软件工程学院", toUserName=XiaoYuan)
        itchat.run()
        
    except:
        message4 = "智能小助手今天不开心，不想回复"#出现异常

#自动回复
def auto_send(to_user):
    itchat.send("欢迎来到智能语音助手", toUserName=XiaoYuan)
    itchat.send("学AI 到北京软件工程学院", toUserName=XiaoYuan)



#自动回复
@itchat.msg_register(itchat.content.TEXT)
def tuling_reply(msg):
    itchat.send(get_response(msg), msg['FromUserName'])
    # itchat.send(random.choice(l),msg['FromUserName'])

#自动识别文字
def get_response(msg):
    apiUrl = 'http://www.tuling123.com/openapi/api'
    data = {
        'key'    : KEY,
        'info'   : msg['Text'],
        'userid' : 'wechat-robot',
    }
    try:
        r = requests.post(apiUrl, data=data).json()
        return r.get('text')
    except:
        return   

#统计好友男女比例
def statistics():
    friends = itchat.get_friends(update=True)[:]
    total = len(friends) - 1  
    man = women = other = 0  
    for friend in friends[0:] :  
        sex = friend["Sex"]  
        if sex == 1 :  
            man += 1  
        elif sex == 2 :  
            women += 1  
        else :  
            other += 1    
  
    print("男性好友：%.2f%%" % (float(man) / total * 100))  
    print("女性好友：%.2f%%" % (float(women) / total * 100))  
    print("其他：%.2f%%" % (float(other) / total * 100))  

def main():
    send_news()
    
#开始调用
if __name__ == '__main__':
    main()
