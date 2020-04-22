# 1)Написать приложение, которое собирает основные новости с сайтов news.mail.ru, lenta.ru, yandex.news
# Для парсинга использовать xpath. Структура данных должна содержать:
# название источника,
# наименование новости,
# ссылку на новость,
# дата публикации
#
# 2)Сложить все новости в БД


from lxml import html
from requests import get
from pprint import pprint
import re
from datetime import datetime as dt
from pymongo import MongoClient

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'}


def request_yandex():
    main_link_yandex = 'https://yandex.ru'
    response = get(main_link_yandex + '/news',
                   headers=headers
                   )

    root = html.fromstring(response.text)
    result = []
    items = root.xpath("//div[contains(@class,'page-content__fixed')]/div/table//td")
    for item in items:
        info = {}
        name_news = item.xpath(".//h2/a/text()")[0]
        name_link = item.xpath(".//h2/a//@href")[0]
        time = item.xpath(".//div[contains(@class, 'story__date')]//text()")[0].split()
        time_news = time[-1]
        name_source = ''.join(time[:-1])

        info['name'] = name_news
        info['source'] = name_source
        info['link'] = main_link_yandex + name_link
        info['datetime'] = time_news
        result.append(info)
    return result

result_ya = request_yandex()


def request_lenta():
    main_link_lenta = 'https://lenta.ru/'
    response = get(main_link_lenta + '/news',
                   headers=headers
                   )

    root = html.fromstring(response.text)
    result = []
    items = root.xpath("//section[@class='row b-top7-for-main js-top-seven']//div[contains(@class,'item')]")
    for item in items:
        info = {}
        name = item.xpath(".//a//text()")[1]
        name_news = name.replace('\xa0', ' ')
        name_link = item.xpath(".//a/@href")[0]
        time = item.xpath(".//time/@datetime")[0].split()
        time_news = time[0].replace(',', '')
        # print(time_news)

        info['name'] = name_news
        info['source'] = main_link_lenta
        info['link'] = main_link_lenta + name_link
        info['datetime'] = time_news
        result.append(info)
    return result

result_lenta = request_lenta()
# pprint(result_lenta)

def request_mail():
    main_link_mail = 'https://mail.ru/'
    main_link_mail_1 = 'https://news.mail.ru/'
    response = get('https://news.mail.ru/',
                   headers=headers
                   )

    root = html.fromstring(response.text)
    item_list = []
    items = root.xpath("//div[@class='js-module']/div//td/div[@class='daynews__item daynews__item_big']//a/@href | //div[@class='js-module']/div//td/div[@class='daynews__item']//a/@href | //div[@class='js-module']/ul/li[@class='list__item']//a/@href | //div[@class='js-module']/ul/li[@class='list__item hidden_small']//a/@href")
    item_list = []
    for item in items:
        link_line = main_link_mail_1 + item
        item_list.append(link_line)

    result = []
    for item in item_list:
        info = {}
        response = get(item, headers=headers)
        root = html.fromstring(response.text)
        item = response.url
        name_news = root.xpath("//h1[@class='hdr__inner']//text()")[0]
        name_source = root.xpath("//a[@class='link color_gray breadcrumbs__link']//span[@class='link__text']//text()")[0]
        time_news = root.xpath("//span[@class='note__text breadcrumbs__text js-ago']/@datetime")[0]

        info['name'] = name_news
        info['source'] = name_source
        info['link'] = item
        info['datetime'] = time_news
        result.append(info)
    return result

result_mail = request_mail()
# pprint(result_mail)



client = MongoClient('localhost', 27017)
db = client['news']
all_news = db.all_news

all_news.insert_many(result_ya)
all_news.insert_many(result_lenta)
all_news.insert_many(result_mail)

news  = all_news.find({})
for record in news:
    print(record)

