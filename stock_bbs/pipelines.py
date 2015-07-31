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


class MongoDBPipeline(object):

    def process_item(self, item, spider):
        print 'process_item'
        print item
        valid = True
        for data in item:
            if not data:
                valid = False
                raise DropItem("Missing {0}!".format(data))
        if valid:
            MongoDB.collection_list.insert(dict(item))
            print("bbs profile added to MongoDB database!")
        return item
