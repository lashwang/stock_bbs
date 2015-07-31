# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from pymongo.connection import MongoClient
from scrapy.conf import settings
from scrapy.exceptions import DropItem
from scrapy import log

class MongoDBPipeline(object):

    def __init__(self):
        client = MongoClient(settings['MONGODB_SERVER'],settings['MONGODB_PORT'])
        self.db = client[settings['MONGODB_DB']]
        self.collection = self.db[settings['MONGODB_COLLECTION_LIST']]

    def process_item(self, item, spider):
        print 'process_item'
        valid = True
        for data in item:
            if not data:
                valid = False
                raise DropItem("Missing {0}!".format(data))
        if valid:
            self.collection.insert(dict(item))
            log.msg("Question added to MongoDB database!",
                    level=log.DEBUG, spider=spider)
        return item
