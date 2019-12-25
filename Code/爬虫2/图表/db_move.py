import requests
from lxml.html import etree
#Page页面.Bar柱状图
from pyecharts.charts import Bar,Page,Pie,Funnel
#主题
from pyecharts.globals import ThemeType
from pyecharts import options as opts
###电影名称 发布日期 类型 地区 关注量
url = 'https://movie.douban.com/cinema/later/beijing/'
headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3722.400 QQBrowser/10.5.3771.400'
}
all_move_info = []
response = requests.get(url=url,headers=headers)
if response.status_code == 200:
    text = response.text
    etree_html = etree.HTML(text)
    if len(etree_html) > 0:
        divs = etree_html.xpath('//div[@id="showing-soon"]/div')
        for div in divs:
            item_dict = {}
            item_dict['name'] = div.xpath('.//h3/a/text()')[0]
            item_dict['publishtime'] = div.xpath('.//ul/li[1]/text()')[0]
            item_dict['type'] = div.xpath('.//ul/li[2]/text()')[0]
            item_dict['area'] = div.xpath('.//ul/li[3]/text()')[0]
            item_dict['attentionum'] = div.xpath('.//ul/li[4]/span/text()')[0].replace('人想看','')
            all_move_info.append(item_dict)
        print(all_move_info)

#实例化一个page对象
page = Page()
###根据电影名称和关注量绘制柱状图
bar = Bar(
    #添加主题黑灰色 不添加默认白色
    init_opts=opts.InitOpts(theme=ThemeType.DARK)
)
#以关注量作为x轴
attention_nums = [info['attentionum'] for info in all_move_info]
#以电影名称作为y轴
names =[info['name'] for info in all_move_info]
#x轴
bar.add_xaxis(names)
#y轴
bar.add_yaxis('电影名称',attention_nums)
#反转
bar.reversal_axis()
bar.set_series_opts(
    label_opts=opts.LabelOpts(
        position='right',#横向
    )
)
bar.set_global_opts(
    #设置柱状图的标题
    title_opts=opts.TitleOpts(
        title='电影关注排行榜',

    )
)
#根据分类频次画出饼状图
all_type = [info['type']for info in all_move_info]
type_info = {}
# {'剧情':1}
for type in type_info:
    result = type.split('/')
    for sub_type in result:
        if sub_type not in type_info:
            type_info[sub_type] = 1
        else:
            type_info[sub_type] += 1
print(type_info)
#制作饼图设置主题色
pie = Pie(
    init_opts=opts.InitOpts(
        theme=ThemeType.DARK
    )
)
#添加词和词频数
pie.add(
    '分类统计',
    [list(z) for z in zip
    (list(type_info.keys()),
     list(type_info.values()),
    )],#设置饼状图所在的位置
    center=['50%','50%'],
    radius=["40%","75%"]
    )
pie.set_series_opts(
    label_opts=opts.LabelOpts(
        # title='上映类型比例'
        formatter="{b}:{c}"
    )
)
bar.set_global_opts(
    #设置柱状图的标题
    title_opts=opts.TitleOpts(
        title='上映类型比例',
    ),
    legend_opts=opts.LegendOpts(
        orient="vertical",
        pos_top="15%",
        pos_left="10%"
    ),
)
#将圆饼图添加到html页面中
page.add(pie)


###----------------###漏斗图
data_times = {}
for info in all_move_info:
    if info['publishtime'] not in data_times:
        data_times[info['publishtime']] = 1
    else:
        data_times[info['publishtime']] += 1
print(data_times)
funnel = Funnel(
    init_opts=opts.InitOpts(
        theme=ThemeType.DARK
    )
)
funnel.add("电影发布数",
           [list(z) for z in zip(
               list(data_times.keys()),
               list(data_times.values()),
           )]
           )
funnel.set_global_opts(
    title_opts=opts.TitleOpts(
        title='上映日期占比图'
    )
)

# bar.render()
page.add(bar)
page.render()
