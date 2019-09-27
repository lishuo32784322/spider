from appium import webdriver
import selenium.webdriver.support.ui as ui
from selenium.webdriver.common.by import By
import selenium.webdriver.support.expected_conditions as EC
from selenium.webdriver.common.touch_actions import TouchActions
import time


desired_caps = {}
# 小红书
# desired_caps['platformName'] = 'Android'
# desired_caps['platformVersion'] = '9'
# desired_caps['deviceName'] = 'S2D0218928005270'
# desired_caps['appPackage'] = 'com.xingin.xhs'
# desired_caps['appActivity'] = 'com.xingin.xhs.activity.SplashActivity'

# 淘宝
desired_caps['platformName'] = 'Android'
desired_caps['platformVersion'] = '9'
desired_caps['deviceName'] = 'NEX'
desired_caps['udid'] = '28ce91bf'
desired_caps['appPackage'] = 'com.taobao.taobao'
desired_caps['appActivity'] = 'com.taobao.tao.TBMainActivity'
desired_caps['noReset'] = 'true'

driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
Action = TouchActions(driver)

ui.WebDriverWait(driver, 3).until(EC.visibility_of_element_located((By.XPATH, '//hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup/android.support.v7.widget.RecyclerView/android.widget.FrameLayout[4]/android.widget.FrameLayout/android.widget.ImageView[24]')))
driver.find_element_by_xpath('//hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup/android.support.v7.widget.RecyclerView/android.widget.FrameLayout[4]/android.widget.FrameLayout/android.widget.ImageView[24]').click()

while 1:
    try:
        ui.WebDriverWait(driver, 3).until(EC.visibility_of_element_located((By.XPATH, '//android.view.View[@content-desc="时髦穿搭"]')))
        break
    except:
        driver.swipe(1000, 300, 50, 300, 100)
driver.find_element_by_xpath('//android.view.View[@content-desc="时髦穿搭"]').click()
ele = driver.find_element_by_class_name('android.widget.FrameLayout')
print(ele.text)
print(ele.__doc__)
print(ele.__repr__())
print(ele.__dict__)

# driver.quit()






def getSize():  # 获取当前的width和height的x、y的值
    x = driver.get_window_size()['width']   #width为x坐标
    y = driver.get_window_size()['height']  #height为y坐标
    return (x, y)


def swipeUp(t):  #当前向上滑动swipeup
    l = getSize()
    x1 = int(l[0] * 0.5)
    y1 = int(l[1] * 0.75)
    y2 = int(l[1] * 0.25)
    driver.swipe(x1, y1, x1, y2,500)  #设置时间为500


def swipLeft(t):  #当前向左进行滑动swipleft
    l = getSize()
    x1 = int(l[0]*0.75)
    y1 = int(l[1]*0.5)
    x2 = int(l[0]*0.05)
    driver.swipe(x1, y1, x2, y1, 500)


def swipeDown(t):  #向下滑动swipedown
    l = getSize()
    x1 = int(l[0] * 0.5)
    y1 = int(l[1] * 0.25)
    y2 = int(l[1] * 0.75)
    driver.swipe(x1, y1, x1, y2,500)


def swipRight(t):  #向右滑行swipright
    l = getSize()
    x1 = int(l[0]*0.05)
    y1 = int(l[1]*0.5)
    x2 = int(l[0]*0.75)
    driver.swipe(x1, y1, x2, y1, 500)
