import requests

#文件上传
url = 'https://httpbin.org/post'

files = {
    'file':open('page.html','r')
}

headers = {
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36'
}

# files: (optional) Dictionary
response = requests.post(url=url,files=files,headers=headers)

if response.status_code == 200:
    print(response.text)
