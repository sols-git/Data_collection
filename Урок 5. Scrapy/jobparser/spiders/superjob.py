# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem

class SuperjobSpider(scrapy.Spider):
    name = 'superjob'
    allowed_domains = ['superjob.ru']

    def __init__(self, text):
        self.start_urls = [f'https://russia.superjob.ru/vacancy/search/?keywords={text}']
        self.vacancy_link = None

    def parse(self, response: HtmlResponse):
        next_page = response.css("a.f-test-link-Dalshe::attr(href)").extract_first()
        # xpath("//a[@class='icMQ_ _1_Cht _3ze9n f-test-button-dalshe f-test-link-Dalshe']/@href").extract()
        yield response.follow(next_page, callback=self.parse)

        vacancy_links = response.xpath("//div[@class='_3mfro CuJz5 PlM3e _2JVkc _3LJqf']/a/@href").extract()
        for link in vacancy_links:
            self.vacancy_link = link
            yield response.follow(link, callback=self.vacancy_pars)

    def vacancy_pars(self, response: HtmlResponse):
        name = response.xpath("//h1[@class='_3mfro rFbjy s1nFK _2JVkc']/text()").extract()[0]
        salary = response.xpath("//span[@class='_3mfro _2Wp8I ZON4b PlM3e _2JVkc']/text()").extract()

        yield JobparserItem(name=name, salary=salary, link=self.vacancy_link)
