from selenium import webdriver
import time

class DouyuSpider(object):

    def __init__(self):
        #创建浏览器驱动
        self.brower = webdriver.Chrome(
            executable_path='/Users/ljh/Desktop/1808爬虫/chromedriver'
        )
        #使用get方法打开页面
        self.brower.get('https://www.douyu.com/directory/all')

    def get_live_data(self):

        #将页面滚动到最底部
        self.brower.execute_script('window.scrollTo(0,document.body.scrollHeight)')
        #从页面源码中获取数据
        html_data = self.brower.page_source
        #可以使用xpath解析数据
        # 。。。。
        #方式二
        live_lis = self.brower.find_elements_by_xpath('//ul[@class="layout-Cover-list"]/li')

        for live_li in live_lis:
            live_dict= {}
            #获取封面图
            live_dict['coverImage'] = live_li.find_element_by_xpath('.//img[@class="DyImg-content is-normal "]').get_attribute('src')
            #标题
            live_dict['title'] = live_li.find_element_by_xpath('.//h3[@class="DyListCover-intro"]').text
            #主播名
            live_dict['name'] = live_li.find_element_by_xpath('.//h2[@class="DyListCover-user"]').text
            #关注量
            live_dict['attentionNum'] = live_li.find_element_by_xpath('.//span[@class="DyListCover-hot"]').text
            #type类型
            live_dict['type'] = live_li.find_element_by_xpath('.//span[@class="DyListCover-zone"]').text

            print(live_dict)

        #模拟点击下一页
        #dy-Pagination-next
        #dy-Pagination-item-custom
        #dy-Pagination-item-custom
        #dy-Pagination-disabled dy-Pagination-next
        next_element = self.brower.find_element_by_xpath('//li[@class=" dy-Pagination-next"]')

        if next_element:
            print('有下一页')
            self.brower.find_element_by_xpath('//li[@class=" dy-Pagination-next"]/span').click()
            time.sleep(1)
            self.get_live_data()
        else:
            print('页面加载完毕')





if __name__ == '__main__':

    spider = DouyuSpider()
    spider.get_live_data()


