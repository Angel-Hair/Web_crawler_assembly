# -*- coding: utf-8 -*-
import scrapy
from scrapytaobao.items import ScrapytaobaoItem
from scrapy import Request

class TaobaospiderSpider(scrapy.Spider):
    name = 'taobaospider'
    allowed_domains = ['www.taobao.com']
    start_urls = 'https://s.taobao.com/search?q=空气清洗剂'
    # max_page = 81

    def start_requests(self):
        yield Request(url="fa"+self.start_urls, callback=self.parse, dont_filter=True) # 注意 dont_filter=True 才能使得每个页面显示的商品数一致

    def parse(self, response):
        urls = response.xpath('//div[@class="items"]/div/div[2]/div[2]/a/@href').extract()
        # print("father:response")
        # print(urls)
        for url in urls:
            detail_url = "sohttp:s" + url
            print("deta:"+detail_url)
            yield Request(url=detail_url, callback=self.parse_detail, dont_filter=True)

        next_url = "fahttp:s" + response.xpath('//li[@class="item next"]/a/@href').extract_first()
        if next_url:
            yield Request(url=next_url, callback=self.parse, dont_filter=True)

    def parse_detail(self, response):
        print(response.xpath('//div[@class="tm-fcs-panel"]'))