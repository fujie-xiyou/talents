# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class TalentsItem(scrapy.Item):
    # define the fields for your item here like:
    code = scrapy.Field()  # 知网唯一code
    name = scrapy.Field()
    orgn = scrapy.Field()  # 所属单位
    domas = scrapy.Field()  # 行业/知识领域
    article_num = scrapy.Field()  # 发文量
    download_num = scrapy.Field()  # 总下载量
    url = scrapy.Field()  # 知网主页链接
