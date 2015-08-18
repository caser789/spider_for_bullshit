# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient
from scrapy.exceptions import DropItem
from .settings import MONGODB_SERVER, MONGODB_PORT, MONGODB_DB, \
        MONGODB_COLLECTION
from scrapy import log


class MongoDBPipeline(object):
    def __init__(self):
        client = MongoClient(
               MONGODB_SERVER,
                MONGODB_PORT)
        db = client[MONGODB_DB]
        self.collection = db[MONGODB_COLLECTION]
    def process_item(self, item, spider):
        valid = True
        for data in item:
            if not data:
                valid = False
                raise DropItem('missing %s of blogposts from %s' %(data,
                    item['url']))
        if valid:
            self.collection.insert(dict(item))
            log.msg('Item wrote to MOngodb %s/%s' %
                    (MONGODB_DB, MONGODB_COLLECTION),
                    level=log.DEBUG, spider=spider)
        return item
