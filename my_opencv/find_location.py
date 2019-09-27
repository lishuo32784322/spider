# coding:utf-8
# author:ls
import time, datetime, json, re, os, sys, random, shutil
import cv2
import numpy as np
from matplotlib import pyplot as plt

def find(big_path, small_path):
    max_value = []
    img = cv2.imread(big_path, 0)
    img2 = img.copy()
    template = cv2.imread(small_path, 0)
    w, h = template.shape[::-1]
    # 所有的匹配方法
    methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR',
               'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']
    for meth in methods:
        img = img2.copy()
        method = eval(meth)  # 去掉字符串的引号
        # 匹配
        res = cv2.matchTemplate(img, template, method)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        # 使用不同的比较方法，对结果的解释不同
        # 如果方法是 TM_SQDIFF or TM_SQDIFF_NORMED, 取最小值
        if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
            top_left = min_loc
        else:
            top_left = max_loc
        bottom_right = (top_left[0] + w, top_left[1] + h)

        cv2.rectangle(img, top_left, bottom_right, 255, 2)

        plt.subplot(121), plt.imshow(res, cmap='gray'),
        plt.title('Matching Result'), plt.axis('off')
        plt.subplot(122), plt.imshow(img, cmap='gray'),
        plt.title('Detected Point'), plt.axis('off')
        plt.suptitle(meth)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(img)
        max_value.append(max_loc)
        # print(min_val, max_val, min_loc, max_loc)
        plt.show()
        # print(max_loc)
    return max(max_value, key=max_value.count)


count = 1
# while count <= 66:
print(find(f'/Users/lishuo/spider/workspace/b_video/pics/{1}.jpg', '/Users/lishuo/spider/workspace/my_opencv/m4.png'))







