# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import scrapy
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline
from pymongo import MongoClient
import os
from urllib.parse import urlparse


class LeroyparserPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.leroy_photo

    def process_item(self, item, spider):
        collection = self.mongo_base[spider.name]
        collection.insert_one(item)
        return item


class LeroyPhotosPipeline(ImagesPipeline):
    global link_to_name
    link_to_name = {}

    def get_media_requests(self, item, info):
        global link_to_name
        for link in item['photos']:
            link_to_name[link] = item['name']
        if item['photos']:
            for img in item['photos']:
                try:
                    yield scrapy.Request(img)
                except Exception as e:
                    print(e)

    def file_path(self, request, response=None, info=None):
        directory_name = link_to_name[request.url]
        image_name = str(request.url).split('/')[-1]
        image_name = image_name[:image_name.find('.')]
        head_directory = self.spiderinfo.spider.name
        file_name = f'{head_directory}/{directory_name}/{image_name}.jpg'
        return file_name

    def item_completed(self, results, item, info):
        if results[0]:
            item['photos'] = [itm[1] for itm in results if itm[0]]
        return item

