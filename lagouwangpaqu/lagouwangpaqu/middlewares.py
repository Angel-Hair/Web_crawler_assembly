# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from selenium import webdriver
from scrapy import signals
from scrapy.http import HtmlResponse
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

class LagouwangpaquSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class LagouwangpaquDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    def __init__(self,parms=None):

        fireFoxOptions = webdriver.FirefoxOptions()
        fireFoxOptions.set_headless()
        fireFoxOptions.add_argument(
            'user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:63.0) Gecko/20100101 Firefox/63.0"',
        )
        fireFoxOptions.add_argument('charset="utf-8"')
        self.driver = webdriver.Firefox(firefox_options=fireFoxOptions)
        # self.wait = WebDriverWait(self.driver, 8) # 初始化 wait 函数 不建议使用time.sleep()

    def __del__(self):
        self.driver.close()

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        print("request.url: "+request.url)
        self.driver.get(request.url)
        time.sleep(0.5)
        #判断加载的页面是简介还是招聘页面
        # try:
        #     self.wait.until(
        #         EC.presence_of_element_located((By.XPATH, '//div[@class="top_info_wrap"]'))
        #         )
        #     if request.url[29] == 'j': 
        #         self.wait.until(
        #         EC.presence_of_element_located((By.XPATH, '//div[@id="posfilterlist_container"]/div[@class="item_ltitle"]'))
        #         )
        #         self.wait.until(
        #         EC.presence_of_element_located((By.XPATH, '//li[@class="item next"]'))
        #         )
        #         # self.wait.until(
        #         # EC.presence_of_element_located((By.CLASS_NAME, "item next"))
        #         # )
        # except TimeoutException:
        #     print("等待容器超时...")

        return HtmlResponse(url=self.driver.current_url, body=self.driver.page_source, request=request, encoding='utf-8') # 注意编码一致

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
