import requests
from lxml import html
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
import re

client = MongoClient('127.0.0.1', 27017)

db = client['yandex_news']
news = db.news

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                         ' Chrome/93.0.4577.82 YaBrowser/21.9.2.169 Yowser/2.5 Safari/537.36'}


response = requests.get('https://yandex.ru/', headers=headers)
dom = html.fromstring(response.text)
news = dom.xpath("//li[contains(@class, 'list__item  list__item_icon')]")

if response.ok and news:
    for item in news:
        news_data = {}
        source = item.xpath(".//span[@class='news__item-inner']/div/@title")
        name = item.xpath(".//span[contains(@class, 'news__item-content')]/text()")
        link = item.xpath(".//a/@href")
        date_news = item.xpath("//div[contains(@class, 'headline__item')]//@data-bem")
        news_data['sources'] = source
        news_data['names'] = name
        news_data['links'] = link
        news_data['date_news'] = re.search(r'\w{4,10} \d{2}, \d{4}', date_news[0])[0]
        news_data['_id'] = link[0][29:100]

        try:
            db.news.insert_one(news_data)
        except DuplicateKeyError:
            print('Новость уже есть в базе данных')
        