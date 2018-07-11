# -*- coding: utf-8 -*-
import time

import requests

from common_utils import *
import sys
import datetime

def checkLogin(driver):
    try:
        driver.find_element_by_class_name("my_header_v4_wrap")
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

        while not checkLogin(driver):
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

        # cookie = "; ".join([item["name"] + "=" + item["value"] for item in driver.get_cookies()])
        # headers = {"referer": "https://p.m.jd.com/cart/cart.action",
        #            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
        #            "cookie":cookie
        #            }
        # requests.get("https://p.m.jd.com/norder/order.action?enterOrder=true&sid=52cd54d1680bc9ce83d8d31b3a5ed2fe&ran=0.6104466918550879",headers=headers)
        driver.get("https://p.m.jd.com/cart/cart.action")
        logger.debug("访问购物车")
        time.sleep(3)
        find_element_by_id(driver, "pcprompt-viewpc")
        time.sleep(3)
        if len(driver.find_elements_by_class_name("selected")) == 0:
            find_element_by_class_name(driver, "icon_select")
            time.sleep(1)
        logger.debug("全选")
        time.sleep(1)

        date = datetime.datetime.now().strftime("%Y-%m-%d")
        buy_time_str = date + ' 09:59:58'

        buytime = time.mktime(time.strptime(buy_time_str, "%Y-%m-%d %H:%M:%S"))
        logger.debug(buytime)
        while (time.time() < buytime):
            time.sleep(0.01)
        find_element_by_class_name(driver, "buyJs")
        time.sleep(0.35)
        if find_element_by_id(driver, "pcprompt-viewpc"):
            time.sleep(0.1)
        find_element_by_link_text(driver, "在线支付")
        time.sleep(15)
    except Exception as e:
        logger.exception("出错退出")
        driver.close()


if __name__ == '__main__':
    login(sys.argv[1], sys.argv[2])
