from selenium import webdriver
import time
import requests
from io import BytesIO
from PIL import Image
from chaojiying import Chaojiying_Client
from selenium.webdriver import ActionChains

driver = webdriver.Chrome(executable_path='/Users/ljh/Desktop/1808爬虫/chromedriver')

driver.get('https://passport.douyu.com/member/login?lang=cn&type=login&client_id=1')


driver.find_element_by_xpath('//span[@class="scancide-to js-to-link js-need-param fr"]').click()

time.sleep(2)

driver.find_element_by_name('phoneNum').send_keys('18518753265')

driver.find_element_by_name('password').send_keys('ljh12345678')

time.sleep(1)

driver.find_element_by_xpath('//input[@class="loginbox-sbt btn-sub"]').click()

time.sleep(4)

imgae_element_div = driver.find_element_by_xpath('//div[@class="geetest_widget geetest_medium_fontsize"]')

location = imgae_element_div.location
size = imgae_element_div.size
print(location)
print(size)

top,bottom,left,right = location['y']+2,location['y']+size['height']-42,location['x']-size['width']-2,location['x']-4

print(top,bottom,left,right)

screen_image = driver.get_screenshot_as_png()

screen_image = Image.open(BytesIO(screen_image))

captcha = screen_image.crop((left,top,right,bottom))

captcha.save('image.png')

chaojiying = Chaojiying_Client('18518753265', 'ljh12345678', '898122')
im = open('image.png', 'rb').read()
result = chaojiying.PostPic(im, 9004)
print(result)

pic_str = result['pic_str'].split("|")
pic_id = result['pic_id']
locations = [[location for location in pic_location.split(",")] for pic_location in pic_str]
print(locations)

for location in locations:
    ActionChains(driver).move_to_element_with_offset(imgae_element_div,int(location[0]),int(location[1])).click().perform()
    time.sleep(1)

driver.find_element_by_xpath('//div[@class="geetest_commit_tip"]').click()

time.sleep(4)

if driver.find_element_by_xpath('//div[@class="geetest_widget geetest_medium_fontsize"]'):
    print('登录失败')
    result = chaojiying.ReportError(pic_id)
    print(result)

# print(driver.get_cookies())