# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider,Rule
from stock_bbs.parser.HtmlParser import *
from scrapy.linkextractors import LinkExtractor
from scrapy.http import Request
from stock_bbs.utils.utils import *
from scrapy.exceptions import CloseSpider

class StockSpider(CrawlSpider):
    name = "stock_list"
    PAGE = 0
    MAX_PAGE = 1
    depth = 0

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

    rules = (
        Rule (LinkExtractor(allow=("nextid", ),
            restrict_xpaths=('//div[@class="links"]/a[@rel="nofollow"]',)),
            callback="parse_index_page", follow=True),
    )

    def parse_start_url(self, response):
        return self.parse_index_page(response)


    def parse_index_page(self,response):
        if self.PAGE > self.MAX_PAGE:
            print 'page number limit exceeded:'
            raise CloseSpider('page number limit exceeded:')
        self.PAGE += 1
        print 'parse_index_page,url:',response.url
        hxs = response.xpath(u'//div[@class="mt5"]')
        hxs = hxs.xpath(u'.//tr')
        for each in hxs:
            yield HtmlParser.parse_bbs_ticket(each,response)


    def parse_detail_page(self,respone):
        print 'parse_detail_page,url:',respone.url
        Request("http://annapolis.craigslist.org/sof/", callback=self.parse_detail_page)

        pass








