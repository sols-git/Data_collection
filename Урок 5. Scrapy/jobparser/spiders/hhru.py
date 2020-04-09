# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem

class HhruSpider(scrapy.Spider):
    name = 'hhru'
    allowed_domains = ['hh.ru']

    def __init__(self, text):
        self.start_urls = [
            f'https://hh.ru/search/vacancy?clusters=true&area=113&enable_snippets=true&salary=&st=searchVacancy&text={text}']
        self.vacancy_link = None
    def parse(self, response:HtmlResponse):
        next_page = response.css("a.HH-Pager-Controls-Next::attr(href)").extract_first()
        yield response.follow(next_page, callback=self.parse)

        vacancy_links = response.xpath("//a[@class='bloko-link HH-LinkModifier']/@href").extract()
        for link in vacancy_links:
            self.vacancy_link = link
            yield response.follow(link,callback=self.vacancy_pars)

    def vacancy_pars(self, response:HtmlResponse):
        name = response.css("div.vacancy-title h1::text").extract_first()
        salary = response.xpath("//span[@class='bloko-header-2 bloko-header-2_lite']/text()").extract()

        yield JobparserItem(name=name, salary=salary, link=self.vacancy_link)
