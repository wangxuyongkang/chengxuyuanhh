from urllib import request,parse
import json
import ssl

url = 'https://www.lagou.com/jobs/positionAjax.json?needAddtionalResult=false'

form_data ={
    'first': 'false',
    'pn': 2,
    'kd': '后端',
}

#post请求参数
b_form_data = parse.urlencode(form_data).encode('utf-8')

#构建一个请求头
req_header = {
    'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
    'Referer':'https://www.lagou.com/jobs/list_%E5%90%8E%E7%AB%AF?labelWords=&fromSearch=true&suginput=',
    'Cookie':'_ga=GA1.2.1244414703.1536362405; user_trace_token=20180908072005-8d8053cb-b2f4-11e8-8c9a-525400f775ce; LGUID=20180908072005-8d805758-b2f4-11e8-8c9a-525400f775ce; _gid=GA1.2.1265023130.1548078142; index_location_city=%E5%85%A8%E5%9B%BD; JSESSIONID=ABAAABAAAFCAAEGED66389BF1AD59E5BEF411743E9DBC14; sajssdk_2015_cross_new_user=1; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22168737ecf6855-03961ed1f25493-3c720356-1228800-168737ecf692a%22%2C%22%24device_id%22%3A%22168737ecf6855-03961ed1f25493-3c720356-1228800-168737ecf692a%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E8%87%AA%E7%84%B6%E6%90%9C%E7%B4%A2%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22https%3A%2F%2Fwww.baidu.com%2Flink%22%2C%22%24latest_referrer_host%22%3A%22www.baidu.com%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC%22%7D%7D; _gat=1; PRE_UTM=; LGSID=20190122134308-98b10703-1e08-11e9-8e55-525400f775ce; PRE_HOST=www.baidu.com; PRE_SITE=https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3DSMM7yKs4y61uTPU61Fm4A3LtI1FlJ33DmDd_ZgFFCzu%26wd%3D%26eqid%3Dcc6f2ca800025abe000000025c4686bc; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2F; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1548125917,1548125926,1548125931,1548135788; TG-TRACK-CODE=index_search; SEARCH_ID=85be67377d2842c1975519d7f81c4d46; LGRID=20190122134319-9f46c74e-1e08-11e9-b735-5254005c3644; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1548135800'}

#实例化一个request对像
req = request.Request(url,headers=req_header,data=b_form_data)

#如果出现了ssl.CertificateError:......
#context:(ssl._create_unverified_context)
context = ssl._create_unverified_context()
#发起请求
response = request.urlopen(req,context=context)

# print(response.read().decode('utf-8'))

result_data = json.loads(response.read().decode('utf-8'))

positiones = result_data['content']['positionResult']['result']

print(positiones)

for position in positiones:
    jobInfo = {}
    #职位名称
    jobInfo['title'] = position['positionName']
    #职位所在地区
    jobInfo['district'] = position['district']
    #发布时间
    jobInfo['publishTime'] = position['formatCreateTime']
    #薪资
    jobInfo['salary'] = position['salary']
    #公司名称
    jobInfo['companyName'] = position['companyFullName']

    print(jobInfo)

    with open('lagou.json','a+') as file:
        data = json.dumps(jobInfo,ensure_ascii=False)
        file.write(data + '\n')