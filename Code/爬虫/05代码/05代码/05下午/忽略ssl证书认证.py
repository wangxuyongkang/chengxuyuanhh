import requests

url = 'https://www.baidu.com/'
headers = {
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36',
}

#如果出现了证书认证ssl ca证书错误
#verify：Defaults to ``True``，默认为true,表示进行证书认证
#如果出现了证书认证ssl ca证书错误修改verify为False，表示忽略证书认证
response = requests.get(url=url,headers=headers,verify=False)

if response.status_code == 200:
    print('请求成功')
    print(response.text)