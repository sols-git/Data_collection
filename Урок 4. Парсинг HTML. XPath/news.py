# Написать приложение, которое собирает основные новости с сайтов mail.ru, lenta.ru, yandex-новости.
# Для парсинга использовать xpath. Структура данных должна содержать:
# •	название источника,
# •	наименование новости,
# •	ссылку на новость,
# •	дата публикации

from lxml import html
import requests
from pprint import pprint
from bs4 import BeautifulSoup as bs
import re
import urllib
from datetime import datetime, date, time


header = {'User-Agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 13_3 like Mac OS X) '
                       'AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/80.0.3987.95 '
                       'Mobile/15E148 Safari/604.1'}

news_aggregators = {'https://news.mail.ru',
                   'https://m.lenta.ru/parts/news',
                   'https://yandex.ru/news/'}

result = []
def get_news(aggregator):
        response = requests.get(aggregator, headers=header)
        root = html.fromstring(response.text)  # Получаем DOM
        # print(response)

        if aggregator == 'https://news.mail.ru':
            items = root.xpath("//a[@class='item item_side_left entity']")
            for item in items:
                dict = {}
                link = str(item.xpath(".//@href")[0])
                if re.search('card', str(link)) or re.search('r.mail.ru', str(link)):
                    print("Не новости или статьи где не указана дата и источник: " + str(link))
                else:
                    if not re.search(aggregator, link):
                        link = aggregator + link
                    try:
                        article_page = requests.get(link, headers=header)
                        article = html.fromstring(article_page.text)  # Получаем DOM
                        article_param = article.xpath("//div[@class='article__params']")[0]
                        dict['link'] = link
                        dict['title'] = item.xpath(".//text()")
                        dict['date'] = str(article_param.xpath(".//@datetime")).replace("['", "").replace("+03:00']", "").replace("T", " ")
                        dict['source'] = article_param.xpath(".//@href")
                        result.append(dict)
                    except Exception as e:
                        print(e)

        elif aggregator == 'https://m.lenta.ru/parts/news':
            items = root.xpath("//div[@class='parts-page__item']")  # Внешние блоки, содержащие ссылку
            for item in items:  # Проходимся по блокам
                try:
                    dict = {}   #Используем ./ чтобы ограничить работу xpath текущим блоком

                    dict['link'] = aggregator.replace("parts/news","") + \
                                   str(item.xpath(".//@href")).replace("['/", "").replace("/']", "")
                    dict['title'] = item.xpath(".//div[@class='card-mini__title']/text()")
                    dict['source'] = aggregator
                    datime = str(datetime.now())[:11]
                    dict['date'] = datime + str(item.xpath(".//time[@class='card-mini__date']/text()")).replace("['", "").replace("']", "")
                    result.append(dict)
                except Exception as e:
                    print(e)
        elif aggregator == 'https://yandex.ru/news/':
            items = root.xpath("//div[@class='card__body']")  # Внешние блоки, содержащие ссылку
            for item in items:  # Проходимся по блокам
                dict = {}  # Используем ./ чтобы ограничить работу xpath текущим блоком
                try:
                    dict['link'] = item.xpath(
                        ".//a[@class='Link link card__link link-like link-like_type_turbo-navigation-react']/@href")
                    dict['title'] = item.xpath(
                        ".//a[@class='Link link card__link link-like link-like_type_turbo-navigation-react']/text()")
                    dict['source'] = item.xpath(".//@aria-label")[0]
                    datime = str(datetime.now())[:11]
                    dict['date'] = datime + str(item.xpath(".//span[@class ='sport-date card__source-date']/text()")).replace("['", "").replace("']", "")
                    result.append(dict)
                except Exception as e:
                    print(e)


def news():
    for aggregator in news_aggregators:
        get_news(aggregator)
    return result

pprint(news())


