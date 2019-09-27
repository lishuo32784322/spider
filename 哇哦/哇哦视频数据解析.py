import os
import json
import re
import time
from pymongo import MongoClient


client = MongoClient('120.92.49.240', username='root', password='BDqilingzhengfan1')


def wao_data(path):
    for i, j, k in os.walk(path):
        for l in k:
            with open(path+'/'+l, 'r') as f:
                try:
                    txt = f.read()
                except:continue
                try:
                    info = re.search('"order":.*?,"result":{"data":(.*?),"attrs":', txt).group(1)
                    vip = 1 if re.search('("v":.*?)', info).group(1) == 'true' else 0
                    user_id = re.search('"accountId":(.*?),', info).group(1)
                    client.all_user.user_info1.save({'_id': user_id, 'vip': vip, 'source': 6, 'created_time': str(time.time()).split('.')[0], 'gender': 0, 'desc': ''})
                except Exception as e:pass
                # print(txt)
                # print('*' * 100)
                datas = re.findall('({"bizType":.*?\.mp4"})', txt)
                for data in datas:
                    # print(data)
                    try:
                        df = json.loads(data)
                    except:continue
                    id = 'wao'+str(df['feedId'])
                    title = df['title']
                    description = df['content']
                    topic = ''
                    tag = ','.join([i for i in df['tags']])
                    pic1 = 'http:'+df['images'][0]
                    video = 'http://'+df['videoUrl']
                    post_type = 1
                    create_time = str(time.time()).split('.')[0]
                    finish_time = str(df['publishTime'])[:-3]
                    modify_time = str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
                    source = 6
                    upload_status = 0  # 上传状态默认0
                    del_status = 0  # 删除状态默认0
                    download_status = 0  # 下载状态默认0
                    likes = df['feedCount']['praiseCount']
                    share = 0
                    favorite = 0
                    origin_post_id = str(df['feedId'])
                    origin_user_id = str(df['userId'])
                    if int(finish_time) < 1554048000:
                        continue
                    try:
                        itemId = '*#*#*'.join(['https://detail.tmall.com/item.htm?id=' + i['itemId'] for i in df['items']])
                    except:itemId = ''
                    try:

                        client.all_post.post_data.insert(
                            {'_id': id, 'title': title, 'description': description, 'topic1': topic, 'tag': tag, 'pic1': pic1,
                             'pic2': 0, 'pic3': 0, 'pic4': 0, 'pic5': 0, 'pic6': 0, 'pic7': 0, 'pic8': 0,
                             'pic9': 0, 'video': video, 'type': post_type, 'finish_time': finish_time,
                             'create_time': create_time, 'modify_time': modify_time, 'source': source,
                             'upload_status': upload_status, 'del_status': del_status, 'download_status': download_status,
                             'origin_post_id': origin_post_id, 'origin_user_id': origin_user_id, 'likes': likes,
                             'share': share, 'favorite': favorite, 'goods_url': itemId})
                    except Exception as e:
                        print(e)






if __name__ == '__main__':
    # wao_data('/Users/lishuo/spider/workspace/哇哦/1')
    wao_data('/Users/lishuo/spider/workspace/哇哦/2')
    # for i in wao_data('/Users/lishuo/spider/workspace/哇哦/data/'):
    #     id = i['feedId']
    #     title = i['title']
    #     description = i['content']
    #     topic1 = i['topics']  # 待验证
    #     tag = i['tag']  # 待验证
    #     post_type = 1
