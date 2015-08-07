# -*- coding: utf-8 -*-

__author__ = 'Simon'

from scrapy import cmdline
import sys


def main():
    print sys.argv
    if len(sys.argv) == 2:
        cmdline.execute(("scrapy crawl " + sys.argv[1]).split())

if __name__ == '__main__':
    main()




