# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import TakeFirst, MapCompose, Compose


def cleaner_photo(value):
    if value[:2] == '//':
        return f'http:{value}'
    return value


def filter_price(value):
    res = int(str(value).replace(" ", ""))
    return res


class LeroyparserItem(scrapy.Item):
    _id = scrapy.Field()
    name = scrapy.Field(output_processor=TakeFirst())
    photos = scrapy.Field(input_processor=MapCompose(cleaner_photo))
    image_paths = scrapy.Field()
    params = scrapy.Field(output_processor=TakeFirst())
    prices_in = scrapy.Field(input_processor=MapCompose(filter_price))
    currency = scrapy.Field(output_processor=TakeFirst())
    unit = scrapy.Field(output_processor=TakeFirst())
    link = scrapy.Field(output_processor=TakeFirst())