# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider,Rule
from stock_bbs.parser.html_parser import *
from scrapy.linkextractors import LinkExtractor
from scrapy.http import Request
from stock_bbs.utils.utils import *
from scrapy.exceptions import CloseSpider
from stock_bbs.database.mongodb import MongoDB

__author__ = 'Simon'



class StockDetailSpider(CrawlSpider):
    name = "stock_detail"
    allowed_domains = ["bbs.tianya.cn"]
    start_urls = (
        'http://bbs.tianya.cn/list-stocks-1.shtml',
    )


    def __init__(self, *a, **kw):
        self.start_urls = []
        for d in MongoDB.collection_list.find()[:2]:
            print d['_id']
            self.start_urls.append(d['url'])

        super(StockDetailSpider, self).__init__(*a, **kw)

    def parse_start_url(self, response):
        print 'parse_start_url:',response.url

        HtmlParser.parse_detail_page_main(response)




