# -*- coding: utf-8 -*-
import time
import sys

from common_utils import *


def checkLogin(driver):
    try:
        if (len(driver.find_elements_by_class_name("qyrv2")) == 2):
            print("登陆成功")
            return True
        else:
            return False
    except Exception:
        print("尚未登陆成功")
        # driver.find_element_by_class_name("nickname")
        return False


def login(user, pwd):
    try:
        url = "http://www.iqiyi.com/iframe/loginreg"
        driver = create_chrome(disableImage=True, mobile=False)
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
                print("账户登录...")
                driver.find_element_by_class_name("txt-account").send_keys(user)
                driver.find_element_by_class_name("txt-password").send_keys(pwd)
                driver.find_element_by_class_name("btn-login").click()
                print("提交密码...")
                time.sleep(5)
                not_connect = True
            except Exception as e:
                print(e.message)
                print("无法访问IQIY")
        count = 0
        while checkLogin(driver) == False:
            try:
                count += 1
                if count > 15:
                    break
                print("第{}次验证".format(count))
                driver.get(url)
                time.sleep(3)
                driver.find_element_by_link_text("账号密码登录").click()
                time.sleep(3)
                print("账户登录...")
                driver.find_element_by_class_name("txt-account").send_keys(user)
                driver.find_element_by_class_name("txt-password").send_keys(pwd)
                driver.find_element_by_class_name("btn-login").click()
                print("提交密码...")
                time.sleep(10)
            except Exception:
                print("无法登陆，重试")

        print("签到")
        try:
            driver.get("http://www.iqiyi.com/u/record")
            time.sleep(2)
            driver.find_element_by_class_name("vt-goldBtn").click()
            time.sleep(2)
            if driver.find_element_by_class_name("vt-grayBtn").text.find("已签到"):
                print("签到成功")
        except Exception:
            print("签到失败")

        print("抽奖")
        try:
            driver.get("http://vip.iqiyi.com/pcwlottery.html")
            time.sleep(2)

            driver.find_element_by_class_name("jackpot-prize-btn").find_element_by_tag_name("a").click()
            time.sleep(2)
            driver.switch_to_alert()
            # driver.find_element_by_class_name("btn-lt").click()
            driver.find_element_by_link_text("知道啦").click()
            time.sleep(2)
        except Exception:
            print("抽奖失败")

        print("任务")
        driver.get('http://www.iqiyi.com/u/point')
        time.sleep(3)
        driver.find_element_by_link_text("签到").click()
        time.sleep(2)
        driver.find_element_by_link_text("去逛逛").click()
        time.sleep(2)
        driver.get('http://www.iqiyi.com/u/point')
        time.sleep(3)
        driver.find_element_by_link_text("去领取").click()
        # 可通过 ActionChains move_to_element perform 触发 mouseon 事件
        # task_list = driver.find_element_by_class_name("qy-scroll-integral")
        # Hover = ActionChains(driver).move_to_element(task_list)
        # Hover.perform()

        time.sleep(20)
        print("退出")
        driver.close()
    except Exception:
        print("出错退出")
        driver.close()

if __name__ == '__main__':
    login(sys.argv[1], sys.argv[2])
