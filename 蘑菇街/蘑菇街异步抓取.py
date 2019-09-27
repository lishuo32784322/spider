# coding:utf-8
# author:ls
import time, datetime, json, re, os, sys, random, shutil
from pymongo import MongoClient
from selenium import webdriver
import uuid
import selenium.webdriver.support.ui as ui
from selenium.webdriver.common.by import By
import selenium.webdriver.support.expected_conditions as EC
import gevent.monkey
gevent.monkey.patch_all()
from gevent.pool import Pool
from tools.time_tool import parse_time
from selenium.common.exceptions import TimeoutException


client = MongoClient('120.131.10.99', username='root', password='BDqilingzhengfan1')
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


def get_data(url):
    try:
        while 1:
            try:
                option.add_argument(f"--proxy-server={random.choice([i['ip'] for i in client.ips.ips.find()])}")
                break
            except:
                time.sleep(0.5)
        option.add_argument(random.choice(user_agent_list))
        driver = webdriver.Chrome(chrome_options=option)
        driver.maximize_window()
        try:
            driver.get(url)
            ui.WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, '//div[@class="cp-look-detail-box "]')))
        except TimeoutException as e:
            # print(f'timeout:{url}', e)
            driver.quit()
            return None

        try:
            origin_user_id = driver.find_element_by_xpath(
                '//div[@class="cp-personalInfo clearfix cp-personalInfo-detail"]//a[1]').get_attribute('href').split(
                'uid=')[1]
        except Exception as e:
            try:
                origin_user_id = driver.find_element_by_xpath(
                    '//a[@class="block flex f-jc-c text-center pointer pos-rlt"]').get_attribute('href').split('uid=')[
                    1]
            except:
                driver.quit()
                return None
        origin_post_id = re.search('iid=(.*?)&', url).group(1)
        goods_url = '*#*#*'.join([i for i in [i.get_attribute('href') for i in driver.find_elements_by_xpath(
            '//a[@class="feed-item fl clearfix v-exposure"]')] if 'mogu' not in i])
        description = re.sub('^\n+|<a class=.*?</a>', '', driver.find_element_by_xpath('//div[contains(@class,"detail-desc-text")]').get_attribute('content')).replace('<br>', '\n')
        create_time = str(time.time()).split('.')[0]
        finish_time = parse_time(driver.find_element_by_xpath('//div[@class="flex f-ai-c fl"]/span[1]').text)
        if str(finish_time) == '0' or int(finish_time)<1567267200:
            print('pass',finish_time,url)
            client.all_post.mogujie_detail_url.update({'_id': url}, {'$set': {'status': 1}})
            driver.quit()
            return None
        modify_time = str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        upload_status = 0  # 上传状态默认0
        del_status = 0  # 删除状态默认0
        download_status = 0  # 下载状态默认0
        source = 7
        topic = ''
        tag = ''
        title = ''
        try:
            favorite = driver.find_element_by_xpath(
                '//span[@class="cp-lookDetailOperate-operate-fav flex f-ai-c pointer"]/span[2]').text
            if '万' in favorite:
                likes = int(int(favorite.split('万')[0]) * 10000)
            else:
                likes = int(favorite)
        except:
            likes = 0
        favorite = 0
        share = 0
        id = 'mogujie_' + str(origin_post_id)
        try:
            driver.find_element_by_xpath('//div[@class="play-button button pointer fl"]')
            post_type = 1
        except Exception as e:
            post_type = 0
        if post_type == 0:  # 图片贴子
            images = [i.get_attribute('src').replace('_100x999.v1c96.70.jpg', '').replace('_100x999.v1c96.70.webp', '')
                      for i in driver.find_elements_by_xpath('//div[@class="cp-look-small-image pointer"]//img')]
            while len(images) < 9:
                images.append(0)
            pic1, pic2, pic3, pic4, pic5, pic6, pic7, pic8, pic9 = images
            video = ''
        else:  # 视频贴子
            video = driver.find_element_by_xpath('//video[@class="vjs-tech"]').get_attribute('src')
            pic1, pic2, pic3, pic4, pic5, pic6, pic7, pic8, pic9 = re.search('url\("(.*?)"\);',
                                                                             driver.find_element_by_xpath(
                                                                                 '//div[@class="vjs-poster"]').get_attribute(
                                                                                 'style')).group(
                1), 0, 0, 0, 0, 0, 0, 0, 0
        if str(pic1) == '0':
            pic1 = driver.find_element_by_xpath('//div[@class="cp-lookItem"]//img').get_attribute('src')
        try:
            client.all_post.mogujie_detail_url.update({'_id': url}, {'$set': {'status': 1}})
            # print(repr(description))
            # print(repr(re.sub('^\n+', '', description)))
            client.all_post.post_data.insert(
                {'_id': id, 'title': title, 'description': re.sub('^\n+', '', description), 'topic': topic, 'tag': tag, 'pic1': pic1,
                 'pic2': pic2, 'pic3': pic3, 'pic4': pic4, 'pic5': pic5, 'pic6': pic6, 'pic7': pic7, 'pic8': pic8,
                 'pic9': pic9, 'video': video, 'type': post_type, 'finish_time': finish_time,
                 'create_time': create_time, 'modify_time': modify_time, 'source': source,
                 'upload_status': upload_status, 'del_status': del_status, 'download_status': download_status,
                 'origin_post_id': origin_post_id, 'origin_user_id': origin_user_id, 'likes': likes,
                 'share': share, 'favorite': favorite, 'goods_url': goods_url, 'export_time': 0})
            print('over')
        except Exception as e:
            print(f'key_err:{url}', e)
        try:
            client.all_user.user_info.insert(
            {'_id': origin_user_id+'_'+str(source), 'gender': 0, 'desc': '', 'create_time': create_time, 'vip': 0, 'source': source, 'export_flag': 0, 'id': origin_post_id,'user_name':origin_user_id})
        except:pass
        # print(id, title, description, topic, tag, pic1, pic2, pic3, pic4, pic5, pic6, pic7, pic8, pic9, video, post_type, create_time, finish_time, modify_time, source, upload_status, del_status, download_status, origin_post_id, origin_user_id, goods_url, favorite, likes, share)
        try:
            for i in driver.find_elements_by_class_name('comment-content'):
                comms_id = uuid.uuid1()
                client.all_comms.new_comms.insert({'_id': comms_id, 'comms_id': comms_id, 'comms_user_id': origin_user_id, 'comms_like': 0, 'comms_text': i.text, 'source': source, 'comms_time': str(int(create_time)-random.randint(100, 3000)), 'export_time': 0})
        except Exception as e:
            print(123,e)

        driver.quit()
    except:pass
    finally:
        try:
            driver.quit()
        except:pass


if __name__ == '__main__':
    pool = Pool(5)
    while 1:
        urls = [i['_id'] for i in client.all_post.mogujie_detail_url.find({'status': 0}).limit(1000)]
        print(len(urls))
        if len(urls) == 0:
            print('完事')
            break
        try:
            pool.map(get_data, urls)
        except:
            pass