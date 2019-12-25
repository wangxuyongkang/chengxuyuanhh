import copy
import six

from scrapy.http import Request, HtmlResponse
from scrapy.utils.spider import iterate_spider_output
from scrapy.spiders import Spider

def identity(x):
    return x


class Rule(object):

    def __init__(self, link_extractor, callback=None, cb_kwargs=None, follow=None, process_links=None, process_request=identity):
        self.link_extractor = link_extractor
        self.callback = callback
        self.cb_kwargs = cb_kwargs or {}
        self.process_links = process_links
        self.process_request = process_request
        if follow is None:
            #注意在设置Rule的follow时，如果不设置，
            #则根据是否设置了回调函数,如果存在回调函数
            #则默认为 False（不跟进），否则，反之。
            self.follow = False if callback else True
        else:
            self.follow = follow


class CrawlSpider(Spider):
    # 用来存放Rule对象,根据规则提取url链接,并且设置回调和是否跟进
    # rules存在多个规则时，假如同一个url链接符合多个 Rule规则，这时
    # 只遵循第一个Rule规则
    rules = ()

    def __init__(self, *a, **kw):
        super(CrawlSpider, self).__init__(*a, **kw)
        self._compile_rules()

    def parse(self, response):
        #parse 方法一定不要在外面重写
        return self._parse_response(response, self.parse_start_url, cb_kwargs={}, follow=True)

    def parse_start_url(self, response):
        #start_urls中的url请求的响应结果，会走这个回调
        return []

    def process_results(self, response, results):
        return results

    def _build_request(self, rule, link):
        #根据link对象，构建Request请求对象
        #请求成功之后，会走self._response_downloaded
        r = Request(url=link.url, callback=self._response_downloaded)
        r.meta.update(rule=rule, link_text=link.text)
        return r

    def _requests_to_follow(self, response):
        #判断是否是响应结果，只处理响应结果，如果不是Response，
        # 则返回
        if not isinstance(response, HtmlResponse):
            return
        seen = set()
        for n, rule in enumerate(self._rules):
            links = [lnk for lnk in rule.link_extractor.extract_links(response)
                     if lnk not in seen]
            if links and rule.process_links:
                links = rule.process_links(links)
            for link in links:
                seen.add(link)
                #根据link对象，调用_build_request，
                # 返回request对象
                r = self._build_request(n, link)
                yield rule.process_request(r)

    def _response_downloaded(self, response):
        #请求成功后，调用Rule规则中设置的回调函数
        rule = self._rules[response.meta['rule']]
        return self._parse_response(response, rule.callback, rule.cb_kwargs, rule.follow)

    def _parse_response(self, response, callback, cb_kwargs, follow=True):
        #callback是Rule规则的回调函数（提取到的url地址请求成功后的回调）
        if callback:
            cb_res = callback(response, **cb_kwargs) or ()
            cb_res = self.process_results(response, cb_res)
            for requests_or_item in iterate_spider_output(cb_res):
                yield requests_or_item

        if follow and self._follow_links:
            for request_or_item in self._requests_to_follow(response):
                yield request_or_item

    def _compile_rules(self):
        def get_method(method):
            if callable(method):
                return method
            elif isinstance(method, six.string_types):
                return getattr(self, method, None)

        self._rules = [copy.copy(r) for r in self.rules]
        for rule in self._rules:
            rule.callback = get_method(rule.callback)
            rule.process_links = get_method(rule.process_links)
            rule.process_request = get_method(rule.process_request)

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(CrawlSpider, cls).from_crawler(crawler, *args, **kwargs)
        spider._follow_links = crawler.settings.getbool(
            'CRAWLSPIDER_FOLLOW_LINKS', True)
        return spider

    def set_crawler(self, crawler):
        super(CrawlSpider, self).set_crawler(crawler)
        self._follow_links = crawler.settings.getbool('CRAWLSPIDER_FOLLOW_LINKS', True)
