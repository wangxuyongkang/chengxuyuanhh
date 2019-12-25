# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class WanfangDegreeItem(scrapy.Item):
    """
    学位分类数据
    """
    #链接地址
    url = scrapy.Field()
    # title(中文标题)
    title = scrapy.Field()
    # content(摘要)
    content = scrapy.Field()
    # keywords(关键词)
    keywords = scrapy.Field()
    # authors(作者)
    authors = scrapy.Field()
    #学位授权单位
    degreeUnit = scrapy.Field()
    #授予学位
    awardedTheDegree = scrapy.Field()
    #学科专业
    professional = scrapy.Field()
    #导师姓名
    mentorName = scrapy.Field()
    #学位年度
    degreeInAnnual = scrapy.Field()
    #语种
    languages = scrapy.Field()
    #分类号
    classNumber = scrapy.Field()
    #在线出版日期
    publishTime = scrapy.Field()
    # 搜索关键字
    searchKey = scrapy.Field()
    # 分类的名称(标示)
    searchType = scrapy.Field()

    def get_sql_data(self,data):
        inserSel, insertData = insert_data_with_data(data,'degree')
        return inserSel, insertData


class WanfangPerioItem(scrapy.Item):
    """
    期刊分类数据
    """
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 链接地址
    url = scrapy.Field()
    #title(中文标题)
    title = scrapy.Field()
    #englishTitle(英文标题)
    englishTitle = scrapy.Field()
    #content(摘要)
    content = scrapy.Field()
    #doi
    doi = scrapy.Field()
    #keywords(关键词)
    keywords = scrapy.Field()
    #Keyword(英文关键词)
    englishKeyWords = scrapy.Field()
    #authors(作者)
    authors = scrapy.Field()
    # authors(作者英文)
    englishAuthors = scrapy.Field()
    #作者单位
    unit = scrapy.Field()
    #刊名
    journalName = scrapy.Field()
    #Journal
    journal = scrapy.Field()
    #（年，卷（期））
    yearsInfo = scrapy.Field()
    #所属期刊栏目
    journalSection = scrapy.Field()
    #分类号
    classNumber = scrapy.Field()
    #基金项目
    fundProgram = scrapy.Field()
    # 发布时间
    publishTime = scrapy.Field()
    #页数
    pages = scrapy.Field()
    #页码
    pageNumber = scrapy.Field()
    # 搜索关键字
    searchKey = scrapy.Field()
    # 分类的名称(标示)
    searchType = scrapy.Field()

    def get_sql_data(self,data):
        inserSel, insertData = insert_data_with_data(data,'perio')
        return inserSel, insertData


class WanfangConferenceItem(scrapy.Item):
    """
    会议分类数据
    """
    # 链接地址
    url = scrapy.Field()
    #title(中文标题)
    title = scrapy.Field()
    #content(摘要)
    content = scrapy.Field()
    #keywords(关键词)
    keywords = scrapy.Field()
    #authors(作者)
    authors = scrapy.Field()
    #作者单位
    unit = scrapy.Field()
    #母体文献
    literature = scrapy.Field()
    #会议名称
    meetingName = scrapy.Field()
    #会议时间
    meetingTime = scrapy.Field()
    #会议地点
    meetingAdress = scrapy.Field()
    #主办单位
    organizer = scrapy.Field()
    #语种
    languages = scrapy.Field()
    #分类号
    classNumber = scrapy.Field()
    #发布时间
    publishTime = scrapy.Field()
    #页码
    pageNumber = scrapy.Field()
    # 搜索关键字
    searchKey = scrapy.Field()
    # 分类的名称(标示)
    searchType = scrapy.Field()

    def get_sql_data(self,data):
        inserSel, insertData = insert_data_with_data(data,'conference')
        return inserSel, insertData


class WanfangTechItem(scrapy.Item):
    """
    科技报告分类数据
    """
    # 链接地址
    url = scrapy.Field()
    #title(中文标题)
    title = scrapy.Field()
    #englishTitle(英文标题)
    englishTitle = scrapy.Field()
    #content(摘要)
    content = scrapy.Field()
    #keywords(关键词)
    keywords = scrapy.Field()
    #authors(作者)
    authors = scrapy.Field()
    #作者单位
    unit = scrapy.Field()
    #报告类型
    reportType = scrapy.Field()
    #公开范围
    openRange = scrapy.Field()
    #全文页数
    pageNumber = scrapy.Field()
    #项目/课题名称
    projectName = scrapy.Field()
    #计划名称
    planName = scrapy.Field()
    #编制时间
    compileTime = scrapy.Field()
    #立项批准年
    approvalYear = scrapy.Field()
    #馆藏号
    collection = scrapy.Field()
    #搜索关键字
    searchKey = scrapy.Field()
    #分类的名称(标示)
    searchType = scrapy.Field()

    def get_sql_data(self,data):
        inserSel, insertData = insert_data_with_data(data,'tech')
        return inserSel, insertData


def insert_data_with_data(data,tableName):

    # inserSel = """
    # INSERT INTO %s (%s)
    # VALUES(%s)
    # """ % (tableName,','.join(data.keys()),','.join(['%s']*len(data)))

    inserSel = """
    REPLACE INTO %s (%s)
    VALUES(%s)
    """ % (tableName, ','.join(data.keys()), ','.join(['%s'] * len(data)))

    insertData = list(data.values())

    return inserSel,insertData






