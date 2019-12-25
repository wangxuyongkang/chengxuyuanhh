from concurrent.futures import ProcessPoolExecutor
import requests,re,json,os
from lxml import etree

def download_home_info(url):

    headers = {
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36',
    }
    response = requests.get(url=url,headers=headers)
    if response.status_code == 200:
        return response.text,response.url


def parse_download_data(futures):

    html,currentUrl = futures.result()
    # print(html)
    #https://bj.lianjia.com/ershoufang/pg1/
    pattern = re.compile('.*?com/(.*?)/.*?')
    type = re.findall(pattern,currentUrl)[0]

    print(type,os.getpid())
    #数据解析
    x_html = etree.HTML(html)
    #创建进程池继续添加下一页
    processPool = ProcessPoolExecutor(max_workers=4)
    if type == 'zufang':
        """租房"""
        # pass
        #content__pg
        totalPage = x_html.xpath('//div[@class="content__pg"]/@*')[3]
        curPage = x_html.xpath('//div[@class="content__pg"]/@*')[4]
        print(curPage,totalPage)
        # pattern = re.compile(r'.*?data-totalPage=(\d+).*?data-curPage=(\d+)',re.S)
        # result = re.findall(pattern,html)
        # print(result)
        # totalPage = int(result[0][0])
        # curPage = int(result[0][1])
        if int(curPage) < int(totalPage):
            print('正在发起请求')
            next_page = int(curPage)+1
            next_url = 'https://bj.lianjia.com/%s/pg%s/' % (type,str(next_page))
            print(next_url)
            # if next_url in crawlUrls:
            #     print('当前url已经爬取过了')
            # else:
            #     crawlUrls.append(next_url)
            result = processPool.submit(download_home_info, next_url)
            result.add_done_callback(parse_download_data)
    else:
        """二手房"""
        #下一页的url地址
        next_data = x_html.xpath('//div[@class="page-box house-lst-page-box"]/@page-data')[0]
        print(next_data)
        next_data = json.loads(next_data)
        totalPage = int(next_data['totalPage'])
        curPage = int(next_data['curPage'])
        if curPage < totalPage:
            print('正在发起请求')
            next_page = curPage+1
            next_url = 'https://bj.lianjia.com/%s/pg%s/' % (type,str(next_page))
        #     if next_url in crawlUrls:
        #         print('当前url已经爬取过了')
        #     else:
        #         crawlUrls.append(next_url)
            result = processPool.submit(download_home_info, next_url)
            result.add_done_callback(parse_download_data)




if __name__ == '__main__':

    #创建进程池
    #max_workers=设置进程池中最大的进程数
    processPool = ProcessPoolExecutor(max_workers=4)

    # #已爬取的url列表
    # crawlUrls = []

    star_urls = [
        'https://bj.lianjia.com/ershoufang/pg1/',
        'https://bj.lianjia.com/zufang/pg1/',
    ]
    for url in star_urls:
        # crawlUrls.append(url)
        result = processPool.submit(download_home_info,url)
        result.add_done_callback(parse_download_data)

    #cannot schedule new futures after shutdown
    #当调用shutdown()，就不能再添加新任务了
    # processPool.shutdown()


