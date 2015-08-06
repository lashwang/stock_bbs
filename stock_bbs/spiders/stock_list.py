# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider,Rule
from stock_bbs.parser.html_parser import *
from scrapy.linkextractors import LinkExtractor
from scrapy.http import Request
from stock_bbs.utils.utils import *
from scrapy.exceptions import CloseSpider
from scrapy.conf import settings


class StockSpider(CrawlSpider):
    name = "stock_list"
    MAX_INDEX_PAGE = int(settings['MAX_INDEX_PAGE'])

    allowed_domains = ["bbs.tianya.cn"]
    start_urls = (
        'http://bbs.tianya.cn/list-stocks-1.shtml',
    )

    '''
    Rule (LinkExtractor(allow=("post",),
        restrict_xpaths=('//div[@class="mt5"]//td/a',)),
        callback="parse_detail_page",follow=True),

    Rule (LinkExtractor(allow=("post",),
        restrict_xpaths=('//div[@id="bd"]/div[@class="clearfix"]/div/form/a[contains(@class,"next")]',)),
        callback="parse_detail_page",follow=True),
    '''

    def __init__(self, *a, **kw):
        self.PAGE = 0
        super(StockSpider, self).__init__(*a, **kw)

    rules = (
        # for page index next link
        Rule (LinkExtractor(allow=("nextid", ),
            restrict_xpaths=('//div[@class="links"]/a[@rel="nofollow"]',)),
            callback="parse_index_page", follow=True),


    )

    def parse_start_url(self, response):
        return self.parse_index_page(response)


    def parse_index_page(self,response):
        if self.PAGE > StockSpider.MAX_INDEX_PAGE:
            print 'page number limit exceeded:' + str(StockSpider.MAX_INDEX_PAGE)
            raise CloseSpider('page number limit exceeded:')
        self.PAGE += 1
        print 'parse_index_page,url:',response.url
        hxs = response.xpath(u'//div[@class="mt5"]')
        hxs = hxs.xpath(u'.//tr')
        for each in hxs:
            item = HtmlParser.parse_bbs_ticket(each,response)
            if not item:
                continue
            clickNumber = int(item['clickNumber'])
            if clickNumber < int(settings['CLICKNUMBER_THRESHOLD'])*10000:
                continue
            print item['url']
            request = Request(item['url'],callback=self.parse_detail_page)
            request.meta['item'] = item
            yield request


    def parse_detail_page(self,respone):
        item = respone.meta['item']
        result = HtmlParser.parse_detail_page_main(respone)

        if result['title']:
            item['title'] = result['title']

        if result['create_date']:
            item['create_date'] = result['create_date']

        return item








