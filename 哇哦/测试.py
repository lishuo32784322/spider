# coding:utf-8
# author:ls
import time, datetime, json, re, os, sys, random, shutil
import requests as r
from pymongo import MongoClient
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.touch_actions import TouchActions
import selenium.webdriver.support.ui as ui
from selenium.webdriver.common.by import By
import selenium.webdriver.support.expected_conditions as EC
import gevent.monkey
gevent.monkey.patch_all()
from gevent.pool import Pool
from selenium.common.exceptions import TimeoutException
import vthread
from selenium_news.change_status import change_sohu


option = webdriver.ChromeOptions()
option.add_experimental_option('excludeSwitches', ['enable-automation'])  # 反识别
option.add_argument('headless')
# option.add_argument(f"--proxy-server={random.choice([i['ip'] for i in collection.find()])}")
prefs = {'profile.default_content_setting_values': {'images': 2, }}
option.add_experimental_option('prefs', prefs)
client = MongoClient('120.92.49.240', username='root', password='BDqilingzhengfan1')


url = 'http://cloud.video.taobao.com/play/u/1739067580/p/1/e/6/t/1/d/ld/228241890473.mp4'
html = r.get(url).text
print(html)


s1 = 'http://daren-auth.alicdn.com/a9b5b21ee64d2b47/4sgI4ZxLLwFyfeb76AJ/GKKBUIMvjFGmwkyLLnn_230707765011_hd_hq.mp4?auth_key=1563085201-0-0-b7baf815e83dacf03a3522802f16628c'
s2 = 'http://daren-auth.alicdn.com/a9b5b21ee64d2b47/4sgI4ZxLLwFyfeb76AJ/GKKBUIMvjFGmwkyLLnn_230707765011_ld_hq.mp4?auth_key=1562828682-0-0-99d248049f20338bcd8090b493ee1c41'

