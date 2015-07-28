# -*- coding: utf-8 -*-
import scrapy


class StockSpider(scrapy.Spider):
    name = "stock"
    allowed_domains = ["bbs.tianya.cn"]
    start_urls = (
        'http://bbs.tianya.cn/list-stocks-1.shtml',
    )

    def parse(self, response):
        pass
