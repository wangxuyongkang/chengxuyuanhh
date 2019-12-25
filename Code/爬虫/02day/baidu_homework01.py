# 1.模拟搜索引擎搜索
# 2.根据搜索关键字获取每个关键字的前10页
from urllib import parse,request
import os,random
from fake_useragent import UserAgent
"""
第一页
https://www.baidu.com/s?wd=%E6%96%B0%E5%B9%B4%E5%BF%AB%E4%B9%90&pn=0
"""

# """
# https://www.baidu.com/s?wd=%E6%96%B0%E5%B9%B4%E5%BF%AB%E4%B9%90&pn=10
# """
# 
# """
# https://www.baidu.com/s?wd=%E6%96%B0%E5%B9%B4%E5%BF%AB%E4%B9%90&pn=20
# """


def baidu_spider():
    """
    输入搜索关键字
    :return: 
    """
    #马云 马天宇 周杰轮 成龙 霸王防脱 洗发水 双节棍 李嘉诚 郭富城 王思聪
    # keys = input('请输入10个搜索关键字空格分割:')
    # keys = keys.split(' ')
    # print(keys)
    keys = []
    while True:
        key = input('请输入搜索关键字:')
        pn = input('请关键字获取的页码:')
        data = {'wd': key, 'page': pn}
        keys.append(data)
        isend = input('(N表示停止输入):')
        if isend == 'N':
            break

    user_agents = [
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
        'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:64.0) Gecko/20100101 Firefox/64.0',
    ]
    ua = UserAgent()
    send_request(keys,user_agents,ua)

def send_request(keys,user_agents,ua):

    # for wd in keys:
    for data_dict in keys:
        # if os.path.exists(wd) == False:
        #     os.mkdir(wd)
        if os.path.exists(data_dict['wd']) == False:
            os.mkdir(data_dict['wd'])

        for page in range(1,int(data_dict['page'])+1):
            #https://www.baidu.com/s?wd=%E6%96%B0%E5%B9%B4%E5%BF%AB%E4%B9%90&pn=0
            parmas = {
                'wd':data_dict['wd'],
                'pn':(page-1)*10,
            }
            #将参数转为url编码格式
            str_parmas = parse.urlencode(parmas)
            full_url = 'https://www.baidu.com/s?'+str_parmas
            #设置请求头
            # req_headers = {
            #     'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
            # }
            #取出UA池中的useragent
            # req_headers = {
            #     'User-Agent': random.choice(user_agents),
            # }
            #使用三方随机获取ua
            req_headers = {
                'User-Agent': ua.random,
            }
            #创建一个request对象
            req = request.Request(url=full_url,headers=req_headers)
            #urlopen方法发起请求
            response = request.urlopen(req)
            print('正在发起请求', full_url)

            if response.status == 200:
                print('请求成功',response.url)
                # print('请求成功'+wd+str(page)+'页')
                print('请求成功' + data_dict['wd'] + str(page) + '页')
                # 马云1.html
                # filepath = wd+'/'+wd+str(page)+'.html'
                filepath = data_dict['wd'] + '/' + data_dict['wd'] + str(page) + '.html'
                html = response.read().decode('utf-8')
                write_html_to_file(filepath,html)

def write_html_to_file(path,html):
    with open(path,'w') as file:
        file.write(html)

if __name__ == '__main__':

    baidu_spider()