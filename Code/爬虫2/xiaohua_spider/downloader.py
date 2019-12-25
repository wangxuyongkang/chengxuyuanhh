import requests

def send_request(url,method="GET",parmas=None,data=None,headers=None):
    if not headers:
        headers = {
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3722.400 QQBrowser/10.5.3771.400',
        }
    if method == "GET":
        response = requests.get(url=url,params=parmas,headers=headers)
    elif method == "POST":
        response = requests.get(url=url,data=data,headers=headers)

    if response.status_code == 200:
        return response.text