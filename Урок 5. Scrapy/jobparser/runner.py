# 1) Доработать паука в имеющемся проекте, чтобы он формировал item по структуре:
# *Наименование вакансии
# *Зарплата от
# *Зарплата до
# *Ссылку на саму вакансию

# *Сайт откуда собрана вакансия
# И складывал все записи в БД(любую)

# 2) Создать в имеющемся проекте второго паука по сбору вакансий с сайта superjob.
# Паука должен формировать item'ы по аналогичной структуре и складывать данные также в БД

from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from jobparser import settings
# from jobparser import settings2
from jobparser.spiders.hhru import HhruSpider
from jobparser.spiders.superjob import SuperjobSpider
if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)
    process = CrawlerProcess(settings=crawler_settings)
    print('введите название вакансии:')
    text = input()
    process.crawl(HhruSpider, text='java')
    process.crawl(SuperjobSpider, text='java')
    process.start()


