# -*- coding: utf-8 -*-
import time

import requests

from common_utils import *
import sys
import datetime


def checkLogin(driver):
    try:
        if len(driver.find_elements_by_class_name("usrrin_name")) > 0:
            logger.debug("login success")
            return True
        else:
            return False
    except Exception:
        logger.debug("login failure")
        # driver.find_element_by_class_name("nickname")
        return False

def login(userName, password):
    try:
        driver = create_chrome(disableImage=False, mobile=False)
        url = "http://login.189.cn/web/login"

        while checkLogin(driver) == False:
            try:
                driver.get(url)
                time.sleep(3)
                logger.debug("loging...")
                txtAccount = driver.find_element_by_id("txtAccount")
                if not userName in txtAccount.get_attribute("data-preval"):
                    driver.find_element_by_id("txtAccount").send_keys(userName)
                password_input = driver.find_element_by_id("txtShowPwd")
                Hover = ActionChains(driver).move_to_element(password_input).click_and_hold(password_input).send_keys(password)
                Hover.perform()

                html = driver.find_element_by_tag_name('html')
                element = driver.find_element_by_id("imgCaptcha")
                driver.maximize_window()
                driver.save_screenshot('screenshot.png')
                logger.debug("find imgCaptcha")
                left = element.location['x']
                top = element.location['y'] - 15
                right = element.location['x'] + element.size['width']
                bottom = element.location['y'] + element.size['height']
                im = Image.open('screenshot.png')
                im = im.resize((html.size['width'],html.size['height']))
                logger.debug("cut imgCaptcha")
                im = im.crop((left, top, right, bottom))
                # im.filter(ImageFilter.FIND_EDGES)
                im.save("out.png")
                # src = element.get_attribute('src')
                # img = requests.get(src)
                # with open('captcha.jpg', 'wb') as f:
                #     f.write(img.content)

                authcode = extract_text_by_google("out.png")
                authcode = authcode.strip().replace(' ', '')
                logger.debug("authcode is :" + authcode)
                if authcode == '':
                    continue

                driver.find_element_by_id("txtCaptcha").send_keys(authcode)
                driver.find_element_by_id("loginbtn").click()
                logger.debug("submit ...")
                time.sleep(5)
            except Exception:
                logger.exception("not able to access DX")
    except Exception:
        logger.exception("not able to access DX")


if __name__ == '__main__':
    login(sys.argv[1], sys.argv[2])