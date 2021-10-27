# https://voronezh.hh.ru/search/vacancy?area=26&fromSearchLine=true&text=Сварщик&from=suggest_post
# https://voronezh.hh.ru/search/vacancy?text=сварщик&salary=&currency_code=RUR&experience=doesNotMatter&order_by=relevance&search_period=0&items_on_page=50&no_magic=true&L_save_area=true

import requests
from bs4 import BeautifulSoup
from pprint import pprint

url = 'https://voronezh.hh.ru/'

vacancy = input('Введите название вакансии: ')

params = {'text': vacancy}

headers = {'User Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/81.0.4044.96 YaBrowser/20.4.0.1458 Yowser/2.5 Safari/537.36'}

response = requests.get(url + 'search/vacancy', params=params, headers=headers).text
print(response)
