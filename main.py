import selenium
from selenium import webdriver
from fake_useragent import UserAgent

ua = UserAgent()
ua_ = ua.random

from pathlib import Path

import requests
from bs4 import BeautifulSoup
import lxml
import json
import time

import re

import xlsxwriter

workbook = xlsxwriter.Workbook('out.xlsx')
worksheet = workbook.add_worksheet()

# Add a bold format to use to highlight cells.
bold = workbook.add_format({'bold': True, 'font_color': 'blue'})
bold.set_align('left')

bold_1 = workbook.add_format({'bold': True, 'font_color': 'black'})
bold_1.set_align('center')

bold_2 = workbook.add_format({'bold': True, 'font_color': 'red'})
bold_2.set_align('center')

bold_3 = workbook.add_format({'bold': True, 'font_color': 'black'})
bold_3 = workbook.add_format({'bg_color': '#b4b4b4'})
bold_3.set_align('center')

bold_4 = workbook.add_format({'bold': True, 'font_color': 'black'})
bold_4.set_align('left')

data_format1 = workbook.add_format({'bg_color': '#b4b4b4'})
data_format1.set_align('center')
#
# =========================================================

# Format the first column
worksheet.set_column('A:A', 15, data_format1)
worksheet.set_column('B:B', 30)
worksheet.set_column('C:C', 25)
worksheet.set_column('D:D', 50)
worksheet.set_column('E:L', 25)


worksheet.set_default_row(25)

worksheet.write('A1', 'Search', bold_3)
worksheet.write('B1', 'Downloaded Date', bold_1)
worksheet.write('C1', 'URL', bold_1)
worksheet.write('D1', 'Title', bold_1)
worksheet.write('E1', 'Duration', bold_1)
worksheet.write('F1', 'Dimension', bold_1)
worksheet.write('G1', 'Aspect Ratio', bold_1)
worksheet.write('H1', 'FPS', bold_1)
worksheet.write('I1', 'Orientation', bold_1)
worksheet.write('J1', 'Username', bold_1)
worksheet.write('K1', 'License', bold_1)
worksheet.write('L1', 'Tags', bold_1)


find_ = 'happy'


"""
https://www.pexels.com/ru-ru/search/videos/happy/
"""

# url = 'https://www.pexels.com/video/people-in-a-party-raising-their-glasses-for-a-toss-while-confetti-are-falling-3188991/'


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


# читаю ССЫЛКИ из ранее созданного файла
# !!! ОБРЕЗАЮ СИМВОЛ ПЕРЕНОСА СТРОКИ !!!
with open('iddd.txt') as file:
    id_list = [line.strip() for line in file.readlines()]

row = 2

for iddd in id_list[0:11]:
# for iddd in id_list:

    print(f"start...{iddd}")

    url_ = f'https://www.pexels.com/video/{iddd}/'

    browser.get(url_)

    time.sleep(2)


    source_html = browser.page_source
    # # запись СПАРСЕНОЙ инфы в ХТМЛ-файл
    # with open('index.html', 'w', encoding='utf-8') as file:
    #     file.write(source_html)

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
    # description_ = ddd['props']['pageProps']['medium']['attributes']['description']
    width_ = ddd['props']['pageProps']['medium']['attributes']['width']
    height_ = ddd['props']['pageProps']['medium']['attributes']['height']

    if int(width_) > int(height_):
        orientations_ = 'Horizontal'
    else:
        orientations_ = 'Vertical'

    url_slug = ddd['query']['slug']
    url__ = f'https://www.pexels.com/video/{url_slug}'

    title_ = ddd['props']['pageProps']['medium']['attributes']['title']
    tags_ = ddd['props']['pageProps']['medium']['attributes']['tags']
    aspect_ratio_ = ddd['props']['pageProps']['medium']['attributes']['aspect_ratio']
    # date_ = ddd['props']['pageProps']['medium']['attributes']['updated_at']
    fps_ = ddd['props']['pageProps']['mediumDetails']['attributes']['fps']
    duration_ = ddd['props']['pageProps']['mediumDetails']['attributes']['duration']

    license__ = ddd['props']['pageProps']['__namespaces']['medium']['license']
    license_ = license__.replace(' %{creative_commons}', '')

    url_download = ddd['props']['pageProps']['medium']['attributes']['video']['video_files']

    download_bool = False

    # d_ = '3840'
    # if any(d_ in str(item).split('=')[-1] for item in url_download):
    #     print('YES! 3840')
    #     download_bool = True
    #     # break
    # else:
    d_ = '1920'
    if any(d_ in str(item).split('=')[-1] for item in url_download):
        print('YES! 1920')
        download_bool = True
        # break
    else:
        d_ = '1280'
        if any(d_ in str(item).split('=')[-1] for item in url_download):
            print('YES! 1280')
            download_bool = True
        else:
            print(f'!!!!!!!!!!!!!!!!   Full_HD or HD video NO present!   !!!!!!!!!!!!!!!!!!!\n')

    date_ = 'NONE'
    if download_bool:
        for d in url_download:
            d__ = d['download_link'].split('=')[-1]
            print(d)
            # print(d__)
            if d__ == d_:
                link_v = d['download_link']

                # obtain filename by splitting url and getting
                # last string
                # file_name = f'{title_}_{d_}.mp4'
                file_name = f'{title_}.mp4'
                file_path = f'./downloads/{file_name}'

                fle = Path(file_path)
                print(f'Download file:\n ---> {file_name}\n')

                if fle.is_file():
                    print(f'File present! Let`s skip...\n')
                    pass
                else:
                    print(f'File NO present!\n Downloding file:\n ---> %s\n' % file_name)

                    # create response object
                    r = requests.get(link_v, stream=True)

                    # download started
                    with open(file_path, 'wb') as f:
                        for chunk in r.iter_content(chunk_size=1024 * 1024):
                            if chunk:
                                f.write(chunk)

                    print("%s downloaded!\n" % file_name)
                    date_ = time.time()

    user_ = ddd['props']['pageProps']['medium']['attributes']['user']['first_name']

    dimension_ = f'{width_} x {height_}'

    # print(title_)
    # print(dimension_)
    # print(orientations_)
    # print(fps_)
    # print(f'{duration_} sec')
    # print(license_)
    # print(tags_)

    worksheet.write(f'A{row}', find_, bold_1)  # worksheet.write_url(f'F{row}', url, string=f'{lot_num}')
    worksheet.write(f'B{row}', date_, bold_1)
    worksheet.write(f'C{row}', url__, bold)
    worksheet.write(f'D{row}', title_, bold_4)
    worksheet.write(f'E{row}', duration_, bold_1)
    worksheet.write(f'F{row}', dimension_, bold_2)
    worksheet.write(f'G{row}', aspect_ratio_, bold_1)
    worksheet.write(f'H{row}', fps_, bold_1)
    worksheet.write(f'I{row}', orientations_, bold_1)
    worksheet.write(f'J{row}', user_, bold_1)
    worksheet.write(f'K{row}', license_, bold_2)
    worksheet.write(f'L{row}', str(tags_), bold_1)

    row = row + 1
    #
workbook.close()

