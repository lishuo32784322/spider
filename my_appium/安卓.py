# coding:utf-8
# author:ls
import time, datetime, json, re, os, sys, random, shutil
import unittest
import selenium
import time
from appium import webdriver
import selenium.webdriver.support.ui as ui
from selenium.webdriver.common.by import By
import selenium.webdriver.support.expected_conditions as EC
from selenium.webdriver.common.touch_actions import TouchActions
import time


# 淘宝
desired_caps = {}
desired_caps['platformName'] = 'Android'
desired_caps['platformVersion'] = '9'
desired_caps['deviceName'] = 'NEX'
desired_caps['udid'] = '28ce91bf'
desired_caps['appPackage'] = 'com.taobao.taobao'
desired_caps['appActivity'] = 'com.taobao.tao.TBMainActivity'
desired_caps['noReset'] = 'true'

driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
Action = TouchActions(driver)
driver.find_element_by_xpath('/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.TextView[2]').click()
driver.find_element_by_xpath('	/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.FrameLayout[2]/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.LinearLayout/android.widget.EditText').send_keys('李大神')
driver.find_element_by_xpath('//android.widget.Button[@content-desc="搜索"]').click()

driver.quit()