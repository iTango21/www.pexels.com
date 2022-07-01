import selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
# from selenium.Java
import time
from random import randrange
from fake_useragent import UserAgent

# from random import randrange
ua = UserAgent()
ua_ = ua.random

import sys
import time
from random import randrange

import asyncio
import aiohttp

import requests
from bs4 import BeautifulSoup
import lxml
import json
import time

import re

import pandas as pd


"""
https://www.pexels.com/ru-ru/search/videos/happy/
"""

url = 'https://www.pexels.com/video/people-in-a-party-raising-their-glasses-for-a-toss-while-confetti-are-falling-3188991/'


headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "User-Agent": f'{ua}'  # "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML,
    # like Gecko) Chrome/96.0.4664.45 Safari/537.36"
}

print('start...')

# # #         = 1 =
# # #
# # # # START of "Init..."
# # # #
chrome_path = "./chromedriver.exe"

options = webdriver.ChromeOptions()
options.headless = False
options.add_argument("--incognito")
options.add_argument("start-maximized")
#
# options.add_argument("--headless")
options.add_argument('--disable-blink-features=AutomationControlled')
#
# options.add_experimental_option("excludeSwitches", ["enable-logging"])
# options.add_experimental_option('useAutomationExtension', False)
browser = webdriver.Chrome(options=options, executable_path=chrome_path)

browser.implicitly_wait(1)
# # #
# # # END of "Init..."
#

browser.get(url)

time.sleep(3)

# logo_xp = '//*[@id="__next"]/div[2]/nav/div[1]/a/svg[1]/g'
# start_time = time.time()
# try:
#     WebDriverWait(browser, 15).until(EC.element_to_be_clickable((By.XPATH, logo_xp)))
# except:
#     pass
# finish_time = time.time() - start_time
# print(f'Load LOGO time: {finish_time}')

source_html = browser.page_source
# запись СПАРСЕНОЙ инфы в ХТМЛ-файл
with open('index.html', 'w', encoding='utf-8') as file:
    file.write(source_html)

soup = BeautifulSoup(source_html, 'lxml')

# SCRYPT!!!
#
script_all = soup.find('script', {'id': '__NEXT_DATA__'})




try:
    script_ = str(re.findall('<script id=\"__NEXT_DATA__\" type=\"application/json\">(.*?)<\/script>', str(script_all))). \
        replace("</script>", ""). \
        replace("['", "").replace("']", "").replace("\\", "_")
except:
    pass

# with open(f'_my_json_.json.', 'w', encoding='utf-8') as file:
#     # json.dump(script_, file, indent=4, ensure_ascii=False)
#     file.write(script_)



ddd = json.loads(script_)

# try:
#
# except:
#     pass

id_ = ddd['props']['pageProps']['medium']['attributes']['id']
description_ = ddd['props']['pageProps']['medium']['attributes']['description']

width_ = ddd['props']['pageProps']['medium']['attributes']['width']
height_ = ddd['props']['pageProps']['medium']['attributes']['height']

if int(width_) > int(height_):
    orientations_ = 'Horizontal'
else:
    orientations_ = 'Vertical'

title_ = ddd['props']['pageProps']['medium']['attributes']['title']
tags_ = ddd['props']['pageProps']['medium']['attributes']['tags']

fps_ = ddd['props']['pageProps']['mediumDetails']['attributes']['fps']
duration_ = ddd['props']['pageProps']['mediumDetails']['attributes']['duration']

license_ = ddd['props']['pageProps']['__namespaces']['medium']['license']


print(title_)
print(f'{width_} x {height_}')
print(orientations_)
print(fps_)
print(f'{duration_} sec')
print(license_)
print(tags_)

