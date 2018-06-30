# -*- coding: utf-8 -*-
import time
import requests
import cv2
import numpy as np
from common_utils import *




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
    driver = create_chrome()
    # TODO, 有时登陆会跳转到linkstar.com，导致异常退出
    url = "http://www.jd.com"
    authcode_img = 'out.png'

    not_connect = False
    while not_connect == False:
        try:
            driver.get(url)
            time.sleep(2)
            driver.find_element_by_link_text("你好，请登录").click()
            time.sleep(3)
            driver.find_element_by_link_text("账户登录").click()
            print("账户登录...")
            driver.find_element_by_name("loginname").send_keys(userName)
            driver.find_element_by_name("nloginpwd").send_keys(password)
            driver.find_element_by_id("loginsubmit").click()
            print("提交密码...")
            time.sleep(5)
            not_connect = True
        except Exception:
            print("无法访问JD")

    count = 0
    while checkLogin(driver) == False:
        try:
            count += 1
            if count > 15:
                break
            print("第", count, "次验证")

            # 如果需要通过截屏的方法处理验证码，则需要获取整个html的大小，然后将screenshot图片resize为html的大小
            # html = driver.find_element_by_tag_name('html')
            element = driver.find_element_by_id('JD_Verification1')
            element.click()
            time.sleep(3)
            src = element.get_attribute('src')
            headers = { "referer":"https://passport.jd.com/uc/login?ltype=logout"}
            print("刷新验证码")
            img = requests.get(src, headers=headers)
            with open('captcha.jpg', 'wb') as f:
                f.write(img.content)

            # driver.maximize_window()
            # driver.save_screenshot('screenshot.png')
            # print("定位验证码图片"
            # left = element.location['x']
            # top = element.location['y']-7
            # right = element.location['x'] + element.size['width']
            # bottom = element.location['y'] + element.size['height']
            # print left, top
            # im = Image.open('screenshot.png')
            # im = im.resize((html.size['width'],html.size['height']))
            # print("剪切验证码图片"
            # im = im.crop((left, top, right, bottom))
            # # im.filter(ImageFilter.FIND_EDGES)
            # im.save(authcode_img)

            # 过滤照片，只提取字符
            img = cv2.imread('captcha.jpg')
            lower_black = np.array([0,0,0])
            upper_black = np.array([30,30,30])
            mask = cv2.inRange(img, lower_black, upper_black)
            cv2.imwrite(authcode_img,mask)

            # 强化照片，然它更平滑
            image = Image.open(authcode_img)
            image = image.filter(ImageFilter.SMOOTH)
            image.save(authcode_img)

            authcode = extract_text_by_baidu(authcode_img)
            print("提取的验证码为:", authcode)
            if len(authcode) != 4:
                print("验证码提取错误")
                continue
            driver.find_element_by_id("authcode").send_keys(authcode)
            time.sleep(2)
            driver.find_element_by_id("loginsubmit").click()
            time.sleep(3)
        except Exception as e:
            print(e.message)
            print("no need authcode")
            time.sleep(5)

    driver.get("https://vip.jd.com/sign/index")
    print("签到，并领取京豆")
    time.sleep(2)

    driver.get("https://home.jd.com/")
    time.sleep(3)
    try:
        print(driver.find_element_by_id("JingdouCount").find_element_by_tag_name("em").text)
    except Exception:
        print("no JingdouCount")

    time.sleep(100)
    driver.close()


if __name__ == '__main__':
    login(sys.argv[1], sys.argv[2])

