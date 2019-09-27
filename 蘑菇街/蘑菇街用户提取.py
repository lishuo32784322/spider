# coding:utf-8
# author:ls
import time, datetime, json, re, os, sys, random, shutil
import pymongo


client = pymongo.MongoClient('120.131.10.99', port=27017, username='root', password='BDqilingzhengfan1')


def get_user(path):
    for i, j, k in os.walk(path):
        for l in k:
            with open(path + '/' + l, 'r') as f:
                # print(f.read())
                for i in set(re.findall('"userId":"(.*?)"|\\\\"userId\\\\":\\\\"(.*?)\\\\"', f.read())):
                    try:
                        if isinstance(i, tuple):
                            i = str(i[1])
                            print(i,1)
                            client.all_post.mogujie_user.save({'_id': 'https://pc.mogu.com/content/personal/' + str(i), 'status': 0})
                            client.all_user.user_info.insert({'_id': i+'_'+str(7), 'gender': 0, 'desc': '', 'create_time': str(time.time()).split('.')[0], 'vip': 0, 'source': 7, 'export_flag': 0, 'id': i,'user_name':i})
                        else:
                            print(i,2)
                            break
                            client.all_user.user_info.insert({'_id': i+'_'+str(7), 'gender': 0, 'desc': '', 'create_time': str(time.time()).split('.')[0], 'vip': 0, 'source': 7, 'export_flag': 0, 'id': i})
                            client.all_post.mogujie_user.save({'_id': 'https://pc.mogu.com/content/personal/'+str(i),'status': 0})
                    except Exception as e:print(e)

if __name__ == '__main__':
    get_user('/Users/lishuo/spider/workspace/蘑菇街/data')
