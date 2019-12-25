#使用selenium进行模拟登录（）
#https://lol.qq.com/
from selenium import webdriver
import time
# 创建浏览器驱动
brower = webdriver.Chrome(
    executable_path='/Users/ljh/Desktop/1808爬虫/chromedriver'
)

brower.get(url='https://lol.qq.com/')

time.sleep(1)

#找到登录按钮并点击
brower.find_element_by_xpath('//div[@class="head-userinfo-brief"]').click()
time.sleep(1)
brower.find_element_by_xpath('//div[@class="head-userinfo-brief"]/p[@class="unlogin"]/a').click()

time.sleep(1)

#如果出现了iframe子页面，这是如果你要找的节点在自页面中
#就需要先切换到自页面，然后在查找节点
brower.switch_to_frame('loginIframe')

time.sleep(0.5)

brower.find_element_by_id('switcher_plogin').click()

# brower.implicitly_wait(5)

#找到账号输入框
brower.find_element_by_id('u').send_keys('')
#找到密码输入框
brower.find_element_by_id('p').send_keys('')

time.sleep(3)
#找到登录按钮点击
brower.find_element_by_id('login_button').click()

cookies = brower.get_cookies()

cookies_dict = {cookie['name']:cookie['value'] for cookie in cookies}

#获取登录后的cookies信息
print(cookies_dict)

import requests

# requests.get(url=url,cookies=cookies_dict)
