# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapytaobaoItem(scrapy.Item):
    purl = scrapy.Field()
    title = scrapy.Field()
    month_sales = scrapy.Field()
    pop = scrapy.Field()
    comment = scrapy.Field()
