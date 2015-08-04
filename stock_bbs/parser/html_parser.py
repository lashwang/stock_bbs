# -*- coding: utf-8 -*-
__author__ = 'Simon'

from stock_bbs.items import StockBBSProfieItem
import urlparse
from scrapy.exceptions import CloseSpider


class HtmlParser(object):
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
        result = {}


        if title and len(title) == 1:
            title = title[0]
            #print title
            result['title']= title

        origin_date = response.xpath(u'//*[@id="post_head"]//*[@class="atl-info"]//span[2]//text()').extract()

        if origin_date and len(origin_date) == 1:
            origin_date = origin_date[0]
            #print origin_date
            result['origin_date']= origin_date

        uname = response.xpath(u'//*[@id="post_head"]//*[@class="atl-info"]//*[@uname]//text()').extract()
        if uname and len(uname) == 1:
            uname = uname[0]
            #print uname
            result['uname']= uname

        page_links = response.xpath(u'//*[@id="post_head"]//*[@class="atl-pages"]//a/@href').extract()
        if page_links and len(page_links) > 2:
            next_page_link = page_links[-1]
            last_page_link = page_links[-2]
            #print last_page_link
            result['last_page_link']= urlparse.urljoin(response.url,last_page_link)
            #print next_page_link
            result['next_page_link']= urlparse.urljoin(response.url,next_page_link)

        # get author's comment
        # get author's first comment
        first_comment = response.xpath(u'//*[@class="atl-item host-item"]//*[contains(@class,"bbs-content")]').extract()
        if first_comment and len(first_comment) == 1:
            first_comment = first_comment[0]
            #print first_comment
            result['first_comment']= first_comment



        return result

    @staticmethod
    def parse_detail_page_sub(response,uname):
        print 'call parse_detail_page_sub'
        page_details = {}

        # get prev page
        prev_page_link = response.xpath(u'//*[@id="post_head"]//*[@class="atl-pages"]//a/@href').extract()
        if prev_page_link and len(prev_page_link) >= 2:
            last_page_link = prev_page_link[0]
            page_details['prev_page_link'] = urlparse.urljoin(response.url,last_page_link)


        # get user's comments
        comments_list_selector = response.xpath(u'//*[@class="atl-item"]')
        bbs_list = HtmlParser.parse_comment_by_uname(comments_list_selector,uname)
        page_details['bbs_list'] = bbs_list

        return page_details


    @staticmethod
    def parse_comment_by_uname(selector,uname):
        bbs_list = []

        for each in selector:
            _uname = each.xpath(u'.//*[@class="atl-info"]//*[@uname]//text()').extract()
            if _uname and len(_uname) == 1:
                _uname = _uname[0]
                #print _uname
                if _uname.encode('utf8') == uname.encode('utf8'):
                    publish_time = each.xpath(u'.//*[@class="atl-info"]//span[2]//text()').extract()
                    print "fine same user"
                    if publish_time and len(publish_time) == 1:
                        publish_time = publish_time[0]
                        #print publish_time
                    else:
                        print 'unexpected xpath in publish time'

                    bbs_content = each.xpath(u'.//*[@class="atl-content"]//*[contains(@class,"bbs-content")]').extract()

                    if bbs_content and len(bbs_content) == 1:
                        bbs_content = bbs_content[0]
                        #print bbs_content
                    else:
                        print 'unexpected xpath in bbs context'

                    bbs_list.append({'publish_time':publish_time,'bbs_content':bbs_content})
            else:
                print 'unexpected xpath in uname'

        return bbs_list
