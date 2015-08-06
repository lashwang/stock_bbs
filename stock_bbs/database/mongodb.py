# -*- coding: utf-8 -*-
from pymongo.connection import MongoClient
from scrapy.conf import settings
from scrapy.exceptions import DropItem
from scrapy import log

__author__ = 'Simon'



class MongoDB(object):
    client = MongoClient(settings['MONGODB_SERVER'],settings['MONGODB_PORT'])
    db = client[settings['MONGODB_DB']]
    bbs_list_coll = db[settings['MONGODB_COLLECTION_LIST']]




