# coding:utf-8
# author:ls
import gevent.monkey
gevent.monkey.patch_all()
from gevent.pool import Pool
import time, datetime, json, re, os, sys, random, shutil
from pymongo import MongoClient
import requests as r
import cv2

client = MongoClient('120.92.49.240', username='root', password='BDqilingzhengfan1',)
path = '/data/workspace/allvideo/'


def get_ip():
    while 1:
        try:
            ip = random.choice([i['ip'] for i in client.ips.ips.find()])
            url = 'http://www.httpbin.org/ip'
            a, b = ip.split('://')
            proxies = {a: b}
            html = r.get(url, proxies=proxies, timeout=3)
            if '120.131.10.99' not in html.text:
                return ip
        except:
            pass


def download(info):
    try:
        pic = r.get(info['url'], proxies={'https': get_ip()})
        if pic.status_code == 200:
            filename = path+str(info['post_id'])+'/'
            try:
                os.mkdir(filename)
            except:pass
            with open(filename+'1.mp4', 'wb') as f:
                f.write(pic.content)
            if cv2.VideoCapture(filename+'1.mp4') is None:
                os.remove(filename+'1.mp4')
                client.download.video.update({'_id': info['_id']}, {'$set': {'status': 5}})
                client.all_post.post_data.update({'_id': info['post_id']}, {'$set': {'download_status': 5}})
                return
            client.download.video.update({'_id': info['_id']}, {'$set': {'status': 1}})
            client.all_post.post_data.update({'_id': info['post_id']}, {'$set': {'download_status': 1}})
            print('over:', info['_id'])
    except Exception as e:
        print(e)


if __name__ == '__main__':
    pool = Pool(10)
    while 1:
        datas = client.download.video.find({'status': 0})
        pool.map(download, datas)
        time.sleep(60)
