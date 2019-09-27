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
from selenium.common.exceptions import TimeoutException
from tools.time_tool import parse_time


client = MongoClient('120.131.10.99', port=27017, username='root', password='BDqilingzhengfan1')
option = webdriver.ChromeOptions()
option.add_experimental_option('excludeSwitches', ['enable-automation'])  # 反识别
option.add_argument('headless')
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


def get_post(target_url):
    while 1:
        try:
            option.add_argument(f"--proxy-server={random.choice([i['ip'] for i in client.ips.ips.find()])}")
            break
        except:time.sleep(0.5)
    option.add_argument(random.choice(user_agent_list))
    option.add_experimental_option('w3c', False)
    driver = webdriver.Chrome(chrome_options=option)
    # driver.maximize_window()
    try:
        driver.get(target_url)
        print(target_url)
        ui.WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, '//a[@class="block"]')))
    except TimeoutException as e:
        driver.quit()
        print(e)
        return
    button = driver.find_element_by_xpath('//a[@class="block"]')
    Action = TouchActions(driver)
    Action.scroll_from_element(button, 0, 5000).perform()
    datas = driver.find_elements_by_tag_name('a')
    urls = [i for i in [i.get_attribute('href') for i in datas if i.get_attribute('href')] if 'detail' in i]
    for url in urls:
        try:
            client.all_post.mogujie_detail_url.insert({'_id': url, 'status': 0})
            print('over:', url)
        except Exception as e:
            print(e)
    client.all_post.mogujie_user.update({'_id': target_url}, {'$set': {'status': 1}})
    driver.quit()

if __name__ == '__main__':
    pool = Pool(3)
    while 1:
        urls = [i['_id'] for i in client.all_post.mogujie_user.find({'status': 0}).limit(30)]
        print(len(urls))
        if urls:
            pool.map(get_post, urls)
        print(len(urls), 'over')
        time.sleep(60)