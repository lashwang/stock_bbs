# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider,Rule
from stock_bbs.parser.html_parser import *
from scrapy.linkextractors import LinkExtractor
from scrapy.http import Request
from stock_bbs.utils.utils import *
from scrapy.exceptions import CloseSpider
from stock_bbs.database.mongodb import MongoDB
from scrapy.conf import settings


__author__ = 'Simon'



class StockDetailSpider(CrawlSpider):
    name = "stock_detail"
    allowed_domains = ["bbs.tianya.cn"]
    start_urls = (
        'http://bbs.tianya.cn/list-stocks-1.shtml',
    )


    def __init__(self, *a, **kw):
        self.start_urls = []
        for d in MongoDB.bbs_list_coll.find()[:1]:
            self.start_urls.append(d['url'])

        super(StockDetailSpider, self).__init__(*a, **kw)

    def parse_start_url(self, response):
        print 'parse_start_url:',response.url

        result = HtmlParser.parse_detail_page_main(response)
        print result

        if result['last_page_link']:
            request = Request(result['last_page_link'],callback=self.parse_sub_url)
            request.meta['uname'] = result['uname']
            request.meta['count'] = 1
            return request



    def parse_sub_url(self,response):
        uname = response.meta['uname']
        count = response.meta['count']
        max_page_count = int(settings['MAX_DETAIL_PAGE'])
        print 'parse_sub_url:',response.url,uname
        results = HtmlParser.parse_detail_page_sub(response,response.meta['uname'])
        print results

        if count >= max_page_count:
            print 'get max detailed page:',count
            return

        if results['prev_page_link']:
            request = Request(results['prev_page_link'],callback=self.parse_sub_url)
            request.meta['uname'] = uname
            request.meta['count'] = count + 1
            return request



