from pymongo import MongoClient
import requests as r
import random
import time
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.touch_actions import TouchActions
import gevent.monkey
gevent.monkey.patch_all()
from gevent.pool import Pool


mobileEmulation = {'deviceName': 'iPhone 7'}
option = webdriver.ChromeOptions()
option.add_experimental_option('mobileEmulation', mobileEmulation)
option.add_experimental_option('excludeSwitches', ['enable-automation'])  # 反识别
option.add_argument('headless')
# option.add_argument(f"--proxy-server={random.choice([i['ip'] for i in collection.find()])}")
prefs = {'profile.default_content_setting_values': {'images': 2, }}
option.add_experimental_option('prefs', prefs)
client = MongoClient('120.92.49.240', username='root', password='BDqilingzhengfan1')


def get(url):
    try:
        driver = webdriver.Chrome(chrome_options=option)
        driver.get(url)
        WebDriverWait(driver, 5)
        time.sleep(5)
        button = driver.find_element_by_tag_name('a')
        Action = TouchActions(driver)
        Action.scroll_from_element(button, 0, 50000).perform()
        client.all_post.wao_url.update({'_id': url}, {'$set': {'status': 1}})
        driver.quit()
    except Exception as e:
        print(e, url)


if __name__ == '__main__':
    pool = Pool(10)
    while 1:
        url_list = [i['_id'] for i in client.all_post.wao_url.find({'status': 0}).limit(120)]
        print(len(url_list))
        pool.map(get, url_list)
        time.sleep(600)
