from scrapy import Request
from scrapy.spiders import Spider
from chengduqiye.items import ChengduqiyeItem
from re import split

class OneSpider(Spider):
    name = "chengduspider"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:62.0) Gecko/20100101 Firefox/62.0',
    }

    address = "address not found"
    frname = "name not found"
    product = "product not found"
    date = "date not found"

    def start_requests(self):
        url = 'http://www.11467.com/chengdu/dir/g.htm'
        yield Request(url, headers=self.headers)

    def parse(self, response):
        # print("father:response")
        # print(response)
        qiyes = response.xpath('//ul[@class="companylist"]//li/div[2]')
        for qiye in qiyes:
            detail_url = "http:"+qiye.xpath("./h4/a/@href").extract_first()
            yield Request(detail_url, callback=self.parse_detail)

        next_url = 'http:'+response.xpath('//div[@class="pages"]/a[last()-1]/@href').extract_first()
        print(next_url)
        if next_url:
            yield Request(next_url, headers=self.headers)
    
    def parse_detail(self, response):
        # print("my:response")
        # print(response)
        item = ChengduqiyeItem()
        self.address = response.xpath('//div[@id="contact"]/div[@class="boxcontent"]/dl/dd[1]/text()').extract_first()
        hang = response.xpath('//div[@id="gongshang"]/div[@class="boxcontent"]/table/tr')
        for li in hang:
            if li.xpath('td[1]/text()').extract_first() == "法人名称：":
                self.frname = li.xpath('td[2]/text()').extract_first()
            if li.xpath('td[1]/text()').extract_first() == "成立时间：":
                self.date = li.xpath('td[2]/text()').extract_first()
            if li.xpath('td[1]/text()').extract_first() == "主要经营产品：":
                self.product = li.xpath('td[2]').extract()[0]
                
        item['address'] = self.address
        item['name'] = self.frname
        item['product'] = self.product
        item['date'] = self.date
        
        yield item