# coding:utf-8
# author:ls
import time, datetime, json, re, os, sys, random, shutil
import requests as r
import vthread
from pymongo import MongoClient


client = MongoClient('120.92.49.240', username='root', password='BDqilingzhengfan1')
path = '/Users/lishuo/spider/workspace/哇哦/'


def get_ip():
    while 1:
        try:
            ip = random.choice([i['ip'] for i in client.ips.ips.find()])
            url = 'http://www.httpbin.org/ip'
            a, b = ip.split('://')
            proxies = {a: b}
            html = r.get(url, proxies=proxies, timeout=2).text
            if '61.148.212.130' not in html:
                return ip
        except Exception as e:
            pass


def os_dir(func):
    def main(url, id):
            try:
                filename = path+id
                os.mkdir(filename)

            except Exception as e:pass
            return func(url, id)
    return main


@vthread.pool(3)
@os_dir
def download(url, id):
    print(id)
    filename = path + id
    try:
        video = r.get(url, proxies={'http': get_ip()}, timeout=3).content
        with open(f'{filename}/1.jpg', 'wb') as f:
            f.write(video)
        client.all_post.wao_data.update({'_id': id}, {'$set': {'download_status': 1}})

    except Exception as e:
        print(e)
        download(url, id)


if __name__ == '__main__':
    datas = client.all_post.wao_data.find({'download_status': 0}, {'pic1': 1}).limit(9)
    for i in datas:
        download(i['pic1'], i['_id'])
