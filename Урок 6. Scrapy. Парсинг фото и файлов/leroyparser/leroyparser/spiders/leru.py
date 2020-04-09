# -*- coding: utf-8 -*-
from collections import defaultdict
import pprint
import scrapy
from scrapy.http import HtmlResponse
from leroyparser.leroyparser.items import LeroyparserItem
from scrapy.loader import ItemLoader
import pandas as pd
class LeruSpider(scrapy.Spider):
    name = 'leru'
    allowed_domains = ['leroymerlin.ru']
    start_urls = ['http://leroymerlin.ru/']

    def __init__(self, text):
        self.start_urls = [f'https://leroymerlin.ru/search/?q={text}']

    def parse(self, response):
        ads_links = response.xpath("//div[@class='product-name']//a/@href").extract()
        for link in ads_links:
            yield response.follow(link, callback=self.parse_ads)

        next_page = response.xpath("//a[@class = 'paginator-button next-paginator-button']/@href").extract_first()
        yield response.follow(next_page, callback=self.parse)

    def parse_ads(self, response: HtmlResponse):
        loader = ItemLoader(item=LeroyparserItem(), response=response)
        loader.add_xpath('name', "//h1[@class='header-2']/text()")
        loader.add_xpath('photos', "//source[@media='only screen and (min-width: 768px)']/@srcset")
        params = response.xpath("//div//dt/text()").extract()
        values = response.xpath("//div//dd/text()").extract()
        d_params = defaultdict(list)
        for param, value in zip(params, values):
            s = str(value).replace("\n", "").replace(" ", "")
            d_params[param].append(s)
        loader.add_value('params', d_params)

        loader.add_xpath('prices_in', "//span[@slot = 'price']/text()")
        loader.add_xpath('currency', "//span[@slot = 'currency']/text()")
        loader.add_xpath('unit', "//span[@slot = 'unit']/text()")

        loader.add_value('link', response.url)
        yield loader.load_item()
