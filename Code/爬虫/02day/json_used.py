import json
# json:可以将python数据类型和json字符串相互转换

#json.dumps():将python数据类型转换为json字符串
data_dict = {
    'name':'郑成峰',
    'age':'21',
    'gener':'男',
    'nums':[1,2,3,4,5,6,7]
}
json_str = json.dumps(data_dict,ensure_ascii=False)
print(json_str)
print(type(json_str))

#json.loads():将json字符串转换为python数据类型
loads_data = json.loads(json_str)
print(loads_data)
print(type(loads_data))

#json.dump():将python数据类型转换为json字符串,可以直接将转换的字符串保存本地
json.dump(data_dict,open('data.json','w'),ensure_ascii=False)

#json.load():将本地文件中的json字符串转换为python数据类型
load_data = json.load(open('data.json','r'))
print(load_data)
print(type(load_data))