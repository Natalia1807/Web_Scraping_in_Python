import requests
import json
from bs4 import BeautifulSoup as bs
from pprint import pprint
import re
import pandas as pd

# text= input('Какую профессию ищем? ')

text = 'Python'
page = 0
max_page = 0

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'}
# Пасрсим 'https://hh.ru'
main_link_hh = 'https://hh.ru'
response = requests.get(main_link_hh+'/search/vacancy?text={text}&page={page}', headers=headers)
if response.ok:
    soup = bs(response.text, 'lxml')

vacancy_bloc = soup.find_all('div', {'class':'vacancy-serp'})[0] # не поняла почемуу нужно ставить индекс, такой тег один. Если без индекса, то вылетает ошибка
vacancy_list = vacancy_bloc.find_all('div',{'class':'vacancy-serp-item'})
hh_pages_max = int(soup.find('a', {'class': 'bloko-button HH-Pager-Control'}).getText())

vacancy_all_hh = []
while max_page != hh_pages_max:
    page += 1
    max_page += 1
    for vacancy in vacancy_list:
        vacancy_hh_data = {}
        vacancy_name_hh = vacancy.find('a').getText()
        vacancy_link_hh = vacancy.find('a')['href']
        vacancy_city_hh = vacancy.find('span', {'class': 'vacancy-serp-item__meta-info'}).getText()
        vacancy_salary_hh = vacancy.find('div', {'class': 'vacancy-serp-item__sidebar'}).getText()

        if len(vacancy_salary_hh) > 1:
            vacancy_salary_hh_1 = vacancy_salary_hh.split(' ')

            if vacancy_salary_hh_1[0] == 'от':
                max_salary_hh = None
                min_salary_hh = vacancy_salary_hh_1[1]
                min_salary_hh = int(re.sub("\D", "", min_salary_hh))
                vacancy_salary_hh_curr = vacancy_salary_hh_1[2]

            elif vacancy_salary_hh_1[0] == 'до':
                max_salary_hh = vacancy_salary_hh_1[1]
                max_salary_hh = int(re.sub("\D", "", max_salary_hh))
                min_salary_hh = None
                vacancy_salary_hh_curr = vacancy_salary_hh_1[2]

            else:
                vacancy_salary_hh_curr = vacancy_salary_hh_1[1]
                vacancy_salary_hh = vacancy_salary_hh_1[0].split('-')
                min_salary_hh = vacancy_salary_hh[0]
                min_salary_hh = int(re.sub("\D", "", min_salary_hh))
                max_salary_hh = vacancy_salary_hh[1]
                max_salary_hh = int(re.sub("\D", "", max_salary_hh))
        else:
            min_salary_hh = None
            max_salary_hh = None
            vacancy_salary_hh_curr = None

        vacancy_hh_data['name'] = vacancy_name_hh
        vacancy_hh_data['link'] = vacancy_link_hh
        vacancy_hh_data['city'] = vacancy_city_hh
        vacancy_hh_data['min_salary'] = min_salary_hh
        vacancy_hh_data['max_salary'] = max_salary_hh
        vacancy_hh_data['currency'] = vacancy_salary_hh_curr
        vacancy_hh_data['source'] = main_link_hh
        vacancy_all_hh.append(vacancy_hh_data)
        # print(vacancy_hh_data)

hh = pd.DataFrame(vacancy_all_hh)
# print(hh)

# Пасрсим 'https://www.superjob.ru/'
#text= input('Какую профессию ищем? ')


page = 0
max_page = 0

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'}

main_link_sj = 'https://www.superjob.ru/'
html_sj = requests.get(main_link_sj + f'/vacancy/search/?keywords={text}&geo%5Bc%5D%5B0%5D=1', headers=headers)
if html_sj.ok:
    soup_sj = bs(html_sj.text, 'lxml')

vacancy_bloc_sj = soup_sj.find_all('div', {'class':'_1ID8B'})[0]
vacancy_list_sj = soup_sj.find_all('div', {'class': '_3zucV f-test-vacancy-item _3j3cA RwN9e _3tNK- _1NStQ _1I1pc'})
sj_pages_max = soup_sj.find('span', {'class': 'qTHqo _1mEoj _2h9me DYJ1Y _2FQ5q _2GT-y'})
sj_pages_max = int(sj_pages_max.find('span', {'class': '_3IDf-'}).getText())


vacancy_all_sj = []
while max_page != sj_pages_max:
    page += 1
    max_page += 1
    for vacancy in vacancy_list_sj:
        vacancy_sj_data = {}
        vacancy_name_sj = vacancy.find('a').getText()
        vacancy_link_sj = main_link_sj + vacancy.find('a')['href']
        vacancy_city_sj = vacancy.find('span', {'class': 'f-test-text-company-item-location'}).getText()
        vacancy_city_sj = vacancy_city_sj.split(' ')[2]
        vacancy_salary_sj = vacancy.find('span', {'class': '_3mfro _2Wp8I _31tpt f-test-text-company-item-salary PlM3e _2JVkc _2VHxz'}).getText()
        vacancy_salary_sj = vacancy_salary_sj.split('-')
        # print(vacancy_salary_sj)
        # print(''.join(re.findall('\d', vacancy_salary_sj[0])))
        if len(vacancy_salary_sj) > 1:
            vacancy_salary_sj_1 = vacancy_salary_sj.split(' ')

            if vacancy_salary_sj_1[0] == 'от':
                max_salary_sj = None
                min_salary_sj = vacancy_salary_sj_1[1]
                min_salary_sj = int(re.sub("\D", "", min_salary_sj))
                vacancy_salary_sj_curr = vacancy_salary_sj_1[2]

            elif vacancy_salary_sj_1[0] == 'до':
                max_salary_sj = vacancy_salary_sj_1[1]
                max_salary_sj = int(re.sub("\D", "", max_salary_sj))
                min_salary_sj = None
                vacancy_salary_sj_curr = vacancy_salary_sj_1[2]

            else:
                vacancy_salary_sj_curr = vacancy_salary_sj_1[1]
                vacancy_salary_sj = vacancy_salary_sj.split('-')
                min_salary_sj = (''.join(re.findall('\d', vacancy_salary_sj[0])))
                max_salary_sj = (''.join(re.findall('\d', vacancy_salary_sj[0])))
        else:
            min_salary_sj = None
            max_salary_sj = None
            vacancy_salary_sj_curr = None

        vacancy_sj_data['name'] = vacancy_name_sj
        vacancy_sj_data['link'] = vacancy_link_sj
        vacancy_sj_data['city'] = vacancy_city_sj
        vacancy_sj_data['min_salary'] = min_salary_sj
        vacancy_sj_data['max_salary'] = max_salary_sj
        vacancy_sj_data['currency'] = main_link_sj
        vacancy_sj_data['source'] = vacancy_salary_sj_curr
        vacancy_all_sj.append(vacancy_sj_data)
        # print(vacancy_sj_data)

sj = pd.DataFrame(vacancy_all_sj)

parser = pd.concat([hh, sj], axis=0)


#исправила ошибки предыдущего урока. Сделала разные листы для вакансий с разных сайтов. Потом объеденила в одном датафрейме.


from pymongo import MongoClient
from pprint import pprint

client = MongoClient('localhost', 27017)
db = client['bases']
vacancies = db.vacancies

vacancies_all = parser.to_dict('records')
# print(len(vacancies_all))
vacancies.insert_many(vacancies_all)
# v = vacancies.find({})  # Спасибо за помощь. Проверила. С переменной в цикле все работает
# for record in v:
#     print(record)

salary_search = int(input('Какую зарплату хотите?: '))
salary = vacancies.find({'max_salary': {'$gt': salary_search}})  # 1-ый вариант
salary_1 = vacancies.find({'$or':[{'min_salary': {'$gt': salary_search}}, {'max_salary': {'$gt': salary_search}}]})  # 2-ой вариант
for records in salary_1:
    pprint(records)



vacancies_all_update = parser.to_dict('records')
for item in vacancies_all_update:
     vacancies.update_one(
         {'link': item['link']},
         {'$set':
         {'name': item['name'],
         'link': item['link'],
         'source': item['source'],
         'city': item['city'],
         'employer': item['employer'],
         'salary': item['salary'],
         'min_salary': item['min_salary'],
         'max_salary': item['max_salary']},
          },
          upsert=True
          )
vacancies_new = vacancies.find({})
for record in vacancies_new:
    pprint(record)

