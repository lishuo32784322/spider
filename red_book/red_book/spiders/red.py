# -*- coding: utf-8 -*-
import scrapy, pymongo, random, json, re
from tools.tool import format_string


class RedSpider(scrapy.Spider):
    name = 'red'
    iPhone_USER_AGENT = [
        'Mozilla/5.0 (iPhone; CPU iPhone OS 9_3_2 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Mobile/13F69 MicroMessenger/6.6.1 NetType/4G Language/zh_CN',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 11_2_2 like Mac OS X) AppleWebKit/604.4.7 (KHTML, like Gecko) Mobile/15C202 MicroMessenger/6.6.1 NetType/4G Language/zh_CN',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 11_1_1 like Mac OS X) AppleWebKit/604.3.5 (KHTML, like Gecko) Mobile/15B150 MicroMessenger/6.6.1 NetType/WIFI Language/zh_CN',
        'Mozilla/5.0 (iphone x Build/MXB48T; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043632 Safari/537.36 MicroMessenger/6.6.1.1220(0x26060135) NetType/WIFI Language/zh_CN'
    ]
    headers = format_string("curl -H 'Host: www.xiaohongshu.com' -H 'Accept: */*' -H 'Auth-Sign: c7e254272d4f8135f0244464063a3a57' -H 'Authorization: 56b19be7-9f1a-4336-949a-e8520a1f9370' -H 'Auth: eyJoYXNoIjoibWQ0IiwiYWxnIjoiSFMyNTYiLCJ0eXAiOiJKV1QifQ.eyJzaWQiOiIxMWQxYzUyMTcyZTY0OTY0YzkzNmRkN2IzNDYzZDI0ZCIsImV4cGlyZSI6MTU1OTIyMDA3NH0.sxi85D6Lhb6nR24Z3D9GUO7MD1LeXAhPrr3WIVlpriY' -H 'Accept-Language: zh-cn' -H 'Device-Fingerprint: WHJMrwNw1k/HU+r3oYFpgKhGuBtA+nDYpI7w7yIC9S8HnxMqIVXJLXKEkWtRGHPd6IljtTwlFuTugZKRqN8h4eKdSHllqVJZ9dCW1tldyDzmauSxIJm5Txg==1487582755342' -H 'Content-Type: application/json' -H 'Referer: https://servicewechat.com/wxffc08ac7df482a27/234/page-frame.html' -H 'User-Agent: Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_3 like Mac OS X) AppleWebKit/603.3.8 (KHTML, like Gecko) Mobile/14G60 MicroMessenger/7.0.4(0x17000428) NetType/WIFI Language/zh_CN' --compressed 'https://www.xiaohongshu.com/wx_mp_api/sns/v1/homefeed?oid=homefeed_recommend&cursor_score=1559218614.9900&sid=session.1558441002986963222179'")
    headers['User-Agent'] = random.choice(iPhone_USER_AGENT)
    client = pymongo.MongoClient('120.92.49.240', username='root', password='BDqilingzhengfan1',)


    def start_requests(self):
        db = self.client['red_book']['user']
        datas = db.find().limit(100).skip(700)
        # print(datas)
        for i in datas:
            url = 'https://www.xiaohongshu.com/wx_mp_api/sns/v1/note/user/%s?sid=session.1558441002986963222179&page=1&page_size=15'%i['_id']
            print('user_url:', url)
            yield scrapy.Request(url, headers=self.headers, dont_filter=True)
            # break


    def parse(self, response):
        # print(response.text)
        # print(1)
        db = self.client['red_book']['post_url']
        # print(response.url)
        try:
            html = json.loads(response.text)
            data = html['data']['notes']
        except Exception as e:print(e)
        for i in data:
            i = i['id']
            # print(i)
            db.save({'_id': 'https://www.xiaohongshu.com/discovery/item/'+str(i)})
            # print('存入一个贴子ID')
        if len(data) == 10:
            next = str(int(re.search('&page=(.*)&', response.url).group(1)) + 1)
            print('next:', next)
            url = re.sub('&(page=.*)&', '&page=%s&' % next, response.url)
            # try:
            yield scrapy.Request(url, headers=self.headers, callback=self.parse, dont_filter=True)
        # print('翻页成功+1')
            # except Exception as e :print('err', e)



