# -*- coding: utf-8 -*-
import scrapy
from pymongo import MongoClient
from tools.tool import format_string
import json
import time


class PicSpider(scrapy.Spider):
    name = 'pic'
    client = MongoClient('120.92.49.240', username='root', password='BDqilingzhengfan1', )
    db = client.red_book.video_url
    headers = format_string("curl -H 'Host: www.xiaohongshu.com' -H 'content-type: application/json' -H 'accept: */*' -H 'auth-sign: 5cefc70fbbeb9b35b4c7439d681214b0' -H 'authorization: 33dc7ea0-2bcb-4a35-a2ef-f6c934ea4f03' -H 'auth: eyJoYXNoIjoibWQ0IiwiYWxnIjoiSFMyNTYiLCJ0eXAiOiJKV1QifQ.eyJzaWQiOiI0ODg5OTUwZmI0Mzk0YjAxY2JkMGQ5Zjc5NjVhOWI4MCIsImV4cGlyZSI6MTU1OTY0MDg5Nn0.yHLTMw0riRX5_RG1WQaug_n5HJMRsmNwWj0tfGXZg5I' -H 'accept-language: zh-cn' -H 'device-fingerprint: WHJMrwNw1k/GaeNGHnkhNIDV1/SFX62MnEtkozUrlw0VZISqGKRuapmTuP02VKNnGz347aB0ySWIhnwk4dvIw1P5vuK38kNCqdCW1tldyDzmauSxIJm5Txg==1487582755342' -H 'referer: https://servicewechat.com/wxffc08ac7df482a27/237/page-frame.html' -H 'user-agent: Mozilla/5.0 (iPhone; CPU iPhone OS 12_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/16B92 MicroMessenger/7.0.3(0x17000321) NetType/WIFI Language/zh_CN' --compressed 'https://www.xiaohongshu.com/wx_mp_api/sns/v1/note/5cdba0dc000000000d016101/feed?num=10&page=1&fetch_mode=3&sid=session.1558582579592269310895'")


    def start_requests(self):
        urls = [i['_id'] for i in self.db.find().limit(50000)]
        for i,id in enumerate(urls):
            url = f'https://www.xiaohongshu.com/wx_mp_api/sns/v1/note/{id}/feed?num=10&page=1&fetch_mode=3&sid=session.1558582579592269310895'
            yield scrapy.Request(url, headers=self.headers, meta={'id': id})
            # time.sleep(3)

    def parse(self, response):
        try:
            data = json.loads(response.text)
            print('This is code:', response.status)
            # print(response.text)
            self.client.red_book.pic_post.save({'data': response.text})
            self.db.remove({'_id': response.meta['id']})
            print('成功一条')
        except Exception as e:
            print(e)

