# 什么叫selenium？
#  谷歌浏览器驱动
#  火狐的浏览器驱动
#  无头浏览器

# 安装：pip3 install selenium
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException,TimeoutException
import time
#创建浏览器驱动（火狐）
# brower = webdriver.Firefox(
#     executable_path='/Users/ljh/Desktop/1808爬虫/geckodriver'
# )

#创建浏览器驱动（无头浏览器phantomjs）
# warnings.warn('Selenium support for PhantomJS
# has been deprecated, please use headless '

# brower = webdriver.PhantomJS(
#     executable_path='/Users/ljh/Desktop/1808爬虫/phantomjs'
# )

#创建浏览器驱动（谷歌）
#设置无头浏览器
# opt = webdriver.ChromeOptions()
# opt.set_headless()
# brower = webdriver.Chrome(
#     executable_path='/Users/ljh/Desktop/1808爬虫/chromedriver'
#     ,options=opt
# )

brower = webdriver.Chrome(
    executable_path='/Users/ljh/Desktop/1808爬虫/chromedriver'
)

brower.set_page_load_timeout(10)

try:
    #使用get方法打开网站
    brower.get('https://www.baidu.com')
except TimeoutException as err:
    print('请求超时')

#保存页面截图
brower.save_screenshot('baidu.png')


#模拟用户点击和输入操作
# brower.find_element_by_id() 根据节点id查找
# brower.find_element_by_class_name() 根据节点class属性查找
# brower.find_element_by_css_selector() 根据css选择器查找
# brower.find_element_by_link_text() 根据节点的文本查找
# brower.find_element_by_xpath() 根据xpath语法选择器查找

brower.find_element_by_id('kw').send_keys('美女')
brower.find_element_by_id('su').click()

#清空关键字
brower.find_element_by_id('kw').clear()
brower.find_element_by_id('kw').send_keys('帅哥')
brower.find_element_by_id('su').click()


# time.sleep(2)
#设置等待
#
# 隐式等待是等待特定的时间，如果节点没有立即出现，
# 隐士等待将一段时间再进行查找 显式等待是指定一个
# 最长的等待时间,直到条件成立时继续执行。
# 如果在设定时间内没加载出来节点,则返回异常信息,
# 如果加载出来了则返回节点
# brower.implicitly_wait(10)

#显式等待
# 显式等待指定某个条件，然后设置最长等待时间。
# 如果在这个时间还没有找到元素，那么便会抛出异常了

#设置显示等待
#根据...找节点
from selenium.webdriver.common.by import By
# 设置WebDriverWait等待
from selenium.webdriver.support.ui import WebDriverWait
#expected_conditions负责添加条件
from selenium.webdriver.support import expected_conditions as EC
kw_element = WebDriverWait(brower,10).until(
    EC.presence_of_element_located((By.ID,'kw'))
)
time.sleep(2)

#获取节点的属性和文本
#get_attribute:获取节点的属性
searchText = brower.find_element_by_id('kw').get_attribute('value')
#text获取节点的文本
# text = brower.find_element_by_class_name('search_tool').text
text = brower.find_element_by_xpath('//div[@class="search_tool"]').text
print(searchText,text)
time.sleep(2)

#可以获取的信息
#获取浏览器渲染之后的页面源码
html = brower.page_source
#获取cookies信息
cookies = brower.get_cookies()
#获取当前请求的url地址
currentUrl = brower.current_url

#关于cookies的操作
#获取cookie中某一个cookie值
# brower.get_cookie(name='cookie名称')
# #添加cookies
# brower.add_cookie(cookie_dict={'cookie的name':'cookie的value'})
# #清空cookies
# brower.delete_all_cookies() #清空所有的cookies
# brower.delete_cookie() #根据cookie的name属性清空某一个cookie


#点击下一页按钮
#异常处理
try:
    brower.find_element_by_link_text('下一页>').click()
except NoSuchElementException as err:
    print('没有找到这个节点')

time.sleep(1)
#返回（后退）
brower.back()
time.sleep(1)
#前进
brower.forward()


#执行js代码打开新的窗口
js = 'window.open("http://www.baidu.com/")'
#execute_script执行js代码
# brower.execute_script(js)

#### 向下滚动到页面底部
brower.execute_script('window.scrollTo(0,document.body.scrollHeight)')

#close()关闭当前浏览器的窗口
# brower.close()
#关闭(退出浏览器)
# brower.quit()







