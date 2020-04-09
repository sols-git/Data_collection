import requests
import json
from pprint import pprint

print('введите пользователя:')
user = input()
main_link = f'https://api.github.com/users/{user}/repos'
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'}

response = requests.get(main_link, headers=headers)

if response.ok:
    data = json.loads(response.text)
    with open('repos.json', 'w') as f:
        json.dump(data, f)
    print(f'У пользователя {data[1]["owner"]["login"]}, есть следующие открытые репозитории:')
    for item in data:
        print({item["html_url"]})
