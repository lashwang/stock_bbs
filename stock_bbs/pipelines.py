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


    def __init__(self):
        MongoDB.bbs_list_coll.create_index(self.__get_uniq_key(),unique=True)

    def process_item(self, item, spider):
        if spider.name == 'stock_list':
            self.process_item_bbs_list(item,spider)
        elif spider.name == 'stock_detail':
            self.process_item_bbs_detail(item,spider)

    def process_item_bbs_list(self,item,spider):
        #print 'process_item_bbs_list,click number:',item['clickNumber']
        clickNumber = int(item['clickNumber'])
        if clickNumber < int(settings['CLICKNUMBER_THRESHOLD'])*10000:
            return item

        data = dict(item)
        print data

        if False:
            MongoDB.bbs_list_coll.insert(data)
        else:
            MongoDB.bbs_list_coll.update({'url':data['url']},{'$set':data},True)
            print "bbs profile added to MongoDB database!"

        return item


    def process_item_bbs_detail(self,item,spider):
        print 'process_item_bbs_detail'

    def __get_uniq_key(self):
        if not settings['MONGODB_UNIQ_KEY'] or settings['MONGODB_UNIQ_KEY'] == "":
            return None
        return settings['MONGODB_UNIQ_KEY']