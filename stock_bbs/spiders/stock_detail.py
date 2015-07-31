# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider,Rule
from stock_bbs.parser.HtmlParser import *
from scrapy.linkextractors import LinkExtractor
from scrapy.http import Request
from stock_bbs.utils.utils import *
from scrapy.exceptions import CloseSpider


__author__ = 'Simon'



class StockDetailSpider(CrawlSpider):
    name = "stock_detail"
    allowed_domains = ["bbs.tianya.cn"]
    start_urls = (
        'http://bbs.tianya.cn/list-stocks-1.shtml',
    )


    def __init__(self, *a, **kw):
        self.start_urls = []


        super(StockDetailSpider, self).__init__(*a, **kw)

    def parse_start_url(self, response):
        print response.url




