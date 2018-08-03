# -*- coding: utf-8 -*-
import time

import requests

from common_utils import *
import sys
import datetime
import time


# todo 京东金融 每日签到，早起活动，双签
# 翻牌 https://active.jd.com/forever/stockSign/html/index.html
# 钢镚 https://coin.jd.com/m/gb/index.html
# 每日签到 https://m.jr.jd.com/vip/sign/html/index.html
# 早起活动， https://m.jr.jd.com/integrate/getUp/html/index.html

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
                logger.debug("无法访问JD")

        # 京豆乐园
        driver.get("https://union-click.jd.com/jdc?d=oDyb0D")
        time.sleep(2)
        driver.get(
            'https://ms.jr.jd.com/jrmserver/base/user/getNewTokenJumpUrl?accessKey=14a143c5-3ff4-40f0-b65c-dc39ab5483be&pin=54K554Gr5LiJ5ZGo&deviceId=008796756085172&clientType=android&a2=AAFbXoZ3AECIb95oHj7QugQF2vU-c1kWNVYdjPAvKdXpxNlqVk3BxURFVUrt2tq0_7-naO9l5LoSS1oPbuaz0_uOo_oDlVUx&sign=05e5b556b2600e15ed4dbc95cfefe6c0&targetUrl=aHR0cHM6Ly9tLmpyLmpkLmNvbS92aXAvc2lnbi9odG1sL2luZGV4Lmh0bWw%3D')
        time.sleep(2)
        headers = config_header(driver, "https://ms.jr.jd.com/")
        resp = requests.post(url="https://ms.jr.jd.com/gw/generic/hy/h5/m/signIn?_={}".format(
                int(time.time() * 1000)), verify=False, headers = headers, data={"reqData":'{"channelSource":"JRAPP"}'})
        print(resp.text)
        logger.info("领取钢镚成功")
        driver.get("https://bean.m.jd.com/")
        time.sleep(2)

        for span in driver.find_elements_by_tag_name("span"):
            if span.text == "签到领京豆":
                span.click()
                break
        logger.info("移动端签到成功")

        headers = config_header(driver, "https://bean.m.jd.com/")

        resp = requests.get(
            'https://api.m.jd.com/client.action?functionId=getCardResult&body=%7B%22index%22%3A5%2C%22rnVersion%22%3A%224.0%22%2C%22fp%22%3A%22-1%22%2C%22shshshfp%22%3A%22-1%22%2C%22shshshfpa%22%3A%22-1%22%2C%22referUrl%22%3A%22-1%22%2C%22userAgent%22%3A%22-1%22%2C%22jda%22%3A%22-1%22%7D&appid=ld&client=android&clientVersion=&networkType=&osVersion=&uuid=&jsonp=jsonp_jsonp_{}_388'.format(
                int(time.time() * 1000)), verify=False, headers=headers)
        print(resp.text)
        logger.info("移动端翻牌成功")
        time.sleep(2)

        # driver.get("https://ljd.m.jd.com/countersign/index.action")
        # time.sleep(2)
        # driver.find_element_by_class_name("gift-dialog-btn").click()
        # time.sleep(2)

        driver.get("https://vip.m.jd.com/")
        time.sleep(2)
        find_element_by_class_name(driver, "sign-pop")
        time.sleep(2)

        driver.get("https://s.m.jd.com/activemcenter/activemsite/m_welfare?ptag=138026.5.1&sceneval=2&logintag=#/main")
        time.sleep(3)
        find_element_by_id(driver, "pcprompt-viewpc")
        time.sleep(2)
        find_element_by_class_name(driver, "day_able")
        logger.debug("签到，并领取京豆")
        time.sleep(2)
        driver.get("https://s.m.jd.com/activemcenter/activemsite/m_welfare?ptag=138026.5.1&sceneval=2&logintag=#/main")
        time.sleep(3)
        find_element_by_id(driver, "pcprompt-viewpc")
        time.sleep(2)
        logger.debug("抽奖")
        find_element_by_class_name(driver, "lottery_btn")
        time.sleep(2)
        driver.get("https://s.m.jd.com/activemcenter/activemsite/m_welfare?ptag=138026.5.1&sceneval=2&logintag=#/main")
        time.sleep(3)
        find_element_by_id(driver, "pcprompt-viewpc")
        time.sleep(2)
        tasks = driver.find_elements_by_class_name("welfareTask_btn")

        logger.debug("领取任务")
        for task in tasks:
            task.click()
            time.sleep(2)
            driver.get(
                    "https://s.m.jd.com/activemcenter/activemsite/m_welfare?ptag=138026.5.1&sceneval=2&logintag=#/main")
            time.sleep(2)

        logger.debug("领取京豆")
        for task in tasks:
            task.click()
            time.sleep(2)

        driver.get("https://m.jr.jd.com/vip/sign/html/index.html")
        time.sleep(2)
        find_element_by_class_name(driver, "sign-btn")
        time.sleep(2)

        logger.debug("早起签到")
        driver.get("https://m.jr.jd.com/integrate/getUp/html/index.html")
        time.sleep(2)
        find_element_by_class_name(driver, "clockBtn")
        time.sleep(2)
        find_element_by_class_name(driver, "mt58")

        time.sleep(100)
        driver.close()
    except Exception as e:
        logger.exception("出错退出")
        driver.close()


if __name__ == '__main__':
    login(sys.argv[1], sys.argv[2])
