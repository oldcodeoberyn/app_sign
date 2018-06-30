# -*- coding: utf-8 -*-
import time
from common_utils import *
import sys

# todo 京东金融 每日签到，早起活动，双签
# 翻牌 https://active.jd.com/forever/stockSign/html/index.html
# 钢镚 https://coin.jd.com/m/gb/index.html
# 每日签到 https://m.jr.jd.com/vip/sign/html/index.html
# 早起活动， https://m.jr.jd.com/integrate/getUp/html/index.html

def checkLogin(driver):
    try:
        driver.find_element_by_class_name("nickname")
        print("登陆成功")
        return True
    except Exception:
        print("尚未登陆成功")
        # driver.find_element_by_class_name("nickname")
        return False

def login(userName, password):
    driver = create_chrome( disableImage=False, mobile=True)
    # TODO, 有时登陆会跳转到linkstar.com，导致异常退出
    url = "https://home.m.jd.com/myJd/home.action"
    authcode_img = 'out.png'

    not_connect = False
    while not_connect == False:
        try:
            driver.get(url)
            time.sleep(2)
            print("账户登录...")
            driver.find_element_by_id("username").send_keys(userName)
            driver.find_element_by_id("password").send_keys(password)
            driver.find_element_by_id("loginBtn").click()
            print("提交密码...")
            time.sleep(5)
            not_connect = True
        except Exception:
            print("无法访问JD")

    driver.get("https://vip.m.jd.com/")

    driver.get("https://s.m.jd.com/activemcenter/activemsite/m_welfare?ptag=138026.5.1&sceneval=2&logintag=#/main")
    time.sleep(3)
    driver.find_element_by_class_name("day_able").click()
    print("签到，并领取京豆")
    time.sleep(2)
    print("抽奖")
    driver.find_element_by_class_name("lottery_btn").click()
    time.sleep(2)
    tasks = driver.find_elements_by_class_name("welfareTask_btn")

    print("领取任务")
    for task in tasks:
        task.click()
        time.sleep(2)
        driver.get("https://s.m.jd.com/activemcenter/activemsite/m_welfare?ptag=138026.5.1&sceneval=2&logintag=#/main")
        time.sleep(2)

    print("领取京豆")
    for task in tasks:
        task.click()
        time.sleep(2)

    print("早起签到")
    driver.get("https://m.jr.jd.com/integrate/getUp/html/index.html")
    time.sleep(2)
    driver.get("https://m.jr.jd.com/vip/sign/html/index.html")
    time.sleep(2)
    driver.find_element_by_class_name("sign-btn").click()
    time.sleep(2)
    driver.get("https://coin.jd.com/m/gb/index.html")


    time.sleep(100)
    driver.close()


if __name__ == '__main__':
    login(sys.argv[1], sys.argv[2])
