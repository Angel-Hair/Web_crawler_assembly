from scrapy import Request
from scrapy.spiders import Spider
from lagouwangpaqu.items import LagouwangpaquItem
from re import split

class OneSpider(Spider):
    name = "lagouwangspider"
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Connection': 'keep-alive',
        'Cookie': 'your_cookie',
        'DNT': '1',
        'Host': 'www.lagou.com',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:63.0) Gecko/20100101 Firefox/63.0',
    }

    company_name = "not found"
    classification = "not found"
    financing = "not found"
    number = "not found"
    map_address = "not found"
    address = "not found"
    # position = "not found"
    position_number = "not found"

    start_urls = []
    max_list = 471720
    start = 7
    for a in range(start,max_list+1):
        url = "https://www.lagou.com/gongsi/"+str(a)+".html"
        start_urls.append(url)



    def parse(self, response):
        item = LagouwangpaquItem()
        print('Start crawling the first page...:'+response.url)

        self.company_name = "not found"
        self.classification = "not found"
        self.financing = "not found"
        self.number = "not found"
        self.map_address = "not found"
        self.address = "not found"
        # self.position = "not found"
        self.position_number = "not found"
        # print("response:",response)

        self.item = LagouwangpaquItem()
        self.company_name = response.xpath('//div[@class="company_main"]/h1/a/@title').extract_first()
        self.classification = response.xpath('//div[@id="basic_container"]/div[@class="item_content"]/ul/li[1]/span/text()').extract_first()
        self.financing = response.xpath('//div[@id="basic_container"]/div[@class="item_content"]/ul/li[2]/span/text()').extract_first()
        self.number = response.xpath('//div[@id="basic_container"]/div[@class="item_content"]/ul/li[3]/span/text()').extract_first()
        self.address = response.xpath('//div[@id="basic_container"]/div[@class="item_content"]/ul/li[4]/span/text()').extract_first()
        yun_map_address = response.xpath('//ul[@class="con_mlist_ul"]/li[1]/p[@class="mlist_li_desc"]/text()').extract_first()
        self.map_address = yun_map_address.strip()
        number_text = response.xpath('//div[@class="company_navs_wrap"]/ul/li[2]/a/text()').extract_first()
        self.position_number = int(number_text[number_text.find('（')+1:number_text.find('）')])

        print('The information of the first level page is processed.')

        # if self.position_number > 0 :
        #     recruit_url = response.url[:29]+"j"+response.url[29:]
        #     print('Start crawling the secondary page...:'+recruit_url)
        #     yield Request(recruit_url, callback=self.parse_recruit)

        print('Start saving information...')
        item['name'] = self.company_name
        item['classification'] = self.classification
        item['financing'] = self.financing
        item['number'] = self.number
        item['map_address'] = self.map_address
        item['address'] = self.address
        # item['position'] = self.position
        item['position_number'] = self.position_number
        
        yield item
    
    # def parse_recruit(self, response):
    #     # print("my:response:",response)
    #     self.position = []
    #     for one in range(1,int(self.position_number)+1):
    #         position_name = response.xpath('//ul[@class="item_con_list"]/li['+one+']/div/a/text()').extract_first()
    #         position_money = response.xpath('//ul[@class="item_con_list"]/li['+one+']/p/span[@class="item_salary"]/text()').extract_first()
    #         requirements = response.xpath('//ul[@class="item_con_list"]/li['+one+']/p/span[@class="item_desc"]/text()').extract_first()
    #         allposition = position_name + ';' + position_money + ';' + requirements
    #         self.position.append(allposition)
    #     print('The information of the secondary page is processed.')