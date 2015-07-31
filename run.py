# -*- coding: utf-8 -*-

__author__ = 'Simon'

from scrapy import cmdline

if __name__ == '__main__':
    cmdline.execute("scrapy crawl stock_list".split())
