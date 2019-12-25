from YDMHTTP3 import get_image_result
from selenium import webdriver
import time,requests
# result, cid = get_image_result('antispam_v2.jpeg',4005)
#
# print(result,cid)

brower = webdriver.Chrome(
    executable_path='/Users/ljh/Desktop/1808爬虫/chromedriver'
)

brower.get('http://login.jiayuan.com/')
time.sleep(1)

#找到账号输入框
brower.find_element_by_id('login_email').send_keys('18518753265')
#找到密码输入框
brower.find_element_by_id('login_password').send_keys('ljh123456')
#找到验证码图片
img_element = brower.find_element_by_id('validate_img')
#get_cookies()获取到cookies信息
cookies = brower.get_cookies()
cookies_dict = {cookie['name']:cookie['value'] for cookie in cookies}
if img_element:
    print('有验证码')
    imageUrl = img_element.get_attribute('src')
    #http://login.jiayuan.com/antispam_v2.php?
    # v=2&rn=0.9454763826063461
    # print(imageUrl)
    headers = {
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36',
    }

    response = requests.get(imageUrl,headers=headers,cookies=cookies_dict)

    if response.status_code == 200:
        with open('code.jpg','wb') as file:
            file.write(response.content)
#
#
    result,cid = get_image_result('code.jpg',4005)

    if result:
        brower.find_element_by_id('validate_code').send_keys(result)

        time.sleep(2)
        #点击登录按钮
        # brower.find_element_by_id('login_btn').click()
        brower.find_element_by_xpath('//form[@id="login"]').click()
        time.sleep(1)
        brower.find_element_by_xpath('//div[@class="btnsBox"]').click()
        time.sleep(2)
        brower.find_element_by_xpath('//a[@id="login_btn"]').click()
else:
    print('没有验证码')


# 注意：

# 1.验证码获取图片请求一次之后，这个图片地址得到的验证是固定的
# 这时直接把图片拿到，然后识别验证。就可以了

# 2.每一次请求验证码图片地址，验证码都在发生变化（url地址不变，
# 图片变化），这时一定要注意，再获取验证码的时候，一定要跟浏览器
# 中的cookies信息绑定





