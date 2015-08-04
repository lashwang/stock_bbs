# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from pymongo.connection import MongoClient
from scrapy.conf import settings
from scrapy.exceptions import DropItem
from scrapy import log
from database.mongodb import MongoDB
from scrapy.conf import settings

class MongoDBPipeline(object):

    def process_item(self, item, spider):
        if spider.name == 'stock_list':
            self.process_item_bbs_list(item,spider)
        elif spider.name == 'stock_detail':
            self.process_item_bbs_detail(item,spider)

    def process_item_bbs_list(self,item,spider):
        print 'process_item,click number:',item['clickNumber']
        clickNumber = int(item['clickNumber'])
        if clickNumber < int(settings['CLICKNUMBER_THRESHOLD'])*10000:
            return item

        valid = True
        for data in item:
            if not data:
                valid = False
                raise DropItem("Missing {0}!".format(data))
        if valid:
            MongoDB.collection_list.insert(dict(item))
            print("bbs profile added to MongoDB database!")
        return item


    def process_item_bbs_detail(self,item,spider):
        print 'process_item_bbs_detail'

