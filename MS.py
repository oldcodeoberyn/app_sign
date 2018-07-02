# -*- coding: utf-8 -*-
import time
from common_utils import *
import sys


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
        driver.get("https://p.m.jd.com/cart/cart.action")
        print("访问购物车")
        time.sleep(3)
        driver.find_element_by_id("pcprompt-viewpc").click()
        print("直接操作")
        time.sleep(3)
        if len(driver.find_elements_by_class_name("selected")) == 0:
            driver.find_element_by_class_name("icon_select").click()
            time.sleep(1)
        print("全选")



        buy_time_str = '2018-07-02 20:00:00'
        buytime = time.mktime(time.strptime(buy_time_str,"%Y-%m-%d %H:%M:%S"))
        print( buytime )
        while(time.time() < buytime):
            time.sleep(0.01)
        driver.find_element_by_class_name("buyJs").click()
        print("下单")
        time.sleep(0.5)
        driver.find_element_by_id("pcprompt-viewpc").click()
        print("直接操作")
        time.sleep(0.5)
        driver.find_element_by_link_text("在线支付").click()
        time.sleep(15)
    except Exception as e:
        logger.exception("出错退出")
        driver.close()


if __name__ == '__main__':
    login(sys.argv[1], sys.argv[2])


