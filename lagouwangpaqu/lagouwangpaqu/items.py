# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LagouwangpaquItem(scrapy.Item):
    name = scrapy.Field() #公司名称
    classification = scrapy.Field() #公司分类
    financing = scrapy.Field() #融资状况
    number = scrapy.Field() #人数
    map_address = scrapy.Field() #具体地址
    address = scrapy.Field() #分类地址
    # position = scrapy.Field() #招聘信息
    position_number = scrapy.Field() #招聘人数
