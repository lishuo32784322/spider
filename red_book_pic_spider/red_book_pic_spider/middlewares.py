# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
import random
from tools.tool import format_string
from pymongo import MongoClient


class RedBookPicSpiderSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class RedBookPicSpiderDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.
    client = MongoClient('120.92.49.240', username='root', password='BDqilingzhengfan1', )
    db = client.ips


    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        try:
            collection = self.db.ips
            ip = random.choice([i['ip'] for i in collection.find()])
            request.meta['proxy'] = ip
        except Exception as e:
            print(e)
        iPhone_USER_AGENT = [
            'Mozilla/5.0 (iPhone; CPU iPhone OS 9_3_2 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Mobile/13F69 MicroMessenger/6.6.1 NetType/4G Language/zh_CN',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 11_2_2 like Mac OS X) AppleWebKit/604.4.7 (KHTML, like Gecko) Mobile/15C202 MicroMessenger/6.6.1 NetType/4G Language/zh_CN',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 11_1_1 like Mac OS X) AppleWebKit/604.3.5 (KHTML, like Gecko) Mobile/15B150 MicroMessenger/6.6.1 NetType/WIFI Language/zh_CN',
            'Mozilla/5.0 (iphone x Build/MXB48T; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043632 Safari/537.36 MicroMessenger/6.6.1.1220(0x26060135) NetType/WIFI Language/zh_CN'
        ]
        headers = format_string(
            "curl -H 'Host: www.xiaohongshu.com' -H 'Accept: */*' -H 'Auth-Sign: 5f9e2f7d11a11b0c28484bc30ee85f37' -H 'Authorization: a6577247-c5c4-4815-894b-fd7495667221' -H 'Auth: eyJoYXNoIjoibWQ0IiwiYWxnIjoiSFMyNTYiLCJ0eXAiOiJKV1QifQ.eyJzaWQiOiJmMTk2Y2JmNDYyNTU0MmVhYzI3Yzk4MmM4ZjA3NDMwMSIsImV4cGlyZSI6MTU1OTIxMDkyOH0.ZVQYJFl-6GGqHP5V3X-naNhOni0xX4Uwu_mCoQWMsFc' -H 'Accept-Language: zh-cn' -H 'Device-Fingerprint: WC39ZUyXRgdHbxgv8hMjcN/f3QYWLuBoNuLqt8gHm+j8PY8hXyHkeHY/athAdnsALal934aHE/ZyxxwNfS9+gZFt6rHpzfpTFtL/WmrP2Tauiuo9Z2Nzm4Q==1487577677129' -H 'Content-Type: application/json' -H 'Referer: https://servicewechat.com/wxffc08ac7df482a27/234/page-frame.html' -H 'User-Agent: Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_3 like Mac OS X) AppleWebKit/603.3.8 (KHTML, like Gecko) Mobile/14G60 MicroMessenger/7.0.4(0x17000428) NetType/WIFI Language/zh_CN' --compressed 'https://www.xiaohongshu.com/wx_mp_api/sns/v1/homefeed?oid=homefeed_recommend&cursor_score=&sid=session.1558441002986963222179'")
        headers['User-Agent'] = random.choice(iPhone_USER_AGENT)
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
