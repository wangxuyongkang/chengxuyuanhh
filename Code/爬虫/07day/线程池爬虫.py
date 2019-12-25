from concurrent.futures import ThreadPoolExecutor
import requests
from requests import exceptions
from lxml import etree

def crawlPageDate(url,**kwargs):
    print(url,kwargs)

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36'
    }
    try:
        response = requests.get(url=url, headers=headers)
        if response.status_code == 200:
            html = response.text
            #获取数据后进行数据解析
            return html,200
    except exceptions.HTTPError as err:
        print(err)
    except exceptions.ConnectTimeout as err:
        print(err)
    except exceptions.RequestException as err:
        print(err)

    return None,404

def done(futures):
    # print('11111')
    # print(futures.result())

    html,status = futures.result()
    print(status)
    if html:
        # 解析数据(实例化一个xpath的解析对象)
        x_html = etree.HTML(html)
        # 获取菜谱列表
        caipu_list = x_html.xpath('//div[@class="listtyle1"]')

        for caipu_div in caipu_list:
            item = {}
            # 封面图片
            item['coverImage'] = caipu_div.xpath('.//img[@class="img"]/@src')[0]
            # 类型
            item['type'] = caipu_div.xpath('.//strong[@class="gx"]/span/text()')
            if len(item['type']) > 0:
                item['type'] = item['type'][0]
            else:
                item['type'] = '暂无'
            # 标题
            item['title'] = caipu_div.xpath('.//div[@class="c1"]/strong/text()')[0]
            print(item)

if __name__ == '__main__':

    #创建一个线程池
    pool = ThreadPoolExecutor(max_workers=8)

    for page in range(1,57):
        #往线程池中提交任务
        """
        fn(要执行的任务), *args(要传递的参数), **kwargs（要传递的参数）
        """
        url = 'https://www.meishij.net/chufang/diy/jiangchangcaipu/?&page='+str(page)

        result = pool.submit(crawlPageDate,url,name='1808')
        #给线程添加后调方法(add_done_callback添加的是方法名)
        result.add_done_callback(done)


