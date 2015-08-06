#coding=utf-8
__author__ = 'Simon'


import unittest2 as unittest
from stock_bbs.parser.html_parser import *

class TestRun(unittest.TestCase):
    def test_create_time_parse(self):
        time_str = u'时间：2015-04-15 00:31:00 '
        time = HtmlParser.parse_create_date(time_str)
        self.assertTrue(datetime.datetime(2015,04,15,00,31,00).now(),time.now())
