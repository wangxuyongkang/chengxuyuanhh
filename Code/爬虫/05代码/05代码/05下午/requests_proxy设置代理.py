import requests

# url = 'https://www.baidu.com/'
url = 'https://httpbin.org/get'
headers = {
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36',
}
proxy = {
    'https': '60.190.250.120:8080',
    'http': '121.61.3.209:9999',
}

#param proxies: (optional) Dictionary
response = requests.get(url=url,headers=headers,proxies=proxy)

if response.status_code == 200:
    print('请求成功')
    print(response.text)
