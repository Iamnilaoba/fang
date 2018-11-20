# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class FangItem(scrapy.Item):
    name=scrapy.Field()
    size=scrapy.Field()
    address=scrapy.Field()
    price=scrapy.Field()
    phone=scrapy.Field()
    province=scrapy.Field()
    city=scrapy.Field()
