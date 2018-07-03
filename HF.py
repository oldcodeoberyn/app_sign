# -*- coding: utf-8 -*-
import time
from common_utils import *
import sys
import datetime


def checkLogin(driver):
    try:
        driver.find_element_by_class_name("nickname")
        logger.debug("登陆成功")
        return True
    except Exception:
        logger.debug("尚未登陆成功")
        # driver.find_element_by_class_name("nickname")
        return False


def login(userName, password):
    try:
        driver = create_chrome(disableImage=False, mobile=False)
        # TODO, 有时登陆会跳转到linkstar.com，导致异常退出
        url = "https://home.m.jd.com/myJd/home.action"
        authcode_img = 'out.png'

        not_connect = False
        while not_connect == False:
            try:
                driver.get(url)
                time.sleep(2)
                logger.debug("账户登录...")
                driver.find_element_by_id("username").send_keys(userName)
                driver.find_element_by_id("password").send_keys(password)
                driver.find_element_by_id("loginBtn").click()
                logger.debug("提交密码...")
                time.sleep(5)
                not_connect = True
            except Exception:
                logger.exception("无法访问JD")


        date = datetime.datetime.now().strftime("%Y-%m-%d")
        buy_time_str = date + ' 11:59:58'
        buytime_12 = time.mktime(time.strptime(buy_time_str,"%Y-%m-%d %H:%M:%S"))

        buy_time_str = date + ' 13:59:58'
        buytime_14 = time.mktime(time.strptime(buy_time_str,"%Y-%m-%d %H:%M:%S"))

        buy_time_str = date + ' 17:59:58'
        buytime_18 = time.mktime(time.strptime(buy_time_str,"%Y-%m-%d %H:%M:%S"))

        buy_time_str = date + ' 19:59:58'
        buytime_20 = time.mktime(time.strptime(buy_time_str,"%Y-%m-%d %H:%M:%S"))

        if time.time() < buytime_12:
            buytime = buytime_12
        elif  time.time() < buytime_14:
            buytime = buytime_14
        elif  time.time() < buytime_18:
            buytime = buytime_18
        else:
            buytime = buytime_20

        logger.debug( datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "准备抢购" )
        while(time.time() < buytime):
            time.sleep(0.01)
        driver.get("https://sale.jd.com/m/act/8Ak3ilHTvYR7.html")
        time.sleep(0.5)
        try:
            driver.find_elements_by_class_name("coup-img")[0].click()
        except Exception:
            logger.exception("按钮没找到")
        driver.get("https://sale.jd.com/m/act/8Ak3ilHTvYR7.html")
        time.sleep(0.2)
        driver.find_elements_by_class_name("coup-img")[0].click()
        try:
            driver.find_elements_by_class_name("coup-img")[0].click()
        except Exception:
            logger.exception("按钮没找到")
        time.sleep(20)
    except Exception as e:
        logger.exception("出错退出")
        driver.close()


if __name__ == '__main__':
    login(sys.argv[1], sys.argv[2])


