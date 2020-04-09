from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from leroyparser.leroyparser import settings
from leroyparser.leroyparser.spiders.leru import LeruSpider
from leroyparser.leroyparser import settings

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)
    process = CrawlerProcess(settings=crawler_settings)
    print('введите название оборудования:')
    text = input()
    process.crawl(LeruSpider, text=text)
    process.start()


