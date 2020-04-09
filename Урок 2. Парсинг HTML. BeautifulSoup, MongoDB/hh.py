from pprint import pprint
from bs4 import BeautifulSoup as bs, ResultSet
import requests
import pandas as pd
pd.set_option('display.max_columns', 6)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'}
site = 'https://hh.ru/'
main_link = 'https://hh.ru/search/vacancy?L_is_autosearch=false&area=113&clusters=true&enable_snippets=true&search_period=30&text='
print('введите название вакансии:')
position = input()

page_number = 0
next_button = []
vacancies = []
while next_button.__class__ != None.__class__:
    addr = f'{main_link}{position}&page={page_number}'
    response = requests.get(addr, headers=headers).text
    soup = bs(response, 'lxml')

    next_button = soup.find('a',{'class':'bloko-button HH-Pager-Controls-Next HH-Pager-Control'})


    vacanсy_block = soup.find_all('div',{'class':'vacancy-serp'})[0]
    vacanсy_list = vacanсy_block.find_all('div',{'data-qa':'vacancy-serp__vacancy'})
    page_number = page_number + 1

    for vacancy in vacanсy_list:
        vacancy_data={}
        vacancy_title = vacancy.find('a',{'data-qa':'vacancy-serp__vacancy-title'}).getText()
        salary_bloc = vacancy.find('span',{'data-qa':'vacancy-serp__vacancy-compensation'})
        vacancy_salary_min = None
        vacancy_salary_max = None
        vacancy_currency = None
        if salary_bloc.__class__ != None.__class__:
            vacancy_salary = salary_bloc.getText().split(" ")

            if vacancy_salary[0] == 'от':
                vacancy_salary_min = vacancy_salary[1].replace('\xa0', '')
            elif vacancy_salary[0] == 'до':
                vacancy_salary_max = vacancy_salary[1].replace('\xa0', '')
            else:
                range = vacancy_salary[0].split("-")
                vacancy_salary_min = range[0].replace('\xa0', '')
                vacancy_salary_max = range[1].replace('\xa0', '')
            vacancy_currency = vacancy_salary[len(vacancy_salary)-1]
        vacancy_link = vacancy.find('a',{'data-qa':'vacancy-serp__vacancy-title'})['href']
        vacancy_data['title'] = vacancy_title
        vacancy_data['salary_min'] = vacancy_salary_min
        vacancy_data['salary_max'] = vacancy_salary_max
        vacancy_data['currency'] = vacancy_currency
        vacancy_data['link'] = vacancy_link
        vacancy_data['site'] = site
        vacancies.append(vacancy_data)

df = pd.DataFrame(vacancies)
df.sort_values('salary_max')
pprint(df)
print(len(df))
print(page_number)

