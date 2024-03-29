#######re 模块
import re
'''
单字符匹配
. : 匹配除了换行之任意字符
\d: 匹配数字0-9  = > [0-9] => [^\D ]
\D: 匹配非数字之外的任意字符 =>[^\d]
\s: 匹配空白字符  空格 \n \r .....
\S: 匹配非空白字符 
\w: 匹配单词字符 [a-z][A-Z][0-9]
\W: 匹配非单词字符 [^\w]
^ : 匹配开头
$ : 匹配结尾



多字符匹配
* 匹配*的表达式任意次
+ 匹配+ 前的表达式至少1次
? 匹配 ?前的表达式0~1次



非贪婪匹配（尽可能少的匹配）
*?
+?
??
| 或
() 分租
r  原始字符
\ 转译符号

'''
#构建正则表达对象
re.compile()
re.match()#从字符串起始位置匹配(第一个字符开始),匹配到结果，立即返回，否者返回None
re.search()# 在整个字符串中匹配，匹配到结果，立即返回，否者返回None 单次匹配
re.findall()#匹配出字符串中所有符合字符串规则的正则表达式的结果，将匹配结果放入list中返回
re.finditer()#匹配出字符串中所有符合字符串规则的正则表达式的结果，将匹配结果放入可迭代对象中
re.split()# 根据正则表达式,分割字符串
re.sub()#根据正则表达式替换字符串
