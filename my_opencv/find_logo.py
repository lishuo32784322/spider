# coding:utf-8
# author:ls
import time, datetime, json, re, os, sys, random, shutil
import pytesseract
from PIL import Image
from PIL import ImageFilter
from PIL import ImageFont
from PIL import ImageDraw
import numpy as np
from PIL import Image

import cv2


def main():
    # 使用模板匹配在图像中寻找物体
    # OpenCV函数：cv2.matchTemplate(), cv2.minMaxLoc()
    # 模板匹配就是用来在大图中找小图，也就是说在一副图像中寻找另外一张模板图像的位置

    #  =================================模板匹配
    img = cv2.imread('/Users/lishuo/spider/workspace/my_opencv/t7.png', 0)
    template = cv2.imread('/Users/lishuo/spider/workspace/my_opencv/m3.png', 0)
    h, w = template.shape[:2]  # rows->h, cols->w
    print("h = ", h)
    print("w = ", w)

    # 相关系数匹配方法：cv2.TM_CCOEFF
    res = cv2.matchTemplate(img, template, cv2.TM_CCOEFF)

    # 平方差匹配CV_TM_SQDIFF：用两者的平方差来匹配，最好的匹配值为0
    # 归一化平方差匹配CV_TM_SQDIFF_NORMED
    # 相关匹配CV_TM_CCORR：用两者的乘积匹配，数值越大表明匹配程度越好
    # 归一化相关匹配CV_TM_CCORR_NORMED
    # 相关系数匹配CV_TM_CCOEFF：用两者的相关系数匹配，1
    # 表示完美的匹配，-1
    # 表示最差的匹配
    # 归一化相关系数匹配CV_TM_CCOEFF_NORMED

    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    # cv2.minMaxLoc()函数可以得到最大匹配值的坐标，以这个点为左上角角点，模板的宽和高画矩形就是匹配的位置了
    print("min_val = ", min_val)
    print("max_val = ", max_val)  # 最大匹配值
    print("min_loc = ", min_loc)
    print("max_loc = ", max_loc)  # 最大左上角坐标

    left_top = max_loc  # 左上角
    right_bottom = (left_top[0] + w, left_top[1] + h)  # 右下角
    cv2.rectangle(img, left_top, right_bottom, 255, 2)  # 画出矩形位置

    cv2.imshow('img', img)
    cv2.waitKey(0)


if __name__ == '__main__':
    main()