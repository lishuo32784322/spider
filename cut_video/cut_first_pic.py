# coding:utf-8
# author:ls
import time, datetime, json, re, os, sys, random, shutil
import cv2
import os


def mov2img():
    vc = cv2.VideoCapture('1.mp4')  # 读入视频文件
    if vc.isOpened():  # 判断是否正常打开
        rval, frame = vc.read()
        print(frame)
        cv2.imwrite('1.jpg', frame)  # 存储为图像
    else:
        rval = False


mov2img()
