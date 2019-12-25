# 1.分析网站，找到目标url
#https://maoyan.com/board/4?offset=0
#https://maoyan.com/board/4?offset=10
#https://maoyan.com/board/4?offset=20
#页面是静态页面
#确定目标数据：排名、封面、标题、主演、时间、评分

from urllib import request,error,parse
import re,ssl
import pymysql

def maoyan_sipder():
    start_url = 'https://maoyan.com/board/4?offset=0'
    start_request(start_url)

def start_request(url):
    #构建请求头
    headers = {
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36',
    }

    #构建一个request
    req = request.Request(url,headers=headers)
    #实例化context (ssl._create_unverified_context())
    context = ssl._create_unverified_context()
    #发起请求（urlopen）
    try:
        response = request.urlopen(req,context=context,timeout=10)
        if response.status == 200:
            print('请求成功')
            html_str = response.read().decode('utf-8')
            result = parse_data(html_str)
            if len(result) > 0:
                #存储数据
                save_data_to_db(result)

                #获取当前请求的url地址
                current_url = response.url
                #获取当前请求的偏移量
                #https://maoyan.com/board/4?offset=0
                pattern = re.compile('.*?offset=(\d+)')
                offset_result = re.findall(pattern,current_url)
                if offset_result:
                    offset = offset_result[0]
                    print('当前偏移量',offset)
                    next_offset = int(offset)+10
                    next_url = 'https://maoyan.com/board/4?offset='+str(next_offset)
                    print(next_url)
                    start_request(next_url)


                #可以获取到数据，继续发起下一页请求
                # pass
            else:
                import time
                time.sleep(5)
                #关闭数据库链接
                cursor.close()
                mysql_client.close()
                print('没有数据了')


    except error.HTTPError as err:
        print(err.code,err.reason)
    except error.URLError as err:
        print(err.reason)

def parse_data(html_str):
    """
    使用正则提取数据
    :param html_str:
    :return:
    """
    # print(html_str)
    # with open('maoyan.html','w') as file:
    #     file.write(html_str)

    pattern = re.compile(
        '<dd.*?<i.*?board-index.*?>(.*?)</i>.*?'+
        '<img.*?data-src="(.*?)".*?>.*?'+
        '<p.*?name.*?>.*?<a.*?>(.*?)</a>.*?'+
        '<p.*?star.*?>(.*?)</p>.*?'+
        '<p.*?releasetime.*?>(.*?)</p>.*?'+
        '<i.*?>(.*?)</i>.*?'+
        '<i.*?>(.*?)</i>',
        re.S
    )
    result = re.findall(pattern,html_str)

    return result
    # # print(result)

def save_data_to_db(result):
    for movieInfo in result:

        info = {}
        info['rank'] = int(movieInfo[0])
        info['coverImage'] = movieInfo[1]
        info['title'] = movieInfo[2]
        info['actor'] = movieInfo[3]
        info['publishTime'] = movieInfo[4]
        info['score'] = float(movieInfo[5]+movieInfo[6])

        insert_sql = """
        INSERT INTO maoyanmovie (%s)
        VALUES (%s)
        """ % (','.join(info.keys()),','.join(['%s']*len(info)))
        # ','.join(['%s','%s','%s']) ==> '%s,%s,%s'

        try:
            cursor.execute(insert_sql,list(info.values()))
            mysql_client.commit()
        except Exception as err:
            print(err)
            mysql_client.rollback()
            
        # insert_sql = """
        # INSERT INTO maoyanmovie(rank,coverImage,title,actor,publishTime,score)
        # VALUES (%s,%s,%s,%s,%s,%s)
        # """
        # try:
        #     cursor.execute(
        #         insert_sql,
        #         [
        #             int(movieInfo[0]),
        #             movieInfo[1],
        #             movieInfo[2],
        #             movieInfo[3].replace(' ','').replace('\n',''),
        #             movieInfo[4],
        #             float(movieInfo[5]+movieInfo[6])
        #         ]
        #     )
        #     mysql_client.commit()
        # except Exception as err:
        #     print(err)
        #     mysql_client.rollback()

if __name__ == '__main__':

    #创建数据库链接
    mysql_client = pymysql.Connect(
        'localhost','root','ljh1314',
        'maoyan',charset='utf8'
    )
    #创建游标
    cursor = mysql_client.cursor()

    maoyan_sipder()





