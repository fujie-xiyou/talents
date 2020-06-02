# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from scrapy import Item


class TalentsPipeline(object):
    def process_item(self, item, spider):
        return item


class MongoDBPipeline(object):
    """
    将item写入MongoDB
    """

    @classmethod
    # 爬虫启动时，初始化管道，会执行该类方法，并将爬虫对象传入
    # 该方法会设置两个类属性，用来保存MongoDB的url和数据库名
    def from_crawler(cls, crawler):
        cls.DB_URL = crawler.settings.get('MONGO_DB_URI')
        cls.DB_NAME = crawler.settings.get('MONGO_DB_NAME')
        return cls()

    #
    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.DB_URL)
        self.db = self.client[self.DB_NAME]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        collection = self.db[spider.name]
        post = dict(item)
        try:
            collection.insert_one(post)
        except pymongo.errors.DuplicateKeyError:
            print("*******检测到重复信息 已丢弃: {}".format(post))
            return
        return item
