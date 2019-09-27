# coding:utf-8
# author:ls
import time, datetime, json, re, os, sys, random, shutil
from pymongo import MongoClient


client = MongoClient('120.92.49.240', username='root', password='BDqilingzhengfan1')


for i in client.all_post.post_data.find({'source': 6}):
    client.all_post.post_data.update({'_id': i['_id']}, {'$set': {'video': 'http://'+i['video']}})

