"""
需要pip3 install redis
"""

from redis import StrictRedis
from urllib.parse import quote


def set_task():
    sr = StrictRedis(host='39.105.214.53', port=6379, db=0)
    #起始urls，根据分类添加url地址
    start_urls = [
        'http://www.wanfangdata.com.cn/search/searchList.do?beetlansyId=aysnsearch&searchType=degree&pageSize=50&page=1&searchWord=%E6%B3%95%E5%BE%8B&order=correlation&showType=detail&isCheck=check&isHit=&isHitUnit=&firstAuthor=false&rangeParame=&navSearchType=degree',
        'http://www.wanfangdata.com.cn/search/searchList.do?beetlansyId=aysnsearch&searchType=degree&pageSize=50&page=1&searchWord=%E6%94%BF%E6%B2%BB&order=correlation&showType=detail&isCheck=check&isHit=&isHitUnit=&firstAuthor=false&rangeParame=&navSearchType=degree',
        'http://www.wanfangdata.com.cn/search/searchList.do?beetlansyId=aysnsearch&searchType=perio&pageSize=50&page=1&searchWord=%E6%94%BF%E6%B2%BB&order=correlation&showType=detail&isCheck=check&isHit=&isHitUnit=&firstAuthor=false&rangeParame=&navSearchType=perio',
        'http://www.wanfangdata.com.cn/search/searchList.do?beetlansyId=aysnsearch&searchType=perio&pageSize=50&page=1&searchWord=%E6%B3%95%E5%BE%8B&order=correlation&showType=detail&isCheck=check&isHit=&isHitUnit=&firstAuthor=false&rangeParame=&navSearchType=perio',
        'http://www.wanfangdata.com.cn/search/searchList.do?beetlansyId=aysnsearch&searchType=conference&pageSize=50&page=1&searchWord=%E6%B3%95%E5%BE%8B&order=correlation&showType=detail&isCheck=check&isHit=&isHitUnit=&firstAuthor=false&rangeParame=&navSearchType=conference',
        'http://www.wanfangdata.com.cn/search/searchList.do?beetlansyId=aysnsearch&searchType=conference&pageSize=50&page=1&searchWord=%E6%94%BF%E6%B2%BB&order=correlation&showType=detail&isCheck=check&isHit=&isHitUnit=&firstAuthor=false&rangeParame=&navSearchType=conference',
        'http://www.wanfangdata.com.cn/search/searchList.do?beetlansyId=aysnsearch&searchType=tech&pageSize=50&page=1&searchWord=%E6%B3%95%E5%BE%8B&order=correlation&showType=detail&isCheck=check&isHit=&isHitUnit=&firstAuthor=false&rangeParame=&navSearchType=tech',
        'http://www.wanfangdata.com.cn/search/searchList.do?beetlansyId=aysnsearch&searchType=tech&pageSize=50&page=1&searchWord=%E6%94%BF%E6%B2%BB&order=correlation&showType=detail&isCheck=check&isHit=&isHitUnit=&firstAuthor=false&rangeParame=&navSearchType=tech',
    ]

    #分类，根据分类和年限时间段添加url地址
    category = ['degree','conference','perio','tech']
    #年份(1990,2019)
    dataList = []
    for i in range(1990,2020):
        dataList.append(i)

    index = 0
    # 关键字
    searchWords = ['法律','政治']
    # (政治) 起始年:2010 结束年:2019
    search_words = []
    for i in dataList:
        index += 1
        for j in dataList[index:]:
            for word in searchWords:
                search_words.append('(%s) 起始年:%s 结束年:%s' % (word,i,j))

    for cate in category:
        for keyWord in reversed(search_words):
            full_url = 'http://www.wanfangdata.com.cn/search/searchList.do?beetlansyId=aysnsearch&searchType=%s&pageSize=50&page=1&searchWord=%s&order=correlation&showType=detail&isCheck=check&isHit=&isHitUnit=&firstAuthor=false&rangeParame=&navSearchType=%s' % (cate,quote(keyWord),cate)
            print(full_url)
            start_urls.append(full_url)


    #将目标url添加到redis数据库，注意wflunwen:start_urls，一定不要写错了
    for url in start_urls:
        print(url)
        sr.lpush('wflunwen:start_urls',url)


if __name__ == '__main__':

    set_task()

