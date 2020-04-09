# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient


class JobparserPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.vacancy312

    def process_item(self, item, spider):

        cleared_item = {}

        if spider.name == 'hhru':
            cleared_item['Наименование вакансии'] = item['name']
            cleared_item['Ссылка на вакансию'] = item['link']
            if len(item['salary']) == 1:
                cleared_item['Зарплата от'] = None
                cleared_item['Зарплата до'] = None
                cleared_item['Валюта'] = None
            if len(item['salary']) == 5:
                cleared_item['Зарплата от'] = item['salary'][1]
                cleared_item['Зарплата до'] = None
                cleared_item['Валюта'] = item['salary'][3]
            if len(item['salary']) == 7:
                cleared_item['Зарплата от'] = item['salary'][1]
                cleared_item['Зарплата до'] = item['salary'][3]
                cleared_item['Валюта'] = item['salary'][5]
            cleared_item['Источник вакансий'] = spider.allowed_domains[0]

            collection = self.mongo_base[spider.name]
            collection.insert_one(cleared_item)

        if spider.name == 'superjob':
            cleared_item['Наименование вакансии'] = item['name']
            cleared_item['Ссылка на вакансию'] = item['link']
            if len(item['salary']) == 1:
                cleared_item['Зарплата от'] = None
                cleared_item['Зарплата до'] = None
                cleared_item['Валюта'] = None
            if len(item['salary']) == 3:
                if item['salary'][0] == 'от':
                    cleared_item['Зарплата от'] = item['salary'][2].split("\xa0")[0] + item['salary'][2].split("\xa0")[1]
                    cleared_item['Зарплата до'] = None
                    cleared_item['Валюта'] = item['salary'][2].split("\xa0")[2]
                if item['salary'][0] == 'до':
                    cleared_item['Зарплата от'] = None
                    cleared_item['Зарплата до'] = item['salary'][2].split("\xa0")[0] + item['salary'][2].split("\xa0")[1]
                    cleared_item['Валюта'] = item['salary'][2].split("\xa0")[2]
            if len(item['salary']) == 4:
                cleared_item['Зарплата от'] = item['salary'][0].split("\xa0")[0] + item['salary'][0].split("\xa0")[1]
                cleared_item['Зарплата до'] = item['salary'][1].split("\xa0")[0] + item['salary'][1].split("\xa0")[1]
                cleared_item['Валюта'] = item['salary'][3]
            cleared_item['Источник вакансий'] = spider.allowed_domains[0]

            collection = self.mongo_base[spider.name]
            collection.insert_one(cleared_item)
        return item
