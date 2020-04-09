from pprint import pprint
from bs4 import BeautifulSoup as bs, ResultSet
import requests
import pandas as pd

pd.set_option('display.max_columns', 6)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'}
site = 'https://superjob.ru'
main_link = 'https://russia.superjob.ru/vacancy/search/?keywords='
print('введите название вакансии:')
position = input()

page_number = 0
next_button = 'Дальше'
vacancies = []
while next_button.__class__ != None.__class__:
    addr = f'{main_link}{position}&page={page_number}'
    response = requests.get(addr, headers=headers).text
    soup = bs(response, 'lxml')
    next_button = soup.find('a', {'class':'icMQ_ _1_Cht _3ze9n f-test-button-dalshe f-test-link-Dalshe'})
    vacanсy_block = soup.find_all('div', {'style': 'display:block'})[0]

    vacanсy_list = vacanсy_block.find_all('div', {'class':"iJCa5 _2gFpt _1znz6 _2nteL"})

    page_number = page_number + 1

    for vacancy in vacanсy_list:
        vacancy_data = {}
        vacancy_title = vacancy.find('div', {'class': '_3mfro CuJz5 PlM3e _2JVkc _3LJqf'}).getText()
        salary_bloc = vacancy.find('span', {'class': '_3mfro _2Wp8I _31tpt f-test-text-company-item-salary PlM3e _2JVkc _2VHxz'})
        vacancy_salary_min = None
        vacancy_salary_max = None
        vacancy_currency = None
        if salary_bloc.__class__ != None.__class__:
            if salary_bloc.getText() != 'По договорённости':
                vacancy_salary = salary_bloc.getText().split("\xa0")
                if vacancy_salary[0] == 'от':
                    vacancy_salary_min = vacancy_salary[1] + vacancy_salary[2]
                elif vacancy_salary[0] == 'до':
                    vacancy_salary_max = vacancy_salary[1] + vacancy_salary[2]
                elif len(vacancy_salary) == 3:
                    vacancy_salary_min = vacancy_salary[0] + vacancy_salary[1]
                    vacancy_salary_max = vacancy_salary[0] + vacancy_salary[1]
                else:
                    vacancy_salary_min = vacancy_salary[0] + vacancy_salary[1]
                    vacancy_salary_max = vacancy_salary[3] + vacancy_salary[4]
                vacancy_currency = vacancy_salary[len(vacancy_salary) - 1]



        vacancy_link = vacancy.find('a')['href']
        vacancy_data['title'] = vacancy_title
        vacancy_data['salary_min'] = vacancy_salary_min
        vacancy_data['salary_max'] = vacancy_salary_max
        vacancy_data['currency'] = vacancy_currency
        vacancy_data['link'] = site + vacancy_link
        vacancy_data['site'] = site
        vacancies.append(vacancy_data)


df = pd.DataFrame(vacancies)
var = df[df["salary_max"].notnull()]
var.sort_values(["salary_max"])
pprint(var)
print(len(df))
print(page_number)
#print(df.describe())
