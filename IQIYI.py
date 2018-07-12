# -*- coding: utf-8 -*-
import time
import sys
import re

from common_utils import *


def checkLogin(driver):
    try:
        if (len(driver.find_elements_by_class_name("vt-user-nickname")) > 0):
            logger.debug("登陆成功")
            return True
        else:
            return False
    except Exception:
        logger.debug("尚未登陆成功")
        # driver.find_element_by_class_name("nickname")
        return False


def login(user, pwd):
    try:
        url = "http://www.iqiyi.com/iframe/loginreg"
        driver = create_chrome(disableImage=False, mobile=False)
        not_connect = False
        while not_connect == False:
            try:
                driver.get(url)
                time.sleep(3)
                # 直接通过跳转后的Loginreg url登陆
                # time.sleep(5)
                # driver.find_element_by_link_text("登录").click()
                # time.sleep(3)
                # driver.switch_to_active_element()
                driver.find_element_by_link_text("账号密码登录").click()
                time.sleep(3)
                logger.debug("账户登录...")
                driver.find_element_by_class_name("txt-account").send_keys(user)
                driver.find_element_by_class_name("txt-password").send_keys(pwd)

                driver.delete_all_cookies()
                with open("cookie") as f:
                    cookie_str = f.readline()
                    cookies = cookie_str.split(";")
                    for c in cookies:
                        cookie = {}
                        cookie['name'] = c.split('=')[0].strip()
                        cookie['value'] = c.split('=')[1].strip()
                        driver.add_cookie(cookie)
                driver.refresh()
                # driver.find_element_by_class_name("btn-login").click()
                # logger.debug("提交密码...")
                time.sleep(5)
                not_connect = True
            except Exception as e:
                logger.debug(e.message)
                logger.debug("无法访问IQIY")
        count = 0
        while checkLogin(driver) == False:
            try:
                count += 1
                if count > 15:
                    break
                logger.debug("第{}次验证".format(count))
                driver.get(url)
                time.sleep(3)
                driver.find_element_by_link_text("账号密码登录").click()
                time.sleep(3)
                logger.debug("账户登录...")
                driver.find_element_by_class_name("txt-account").send_keys(user)
                driver.find_element_by_class_name("txt-password").send_keys(pwd)
                driver.find_element_by_class_name("btn-login").click()
                logger.debug("提交密码...")
                time.sleep(10)
            except Exception:
                logger.debug("无法登陆，重试")

        logger.debug("签到")
        try:
            driver.get("http://www.iqiyi.com/u/record")
            time.sleep(2)
            driver.find_element_by_class_name("vt-goldBtn").click()
            time.sleep(2)
            if driver.find_element_by_class_name("vt-grayBtn").text.find("已签到"):
                logger.debug("签到成功")
        except Exception:
            logger.debug("签到失败")

        logger.debug("抽奖")
        try:
            driver.get("http://vip.iqiyi.com/pcwlottery.html")
            time.sleep(2)

            l_times_str = driver.find_element_by_class_name("head-lt").text
            logger.debug(l_times_str)
            s = re.search('\d', l_times_str)
            l_times = 0
            if s:
                l_times = int(s.group())
            for i in range(l_times):
                driver.find_element_by_class_name("jackpot-prize-btn").find_element_by_tag_name("a").click()
                time.sleep(5)
                driver.get("http://vip.iqiyi.com/pcwlottery.html")
                time.sleep(2)
        except Exception:
            logger.Exception("抽奖失败")
        time.sleep(3)
        logger.debug("任务")
        driver.get('http://www.iqiyi.com/u/point')
        time.sleep(3)
        find_element_by_link_text(driver,"签到")
        time.sleep(2)
        find_element_by_link_text(driver,"去逛逛")
        time.sleep(2)
        driver.get('http://www.iqiyi.com/u/point')
        time.sleep(3)
        find_element_by_link_text(driver,"去领取")
        # 可通过 ActionChains move_to_element perform 触发 mouseon 事件
        # task_list = driver.find_element_by_class_name("qy-scroll-integral")
        # Hover = ActionChains(driver).move_to_element(task_list)
        # Hover.perform()

        time.sleep(20)
        logger.debug("退出")
        driver.close()
    except Exception:
        logger.exception("出错退出")
        driver.close()

if __name__ == '__main__':
    login(sys.argv[1], sys.argv[2])
