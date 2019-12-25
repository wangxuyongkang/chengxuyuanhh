#豆瓣电影数据可视化
import requests
from lxml.html import etree
#Page页面、Bar柱状图
from pyecharts.charts import Page,Bar,Pie,Funnel,Line,WordCloud
#主题
from pyecharts.globals import ThemeType
from pyecharts import options as opts

##电影名称、发布日期、类型、地区、关注量
url = 'https://movie.douban.com/cinema/later/beijing/'
response = requests.get(
    url=url,
    headers={
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'
    }
)

#all_movie_info = [{'name': '疯狂一家秀', 'publishtime': '08月17日', 'type': '剧情 / 喜剧', 'area': '中国大陆', 'attentionnum': '22'}, {'name': '猎袭', 'publishtime': '08月22日', 'type': '动作 / 犯罪', 'area': '中国大陆', 'attentionnum': '93'}, {'name': '速度与激情：特别行动', 'publishtime': '08月23日', 'type': '动作 / 犯罪', 'area': '美国', 'attentionnum': '30620'}, {'name': '保持沉默', 'publishtime': '08月23日', 'type': '剧情 / 爱情 / 悬疑', 'area': '中国大陆', 'attentionnum': '22212'}, {'name': '昆虫总动员2——来自远方的后援军', 'publishtime': '08月23日', 'type': '动画', 'area': '法国', 'attentionnum': '3675'}, {'name': '侠路相逢', 'publishtime': '08月23日', 'type': '动作 / 犯罪 / 悬疑', 'area': '中国大陆', 'attentionnum': '2936'}, {'name': '呼伦贝尔城', 'publishtime': '08月23日', 'type': '剧情', 'area': '中国大陆', 'attentionnum': '180'}, {'name': '碧血丹砂', 'publishtime': '08月23日', 'type': '爱情 / 奇幻 / 武侠', 'area': '中国大陆', 'attentionnum': '135'}, {'name': '到你身边', 'publishtime': '08月23日', 'type': '剧情', 'area': '中国大陆', 'attentionnum': '68'}, {'name': '格桑花之爱在前行', 'publishtime': '08月23日', 'type': '剧情 / 喜剧', 'area': '中国大陆', 'attentionnum': '36'}, {'name': '风从塬上来', 'publishtime': '08月23日', 'type': '爱情 / 西部', 'area': '中国大陆', 'attentionnum': '18'}, {'name': '秘密菜园', 'publishtime': '08月23日', 'type': '剧情', 'area': '中国大陆', 'attentionnum': '4'}, {'name': '骡子', 'publishtime': '08月26日', 'type': '剧情 / 犯罪 / 悬疑', 'area': '美国', 'attentionnum': '52918'}, {'name': '雷雨', 'publishtime': '08月27日', 'type': '剧情 / 戏曲', 'area': '中国大陆', 'attentionnum': '323'}, {'name': '毕业的我们', 'publishtime': '08月27日', 'type': '剧情', 'area': '中国大陆', 'attentionnum': '39'}, {'name': '一路爱情', 'publishtime': '08月28日', 'type': '喜剧 / 爱情', 'area': '中国大陆', 'attentionnum': '6'}, {'name': '禁锢之地', 'publishtime': '08月30日', 'type': '犯罪 / 悬疑', 'area': '中国大陆', 'attentionnum': '10930'}, {'name': '共同命运', 'publishtime': '08月30日', 'type': '剧情 / 纪录片', 'area': '中国大陆', 'attentionnum': '10569'}, {'name': '铤而走险', 'publishtime': '08月30日', 'type': '剧情 / 犯罪', 'area': '中国大陆', 'attentionnum': '7947'}, {'name': '深夜食堂', 'publishtime': '08月30日', 'type': '剧情', 'area': '中国大陆', 'attentionnum': '7362'}, {'name': '郊区的鸟', 'publishtime': '08月30日', 'type': '剧情', 'area': '中国大陆', 'attentionnum': '6172'}, {'name': '死寂逃亡', 'publishtime': '08月30日', 'type': '恐怖', 'area': '德国', 'attentionnum': '4327'}, {'name': '女王的柯基', 'publishtime': '08月30日', 'type': '喜剧 / 动画', 'area': '比利时', 'attentionnum': '2652'}, {'name': '傻儿夫妻小神郎', 'publishtime': '08月30日', 'type': '喜剧 / 爱情', 'area': '中国大陆', 'attentionnum': '95'}, {'name': '血溅鸳鸯楼', 'publishtime': '08月30日', 'type': '动作 / 武侠', 'area': '中国大陆', 'attentionnum': '39'}, {'name': '北京屋檐下', 'publishtime': '08月30日', 'type': '剧情 / 家庭', 'area': '中国大陆', 'attentionnum': '13'}, {'name': '踢球吧孩子', 'publishtime': '08月30日', 'type': '纪录片', 'area': '中国大陆', 'attentionnum': '10'}, {'name': '飞行员呆呆鸟', 'publishtime': '08月30日', 'type': '喜剧 / 爱情', 'area': '中国大陆', 'attentionnum': '1'}]
all_movie_info = []
if response.status_code == 200:
    print('请求成功')
    etree_html = etree.HTML(response.text)
    #提取电影信息
    movie_divs = etree_html.xpath('//div[@id="showing-soon"]/div')
    for div in movie_divs:
        movie_info = {}
        #电影名称
        movie_info['name'] = div.xpath('.//h3/a/text()')[0]
        #发布日期
        movie_info['publishtime'] = div.xpath('.//ul/li[1]/text()')[0]
        #类型
        movie_info['type'] = div.xpath('.//ul/li[2]/text()')[0]
        #地区
        movie_info['area'] = div.xpath('.//ul/li[3]/text()')[0]
        #关注量
        movie_info['attentionnum'] = div.xpath('.//ul/li[4]/span/text()')[0].replace('人想看','')
        all_movie_info.append(movie_info)

print(all_movie_info)


##实例化一个page对象，存放图表
page = Page()

###根据电影名称和关注量绘制柱状图
bar = Bar(
    init_opts=opts.InitOpts(theme=ThemeType.DARK)
)
#以关注量作为x轴
attention_nums = [info['attentionnum'] for info in all_movie_info]
#以电影名称作为y轴
names = [info['name'] for info in all_movie_info]

#添加x轴
bar.add_xaxis(names)
#添加y轴
bar.add_yaxis('未上映电影关注排行榜',attention_nums)

#反转
bar.reversal_axis()
#添加反转
bar.set_series_opts(
    label_opts=opts.LabelOpts(
        # title='电影关注排行榜',
        position='right'  ##横向
    )
)

##添加柱状图的标题
bar.set_global_opts(
    #设置柱状图的标题
    title_opts=opts.TitleOpts(
        title='电影关注排行榜'
    ),
    yaxis_opts=opts.AxisOpts(name='电影名称'),
    xaxis_opts=opts.AxisOpts(name='关注量')
)
page.add(bar)

#根据分类频次,画出饼状图
all_types = [info['type'] for info in all_movie_info]
types_info = {}
# {'剧情':1}
for type in all_types:
    result = type.split(' / ')
    for sub_type in result:
        if sub_type not in types_info:
            types_info[sub_type] = 1
        else:
            types_info[sub_type] += 1
print(types_info)

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
        (
            list(types_info.keys()),
            list(types_info.values()),
        )
    ],
    #设置饼图所在的未知
    center=['60%','50%'],
    #设置半径
    radius=["40%", "75%"],
)
#设置饼图文本展示格式
pie.set_series_opts(
    label_opts=opts.LabelOpts(
        formatter="{b}: {c}")
)
#添加标题
pie.set_global_opts(
    title_opts=opts.TitleOpts(
        title='上映类型占比',
    ),
    legend_opts=opts.LegendOpts
    (
        orient="vertical",
        pos_top="15%",
        pos_left="2%"
    ),
)
#将饼图添加至html模版页面
page.add(pie)


####漏斗图,根据电影发布日期，统计电影发布量
# {'08月17日':3}
data_times = {}
for info in all_movie_info:
    if info['publishtime'] not in data_times:
        data_times[info['publishtime']] = 1
    else:
        data_times[info['publishtime']] += 1

print(data_times)
#制作漏斗图
funnel = Funnel(
    init_opts=opts.InitOpts(
        theme=ThemeType.DARK
    )
)
funnel.add(
    "电影发布数",
    [list(z) for z in zip
    (
        list(data_times.keys()),
        list(data_times.values())
    )],
    sort_="ascending",
)
funnel.set_global_opts(
    title_opts=opts.TitleOpts(
        title='上映日期占比漏斗图'
    )
)
page.add(funnel)


###折线图(电影发布日期和发布电影数量折线图)
line = Line(
    init_opts=opts.InitOpts(
        theme=ThemeType.DARK
    )
)
#添加x轴坐标(发布日期)
line.add_xaxis(list(data_times.keys()))
#添加y轴（电影发布数量）
line.add_yaxis('发布电影数量',
               list(data_times.values()),
               is_smooth=True,#设置折线图为曲线图
               )

#添加标题
line.set_global_opts(
    title_opts=opts.TitleOpts(
        title='上映日期折线图'
    )
)
page.add(line)

####词云图
words = []
# {'剧情':3,'动作':2}
for key,value in types_info.items():
    data = (key,value)
    words.append(data)

print(words)

wordcolud = WordCloud(
    init_opts=opts.InitOpts(
        theme=ThemeType.DARK
    )
)
wordcolud.add(
    "词频数",
    words,
    word_size_range=[15,150]
)
wordcolud.set_global_opts(
    title_opts=opts.TitleOpts(
        title='电影分类词云图'
    )
)

page.add(wordcolud)

# bar.render()
page.render()
















