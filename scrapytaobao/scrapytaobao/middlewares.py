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
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time

class ScrapytaobaoSpiderMiddleware(object):
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


class ScrapytaobaoDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    def __init__(self,parms=None):

        fireFoxOptions = webdriver.FirefoxOptions()
        fireFoxOptions.set_headless()
        fireFoxOptions.add_argument(
            'user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:62.0) Gecko/20100101 Firefox/62.0"',
        )
        fireFoxOptions.add_argument('charset="utf-8"')
        self.driver = webdriver.Firefox(firefox_options=fireFoxOptions)
        self.wait = WebDriverWait(self.driver, 8) # 初始化 wait 函数 不建议使用time.sleep()

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
        print("request.url"+request.url)
        bj = request.url[:2]
        url = request.url[2:]
        print("bjurl"+url)
        self.driver.get(url)
        # 注意以下判断是否为主/子页面请求
        if bj == "fa":
            try:
                self.wait.until(
                EC.presence_of_element_located((By.XPATH, '//div[@class="items"]/div[1]'))
                )
                self.wait.until(
                EC.presence_of_element_located((By.XPATH, '//li[@class="item next"]'))
                )
                # self.wait.until(
                # EC.presence_of_element_located((By.CLASS_NAME, "item next"))
                # )
            except TimeoutException:
                print("等待容器（商品或下一页）超时...")
            # 等待第一个商品以及下一页标签加载完毕
            # 注意超时会抛出错误,建议所有等待元素都包含在try里
        if bj == "so":
            try:
                self.wait.until(
                EC.presence_of_element_located((By.XPATH, '//a[@data-index="1"]'))
                )
                commentshow = self.driver.find_element_by_xpath('//a[@data-index="1"]')
                ActionChains(self.driver).click(commentshow).perform()
            except TimeoutException:
                print("等待评论按钮超时...")
            # 等待并点击评论按钮
            # 记得在点击前查找元素
            # .perform() 立即加载所有储存事件

            # 以下为对待天猫和淘宝页的不同分析结果
            if "tmall" in url:
                try:
                    element = WebDriverWait(self.driver, 2).until(
                    EC.presence_of_element_located((By.XPATH, '//div[@class="rate-tag-box"]'))
                    )
                    try:
                        turof = WebDriverWait(self.driver, 1).until(
                        EC.presence_of_element_located((By.CLASS_NAME, "rate-tag-toggle rate-tag-toggle-expand"))
                        )
                        commentshow = self.driver.find_element_by_class_name("rate-tag-toggle rate-tag-toggle-expand")
                        ActionChains(self.driver).click(commentshow).perform()
                        # 点击展开评论的标签
                    except TimeoutException:
                        print("等待展开评论的标签超时(1s)...")
                except TimeoutException:
                    print("等待评论标签超时(2s)...")
            if "taobao" in url:
                try:
                    element = WebDriverWait(self.driver, 2).until(
                    EC.presence_of_element_located((By.XPATH, '//ul[@class="kg-rate-wd-impression tb-r-ubox-bd"]'))
                    )
                except TimeoutException:
                    print("等待评论标签超时(2s)...")

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
