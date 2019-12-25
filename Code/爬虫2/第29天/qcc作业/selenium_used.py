# pip3 install selenium
from selenium import webdriver
import requests
from YDM import get_code_result

##Phontomjs无头浏览器
# phontomjs_driver = webdriver.PhantomJS(
#     executable_path='/Users/ljh/Desktop/driver/phantomjs'
# )

###火狐浏览器
# huohu_driver = webdriver.Firefox(
#     executable_path='/Users/ljh/Desktop/driver/geckodriver'
# )


##谷歌浏览器
gugo_driver = webdriver.Chrome(
    executable_path='/Users/ljh/Desktop/driver/chromedriver'
)

# url = 'https://www.baidu.com/'
# gugo_driver.get(url)
# #
# gugo_driver.save_screenshot('baidu.png')


#模拟登录云打码
gugo_driver.get('http://www.yundama.com/')

gugo_driver.implicitly_wait(5)

#输入账户名
gugo_driver.find_element_by_id('username').send_keys('wsygfsj')
#输入密码
gugo_driver.find_element_by_id('password').send_keys('123123')

###获取验证码图片的url地址
image_url = gugo_driver.find_element_by_id('verifyImg').get_attribute('src')
print(image_url)
headers = {
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',
}

cookies = {cookie['name']:cookie['value'] for cookie in gugo_driver.get_cookies()}
print(cookies)
response = requests.get(url=image_url,headers=headers,cookies=cookies)

"""
session=
0LD9rYrgqk7PqNbAMNS9bsYHdgfyqzHpVCohPzm9SiREcxoZpmupJpdgH8uSJ9eRmFLMAfHi%2F5SeVb%2FOYXzQNc4C%2BpBHFgYKc8ReVoDYem9zJpuMBHpx9VWeBJC85rvRPXqDBCepWKClnOzox4NWJ12OYG%2BqtsL4D1h5EbEEC%2BEeyKa1gDFtdw5XzmLEY1wYFbbcGWNfTbhBEgXRmpVaVxfKzuaNbUxxgF2gYU27IdEK7pGTcoJvuxdBnb1SabRKJq4Ylc%2F6XPMW6zHKBIYvuG3CfQxuM6ZD%2FuoI9AB9oWuDRLCRWW4NfZ1ExTnggmFqv3oNoQs2Qeri3d%2BPegJqhrsoeYOoi8Oxfb2aj5mXzWAafV41r34bE0vjL0bqXZLkAEumdEQLm3jKemH9CcYZFR94NPw3QXzvilsvd0I%2B4tLhlw9ngctfPWdyFO%2B4%2BqmaZUV%2BdATxZBcyHZwvEhWLJA%3D%3D; expires=Wed, 07-Aug-2019 04:39:46 GMT; path=/, session=bO9yU0RfBtgKNyBJHLzIs0tBcnRbn4QOXNb7hS2lckxwaXiZprKRQ%2FfviCNp1cvPBR%2Budqn%2B42Q6YTSbbyW1n515eWOqnScDJMUs6Qc4O%2FHWcgeeMpi0F2kOvD2N2GHftpNuRDwrlu5JzooQwsUmF0f%2Fsx6GKCMhSbO7IezoljZH%2F5cO%2FAHaxh8N0PjZDWl9VMfvX%2BrPobLFbQDTsxaXIiT3Mh71BU7AinR7nESG1W%2BE3%2BJu1xEx7fy2ZRXYczfzTnlIgJOjAsd5VrK1WtknjFR7ONO4ZKJzXvIK1ihnafBAiYKqLpq%2FDmuG6Hn0Fxazwunuy6jMzVzfuolWTjr41hh6fnSmHD5HmNnQ3WJINPGsYmp2WFtg%2BSNSO9zy5F6%2B%2BtnHgBOJ7Abwjp0nj%2BaoHoK1D1umQ2hjemncfqtxZ0N5MYQETP33oPp%2FBaQ1Ta%2B%2Ful1UI2zbcwCVMhTnPgT3nhPLpKv%2BZzpl6rH8FpLg8SOURISn%2BcuHHIXFp4wb%2F6WE; expires=Wed, 07-Aug-2019 04:39:46 GMT; path=/

"""


#识别图片
with open('captcha.jpg','wb') as file:
    file.write(response.content)

result = get_code_result(filename='captcha.jpg',codetype=3005)
print('验证码识别结果:',result)
#获取的session信息，更新本地的cookies
print('替换session前',{cookie['name']:cookie['value'] for cookie in gugo_driver.get_cookies()})
session = response.headers['Set-Cookie'].split('; ')[0].split('=')[1]

#{'name' : 'foo', 'value' : 'bar'}
gugo_driver.add_cookie({'name':'session','value':session})
print('替换session后',{cookie['name']:cookie['value'] for cookie in gugo_driver.get_cookies()})

gugo_driver.find_element_by_id('vcode').send_keys(result[1])

#点击登录按钮
gugo_driver.find_element_by_xpath('//input[@class="sub"]').click()

import time

time.sleep(1)

#获取登录后的cookies信息
login_cookies = {cookie['name']:cookie['value'] for cookie in gugo_driver.get_cookies()}
print('login_cookies',login_cookies)
gugo_driver.get('http://www.yundama.com/user')

with open('profile.html','w') as file:
    file.write(gugo_driver.page_source)

print(gugo_driver.current_url)