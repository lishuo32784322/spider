# coding:utf-8
# author:ls
import time, datetime, json, re, os, sys, random, shutil
from PIL import Image, ImageChops


def equal(im1, im2):
    return ImageChops.difference(im1, im2).getbbox() is None

def testWaterMarking (pic , mark):
    # 预处理
    img = Image.open(pic).convert("RGB")
    width, height = img.size   # 读取大小

    img_mark = Image.open(mark).convert("RGB")
    img_mark = img_mark.resize((width, height)) #缩放水印到文件大小

    img_pixels = list(img.getdata())
    # print img_pixels[:10]
    # 提取出来的水印
    img_get = img.point(lambda i: (int(i&3))*85)
    # img_get.show()
    # 正常应该得到的水印
    img_mark = img_mark.point(lambda i: round(i/85)*85)
    print(equal(img_get,img_mark))

    return equal(img_get,img_mark)

if __name__ == '__main__':
    print(testWaterMarking('t7.png', 'm4.png'))
