
from selenium import webdriver
import queue
from selenium.common.exceptions import NoSuchElementException

class Douban_movie(object):

    def __init__(self):

        self.driver = webdriver.Chrome(
            executable_path='/Users/xykang/PycharmProjects/chromedriver'
        )
        self.queue = queue.Queue()

    def start_spider(self,key):

        print('正在获取新的关键字信息',key)

        self.driver.get('https://movie.douban.com/')

        #找到搜索框，输入关键字
        self.driver.find_element_by_id('inp-query').send_keys(key)
        #找到搜索按钮点击
        self.driver.find_element_by_xpath('//div[@class="inp-btn"]/input').click()

        #跳转到电影列表页后，获取列表页数据
        self.get_movie_list_data(key)

    def get_movie_list_data(self,key):

        self.driver.implicitly_wait(5)

        # with open('page.html','w') as file:
        #     file.write(self.driver.page_source)

        # 将页面滚动到底部（注意这里必须要将页面滚动到底部,不然会获取不到数据）
        self.driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')

        #解析当前页面的电影列表数据
        movie_list = self.driver.find_elements_by_xpath('//div[@id="root"]//div[@class="item-root"]')
        print(len(movie_list))
        for movie in movie_list[1:]:
            movie_dict = {}
            movie_dict['title'] = movie.find_element_by_xpath('.//a[@class="title-text"]').text
            movie_dict['cover_image'] = movie.find_element_by_xpath('.//a[@class="cover-link"]/img').get_attribute('src')
            try:
                movie_dict['start'] = movie.find_element_by_xpath('.//span[@class="rating_nums"]').text
            except NoSuchElementException as err:
                print(err)
                movie_dict['start'] = '暂无'
            movie_dict['comment'] = movie.find_element_by_xpath('.//span[@class="pl"]').text
            movie_dict['tags'] = movie.find_element_by_xpath('.//div[@class="meta abstract"]').text
            movie_dict['actors'] = movie.find_element_by_xpath('.//div[@class="meta abstract_2"]').text
            self.save_movie_data(movie_dict)

        from selenium.common import exceptions
        try:
            #获取下一页节点，点击获取下一页数据
            next_element = self.driver.find_element_by_xpath('//a[@class="next"]')
            # self.driver.find_element_by_link_text('后页>')
            #先确定是否存在下一页的标签
            if next_element:
                print('下一页',key)
                next_element.click()
                self.get_movie_list_data(key)
        except exceptions.NoSuchElementException as err:
            #当前关键字所有分页获取完毕,获取下一个关键字数据
            if not self.queue.empty():
                self.start_spider(self.queue.get())
            else:
                self.driver.quit()

    def save_movie_data(self,data):
        """
        存储获取的数据
        :param data:
        :return:
        """
        print(data)

if __name__ == '__main__':

    dbspider = Douban_movie()
    print('可以输入两个搜索关键字')
    for i in range(2):
        key = input('请输入第'+str(i)+'个关键字:')
        dbspider.queue.put(key)
    # dbspider.queue.put('成龙')
    # dbspider.queue.put('范冰冰')

    dbspider.start_spider(dbspider.queue.get())