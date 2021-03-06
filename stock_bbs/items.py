# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class StockBBSProfieItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    author = scrapy.Field()
    clickNumber = scrapy.Field()
    responseNUmber = scrapy.Field()
    create_date = scrapy.Field()
    pass


class StockBBSDetailItem(scrapy.Item):
    url = scrapy.Field()
    first_comment = scrapy.Field()
    bbs_list = scrapy.Field() # list of bbs comment

