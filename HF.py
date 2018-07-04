# -*- coding: utf-8 -*-
import time

import requests

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

        driver.get("https://sale.jd.com/m/act/8Ak3ilHTvYR7.html")
        time.sleep(2)

        date = datetime.datetime.now().strftime("%Y-%m-%d")

        buy_time_str = date + ' 09:59:59'
        buytime_10 = time.mktime(time.strptime(buy_time_str, "%Y-%m-%d %H:%M:%S"))

        buy_time_str = date + ' 11:59:59'
        buytime_12 = time.mktime(time.strptime(buy_time_str, "%Y-%m-%d %H:%M:%S"))

        buy_time_str = date + ' 13:59:59'
        buytime_14 = time.mktime(time.strptime(buy_time_str, "%Y-%m-%d %H:%M:%S"))

        buy_time_str = date + ' 17:59:59'
        buytime_18 = time.mktime(time.strptime(buy_time_str, "%Y-%m-%d %H:%M:%S"))

        buy_time_str = date + ' 19:59:59'
        buytime_20 = time.mktime(time.strptime(buy_time_str, "%Y-%m-%d %H:%M:%S"))

        if time.time() < buytime_12:
            buytime = buytime_12
        elif time.time() < buytime_14:
            buytime = buytime_14
        elif time.time() < buytime_18:
            buytime = buytime_18
        else:
            buytime = buytime_20

        logger.debug("准备抢购")
        cookie = "; ".join([item["name"] + "=" + item["value"] for item in driver.get_cookies()])
        headers = {"referer": "https://sale.jd.com/m/act/8Ak3ilHTvYR7.html",
                   "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
                   "cookie":cookie
                   }
        logger.debug(headers)
        while time.time() < buytime + 0.8:
            time.sleep(0.1)
        while time.time() > buytime + 0.8 and time.time() < buytime:
            time.sleep(0.025)
            resp = requests.get(
                "http://act-jshop.jd.com/couponSend.html?ruleId=12816307&key=9e2c507aa97c43f9a9dad267bbd4bb40&sid=df194dd9015d61b069c80548c75a8527&eid=63MC7EDDUH3243MORQ6DB7M4DE5MRVJBHY45TJTOLUBLHKPV7ZM5K7NODMX23BJDXO5D3PO4WJDNP3CLSH23KQ4LHY&fp=a5cfd575a431a5c829b88a9062947ac4&shshshfp=a5b45026da1ec74832d172380fe4983e&shshshfpa=aa869845-629a-d170-0163-904170f09f1d-1530679125&shshshfpb=0dc613037052c5423615861c74482464d9908091518dc06c55b3446a37&jda=122270672.15301079406641749654337.1530107941.1530678243.1530684086.21&pageClickKey=-1&platform=3&applicationId=983467&_=1530684192499&callback=Zepto1530684165390",headers=headers)
            logger.debug(resp.text)

        resp = requests.get(
            "http://act-jshop.jd.com/couponSend.html?ruleId=12816307&key=9e2c507aa97c43f9a9dad267bbd4bb40&sid=df194dd9015d61b069c80548c75a8527&eid=63MC7EDDUH3243MORQ6DB7M4DE5MRVJBHY45TJTOLUBLHKPV7ZM5K7NODMX23BJDXO5D3PO4WJDNP3CLSH23KQ4LHY&fp=a5cfd575a431a5c829b88a9062947ac4&shshshfp=a5b45026da1ec74832d172380fe4983e&shshshfpa=aa869845-629a-d170-0163-904170f09f1d-1530679125&shshshfpb=0dc613037052c5423615861c74482464d9908091518dc06c55b3446a37&jda=122270672.15301079406641749654337.1530107941.1530678243.1530684086.21&pageClickKey=-1&platform=3&applicationId=983467&_=1530684192499&callback=Zepto1530684165390",headers=headers)
        logger.debug(resp.text)
        resp = requests.get(
            "http://act-jshop.jd.com/couponSend.html?ruleId=12816308&key=9e2c507aa97c43f9a9dad267bbd4bb40&sid=df194dd9015d61b069c80548c75a8527&eid=63MC7EDDUH3243MORQ6DB7M4DE5MRVJBHY45TJTOLUBLHKPV7ZM5K7NODMX23BJDXO5D3PO4WJDNP3CLSH23KQ4LHY&fp=a5cfd575a431a5c829b88a9062947ac4&shshshfp=a5b45026da1ec74832d172380fe4983e&shshshfpa=aa869845-629a-d170-0163-904170f09f1d-1530679125&shshshfpb=0dc613037052c5423615861c74482464d9908091518dc06c55b3446a37&jda=122270672.15301079406641749654337.1530107941.1530678243.1530684086.21&pageClickKey=-1&platform=3&applicationId=983467&_=1530684192499&callback=Zepto1530684165390",headers=headers)
        logger.debug(resp.text)
        driver.get("https://sale.jd.com/m/act/8Ak3ilHTvYR7.html")
        time.sleep(0.3)
        try:
            logger.debug("按按钮")
            driver.find_elements_by_class_name("coup-img")[0].click()
        except Exception:
            logger.exception("按钮没找到")
        logger.debug("再抢")
        driver.get("https://sale.jd.com/m/act/8Ak3ilHTvYR7.html")
        time.sleep(0.2)
        try:
            logger.debug("按按钮")
            driver.find_elements_by_class_name("coup-img")[1].click()
        except Exception:
            logger.exception("按钮没找到")
        time.sleep(20)
    except Exception as e:
        logger.exception("出错退出")
        driver.close()


if __name__ == '__main__':
    login(sys.argv[1], sys.argv[2])
