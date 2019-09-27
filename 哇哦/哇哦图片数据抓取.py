# coding:utf-8
# author:ls
import time, datetime, json, re, os, sys, random, shutil
from pymongo import MongoClient
import time
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.touch_actions import TouchActions
import selenium.webdriver.support.ui as ui
from selenium.webdriver.common.by import By
import selenium.webdriver.support.expected_conditions as EC


mobileEmulation = {'deviceName': 'iPhone 7'}
option = webdriver.ChromeOptions()
option.add_experimental_option('mobileEmulation', mobileEmulation)
option.add_experimental_option('excludeSwitches', ['enable-automation'])  # 反识别
option.add_argument('headless')
# option.add_argument(f"--proxy-server={random.choice([i['ip'] for i in collection.find()])}")
client = MongoClient('120.92.49.240', username='root', password='BDqilingzhengfan1',)


def get(url):
    try:
        driver = webdriver.Chrome(chrome_options=option)
        driver.get(url)
        WebDriverWait(driver, 5)

        button = driver.find_element_by_tag_name('a')
        Action = TouchActions(driver)
        Action.scroll_from_element(button, 0, 30000).perform()
        client.all_post.wao_url.update({'_id': url}, {'$set': {'status': 1}})
        driver.quit()
    except Exception as e:
        print(e)


if __name__ == '__main__':
    url_list = [i['_id'] for i in client.all_post.wao_url.find({'status': 0}).limit(120)]
    for url in url_list:
        print(url)
        get(url)
        break
