# -*- coding: utf-8 -*-

from selenium.webdriver import Chrome, PhantomJS, ChromeOptions, ActionChains
from piltesseract import get_text_from_image
from aip import AipOcr
from PIL import Image, ImageEnhance, ImageFilter

import logging
from logging.config import fileConfig

fileConfig('logging.ini')
logger = logging.getLogger()

CHROME_PATH = '/Users/caishichao/Applications/webdriver/chromedriver'
SWITCHER_PATH = 'User-Agent-Switcher.crx'
PHANTOMJS_PATH = '/Users/caishichao/Applications/phantomjs-2.1.1-macosx/bin/phantomjs'


def create_chrome( disableImage = True, mobile=False ):
    options = ChromeOptions()
    chrome_prefs = {}
    if disableImage:
        chrome_prefs["profile.default_content_settings"] = {"images": 2}
        chrome_prefs["profile.managed_default_content_settings"] = {"images": 2}
    options.experimental_options["prefs"] = chrome_prefs
    options.add_argument('no-sandbox')
    if mobile:
        options.add_extension(SWITCHER_PATH)
    options.add_argument('disable-images')
    options.add_argument('headless')
    options.add_argument('disable-gpu')
    driver = Chrome(executable_path=CHROME_PATH, chrome_options=options)
    return driver


def create_PhantomJS():
    return PhantomJS(executable_path=PHANTOMJS_PATH)

""" 读取图片 """
def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()

def enhancer_img(img):
    enhancer = ImageEnhance.Contrast(img)  # 加强效果
    return enhancer.enhance(2)  # 加强效果


def del_img_noise(img):
    new_im = img.filter(ImageFilter.MedianFilter())  # 去噪
    # new_im.show()
    return enhancer_img(new_im)  # 加强效果


def convert_img_2_baw(img):
    return img.convert('L')  # 转化为灰度图片(黑白图片)


def extract_text_by_baidu(imagePath):
    """ 你的 APPID AK SK """
    APP_ID = '10523897'  # '10524589'
    API_KEY = 'eBr4MdT7xxm7wNMMlkqqtoCj'  # 'WPXZIn9Lve9oOym8Ep4UIEm4'
    SECRET_KEY = 'ATX9PR2mc2IdmT9wGm633LoAlQCeblTj'  # 'Afn2FUL2rMIO3Fn0Lj9SXQlXrFCN1H8k'
    client = AipOcr(APP_ID, API_KEY, SECRET_KEY)

    """ 如果有可选参数 """
    options = {}
    options["detect_direction"] = "true"
    options["probability"] = "true"
    img = get_file_content(imagePath)
    result = client.basicAccurate(img)
    if (len(result['words_result']) > 0):
        return result['words_result'][0]['words'].strip()
    else:
        return ""


def extract_text_by_google(imagePath):
    with Image.open(imagePath) as img:
        return get_text_from_image(img, tessedit_char_whitelist=digits)
