# coding:utf-8
# author:ls
import time, datetime, json, re, os, sys, random, shutil
import pandas as pd
from pymongo import MongoClient


client = MongoClient('120.92.49.240', username='root', password='BDqilingzhengfan1',)


df = pd.read_excel('/Users/lishuo/spider/workspace/哇哦/2/哇哦视频二期 2.xlsx')
for i in df['地址'].values.tolist():
    try:
        client.all_post.wao_url.insert({'_id': re.search('】(.*?) 点', i).group(1), 'status': 0})
    except:pass





