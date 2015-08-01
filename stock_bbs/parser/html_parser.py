# -*- coding: utf-8 -*-
__author__ = 'Simon'

from stock_bbs.items import StockBBSProfieItem
import urlparse
from scrapy.exceptions import CloseSpider


class HtmlParser():
    def __init__(self):
        pass

    @staticmethod
    def parse_bbs_ticket(hxs,response):
        hxs = hxs.xpath(u'.//td')
        bbsProfile = StockBBSProfieItem()
        #print len(hxs),hxs
        if len(hxs) == 0:
            return None
        url = (hxs[0]).xpath(u'.//a/@href').extract()
        if url and len(url) == 1:
            url = urlparse.urljoin(response.url,url[0])
            bbsProfile['url'] = url
            #print "url:" + url
        '''
        title = (hxs[0]).xpath(u'.//a/text()').extract()
        if title and len(title[0].strip()) == 0:
            title = (hxs[0]).xpath(u'.//a//span[1]//text()').extract()
        if title and len(title[0].strip()) == 0:
            title = (hxs[0]).xpath(u'.//a/text()[last()]').extract()
        if title and len(title[0].strip()) > 0:
            title = title[0].strip()
            bbsProfile['title'] = title
        else:
            from scrapy.utils.response import open_in_browser
            print "empty title:",url
            print title
            open_in_browser(response)
            raise CloseSpider('page number limit exceeded:')
        '''


        author = (hxs[1]).xpath(u'.//a/text()').extract()
        if author and len(author) == 1:
            author = author[0]
            bbsProfile['author'] = author
            #print "author:" + author

        clictNumber = (hxs[2]).xpath(u'.//text()').extract()
        if clictNumber and len(clictNumber):
            clictNumber = clictNumber[0]
            bbsProfile['clickNumber'] = clictNumber
            #print "clictNumber:" + clictNumber

        responseNUmber = (hxs[3]).xpath(u'.//text()').extract()
        if responseNUmber and len(responseNUmber):
            responseNUmber = responseNUmber[0]
            bbsProfile['responseNUmber'] = responseNUmber
            #print "responseNUmber:" +responseNUmber


        return bbsProfile

    @staticmethod
    def parse_detail_page_main(response):
        title = response.xpath(u'//*[@class="s_title"]//span//text()').extract()

        if title and len(title) == 1:
            title = title[0]
            print title

        origin_date = response.xpath(u'//*[@id="post_head"]//*[@class="atl-info"]//span[2]//text()').extract()

        if origin_date and len(origin_date) == 1:
            origin_date = origin_date[0]
            print origin_date
