# coding:utf-8
# author:ls
import time, datetime, json, re, os, sys, random, shutil
import selenium.webdriver.support.ui as ui
from selenium.webdriver.common.by import By
import selenium.webdriver.support.expected_conditions as EC
import vthread
from pymongo import MongoClient
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait


# urls_list = []
# with open('/Users/lishuo/spider/workspace/selenium_bilibili/B站账号整理.csv', 'r') as f:
#     urls = re.findall('(https://.*?),,,,', f.read())
#     for url in urls:
#         if 'video' not in url:
#             try:
#                 client.all_post.b_url.insert({'_id': url, 'status': 0})
#             except Exception as e:
#                 print(e)
            # urls_list.append(url)
# print(urls, len(urls))
client = MongoClient('120.92.49.240', username='root', password='BDqilingzhengfan1',)
option = webdriver.ChromeOptions()
prefs = {
    'profile.default_content_setting_values': {
        'images': 2,
    }
}
# mobileEmulation = {'deviceName': 'iPhone 7'}
# option.add_argument(f"--proxy-server={random.choice([i['ip'] for i in collection.find()])}")
option.add_experimental_option('excludeSwitches', ['enable-automation'])  # 反识别
option.add_argument('headless')
option.add_experimental_option('prefs', prefs)



@vthread.pool(5)
def get(url):
    count = 0
    driver = webdriver.Chrome(chrome_options=option)
    driver.get(url)
    while 1:
        try:
            ui.WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, '//div[@class="meta"]')))
            count += 1
            ui.WebDriverWait(driver, 3).until(EC.visibility_of_element_located((By.XPATH, '//li[@class="be-pager-next"]')))
            driver.find_element_by_xpath('//li[@class="be-pager-next"]').click()
        except:break
    if count >= 1:
        client.all_post.bili_url.update({'_id': url}, {'$set': {'status': 1}})
        print(url)
    client.all_post.bili_url.remove({'_id': url})
    driver.quit()


if __name__ == '__main__':
    # while 1:
    urls = [i['_id'] for i in client.all_post.bili_url.find({'status': 0})]
    print(len(urls))
    # if urls is None:
    #     break
    for url in urls:
        if url:
            get(url)
        # time.sleep(60)


