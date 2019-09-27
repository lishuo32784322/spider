# coding:utf-8
# author:ls
import time, datetime, json, re, os, sys, random, shutil, glob


path = '/Users/lishuo/Desktop/B站/'
file_list= []
def get_file(path):          #获取文件路径
    for root, dirs, files in os.walk(path):

        for file in files:
            #print(file)     #文件名
            file_list.append(os.path.join(root,file))
get_file(path)



# print(file_list, len(file_list))
for num, i in enumerate(file_list):
    if 'data7' in i:
        print(num, i)
