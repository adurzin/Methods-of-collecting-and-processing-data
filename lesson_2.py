# https://voronezh.hh.ru/search/vacancy?text=Python&area=26&salary=&currency_code=RUR&experience=doesNotMatter&order_by=publication_time&search_period=0&items_on_page=20&no_magic=true&L_save_area=true&page=1

import requests
from bs4 import BeautifulSoup as bs
from pprint import pprint

url = 'https://hh.ru/'

vacancy = input('Введите название вакансии: ')

params = {'text': vacancy,
          'area': 26,
          'clusters': 'true',
          'enable_snippets': 'true',
          'ored_clusters': 'true',
          'experience': 'doesNotMatter',
          'order_by': 'publication_time',
          'search_period': 0,
          'items_on_page': 20,
          'no_magic': 'true',
          'L_save_area': 'true',
          'page': 0}

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)'
                         'Chrome/81.0.4044.96 YaBrowser/20.4.0.1458 Yowser/2.5 Safari/537.36'}

vacancy_list = []

while True:
    response = requests.get(url + 'search/vacancy', params=params, headers=headers)
    dom = bs(response.content, 'html.parser')
    vacancies = dom.find_all('div', {'class': "vacancy-serp-item"})

    if response.ok and vacancies:
        for vacancy in vacancies:
            vacancy_data = {}
            name = vacancy.find('a', {'data-qa': "vacancy-serp__vacancy-title"}).text
            link = vacancy.find('a', {'data-qa': "vacancy-serp__vacancy-title"})['href']
            try:
                salary = vacancy.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'}).text

                currency = salary.split()[::-1][0]  # зп валюта
                if salary.split()[0] == 'от':
                    salary_min = int(''.join(salary.split()[1:-1]))  # если "от"
                elif salary.split()[0] == 'до':
                    salary_max = int(''.join(salary.split()[1:-1]))  # если "до"
                else:
                    salary_min = salary[:(salary.find(' – '))]
                    salary_max = ''.join(salary[((salary.rfind(' – ') + 3)):(salary.rfind(' '))])
                    salary_min = int(''.join(salary_min.split()))  # минимальная зп
                    salary_max = int(''.join(salary_max.split()))  # максимальная зп
            except:
                salary_min = None
                salary_max = None
                currency = None

            vacancy_data['name'] = name  # наименование должности
            vacancy_data['link'] = link  # ссылка на вакансию
            vacancy_data['salary_min'] = salary_min  # минимальная зп
            vacancy_data['salary_max'] = salary_max  # максимальная зп
            vacancy_data['currency'] = currency  # валюта
            vacancy_data['site'] = 'hh.ru'  # не совсем понял, что нужно в этом пункте
            vacancy_list.append(vacancy_data)
        print(f'Обработана страница № {params["page"]}')
        params['page'] += 1
    else:
        break

import pandas as pd

df = pd.DataFrame(vacancy_list)

df.to_csv('data.csv')

print(len(vacancy_list))