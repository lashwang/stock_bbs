# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from stock_bbs.parser.HtmlParser import *

class StockSpider(scrapy.Spider):
    name = "stock"
    allowed_domains = ["bbs.tianya.cn"]
    start_urls = (
        'http://bbs.tianya.cn/list-stocks-1.shtml',
    )

    def parse(self, response):
        hxs = response.xpath(u'//div[@class="mt5"]')
        print hxs
        hxs = hxs.xpath(u'.//tr')
        print response.url
        for each in hxs:
            yield HtmlParser.parse_bbs_ticket(each,response)











