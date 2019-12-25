import requests,re,json
from lxml.html import etree
from requests.exceptions import HTTPError,RequestException,Timeout,ConnectTimeout


#蘑菇街分析
# 主题市场分类url地址
#https://mce.mogucdn.com/jsonp/multiget/3?
# callback=jQuery21106706790358065093_1551943370439
# &pids=109499%2C109520%2C109731%2C109753%2C110549%2C109779
# %2C110548%2C110547%2C109757%2C109793%2C109795%2C
# 110563%2C110546%2C110544
# &appPlat=p&_=1551943370441

#https://mce.mogucdn.com/jsonp/multiget/3?callback=jQuery21106706790358065093_1551943370439&pids=109499%2C109520%2C109731%2C109753%2C110549%2C109779%2C110548%2C110547%2C109757%2C109793%2C109795%2C110563%2C110546%2C110544&appPlat=p&_=1551943370441

#109499%2C109520%2C109731%2C109753%2C110549%2C109779
# %2C110548%2C110547%2C109757%2C109793%2C109795%2C
# 110563%2C110546%2C110544


#家具商品分类的第一页url
# https://list.mogujie.com/search?
# callback=''
# &_version=8193&ratio=3%3A4&cKey=15&page=1&sort=pop
# &ad=0&fcid=51642&action=home



#https://list.mogujie.com/search?
# callback=''
# &_version=8193&ratio=3%3A4&cKey=15&page=1&sort=pop
# &ad=0&fcid=52805&action=home

#https://list.mogujie.com/book/home/51642?
# acm=3.mce.1_10_1hets.109793.0.azme8rk1hoqR1.pos_0-m_406156-sd_119


#https://list.mogujie.com/search?
# callback=jQuery2110023333688598202285_1551948475833
# &_version=8193&ratio=3%3A4&cKey=15&page=1&sort=pop
# &ad=0&fcid=52805&action=home
# &acm=3.mce.1_10_1hetu.109793.0.azme8rk1hoqR3.pos_1-m_406157-sd_119&_=1551948475834

#//list.mogujie.com/book/home/52805?acm=3.mce.1_10_1hetu.109793.0.azme8rk1hoqR3.pos_1-m_406157-sd_119



def mgjSpider():

    bigCategoryStr = getBigCategory()
    # print(bigCategoryStr)
    all_category = get_all_category(bigCategoryStr)
    print(all_category)

def getBigCategory():

    url = 'https://mce.mogucdn.com/jsonp/multiget/3?callback=''&pids=110119&appPlat=p&_=1551943370440'
    json_str = send_request(url).replace('(','').replace(')','')
    category_list = json.loads(json_str)['data']['110119']['list']
    category_ids = []

    for category in category_list:
        # print(category)
        category_ids.append(category['categoryPid'])

    # print(json_str)
    return '%2C'.join(category_ids)

def get_all_category(bigCategoryStr):
    """
    根据大分类的ID,获取主题商品小分的所有id
    :param bigCategoryStr:
    :return:
    """

    allCategoryUrl = "https://mce.mogucdn.com/jsonp/multiget/3?callback=''&pids=%s&appPlat=p&_=1551943370441" % bigCategoryStr
    # print(allCategoryUrl)
    response = send_request(allCategoryUrl)
    pattern = re.compile(r'.*?\((.*?)\)')
    json_str = re.findall(pattern,response)[0]
    allCategory = json.loads(json_str)['data']

    all_category = []
    for key,value in allCategory.items():
        for item in value['list']:
            # print(item['title'],item['link'])
            #//list.mogujie.com/book/home/51649?acm=3.mce.1_10_1hetw.109793.0.azme8rk1hoqR5.pos_2-m_406158-sd_119
            category_id = re.search('\d+',item['link']).group()
            all_category.append(category_id)

    return all_category








def send_request(url,headers={'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36'}):

    try:
        response = requests.get(url=url,headers=headers)
        if response.status_code == 200:
            return response.text
    except (HTTPError,RequestException,Timeout,ConnectTimeout) as err:
        print(err)
        return None

if __name__ == '__main__':
    mgjSpider()











