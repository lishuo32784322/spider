# coding:utf-8
# author:ls
import time, datetime, json, re, os, sys, random, shutil
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
from tools.time_tool import parse_time


client = MongoClient('120.92.49.240', username='root', password='BDqilingzhengfan1')
option = webdriver.ChromeOptions()
option.add_experimental_option('excludeSwitches', ['enable-automation'])  # 反识别
# option.add_argument('headless')
prefs = {'profile.default_content_setting_values': {'images': 2, }}
option.add_experimental_option('prefs', prefs)
user_agent_list = ["Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 10.0; …) Gecko/20100101 Firefox/61.0",
                    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36",
                    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36",
                    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
                    "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10.5; en-US; rv:1.9.2.15) Gecko/20110303 Firefox/3.6.15"]


def get_user():
    driver = webdriver.Chrome(chrome_options=option)
    driver.get('https://www.mogu.com/')
    # ui.WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, '//div[@class="column-wrap"]')))
    time.sleep(5)
    button = driver.find_element_by_xpath('//a')
    Action = TouchActions(driver)
    Action.scroll_from_element(button, 0, 10000).perform()


get_user()



