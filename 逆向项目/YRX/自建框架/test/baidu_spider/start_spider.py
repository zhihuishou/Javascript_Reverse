import requests
from YRX.自建框架.bald_spider.core.engine import Engine
from YRX.自建框架.bald_spider import Spider
from YRX.自建框架.bald_spider import Request


# 这里构建初始start_url继承关系
class Baidu_spider(Spider):

    start_urls = ["https://www.baidu.com/","https://www.baidu.com/"]


    def parse(self, response):
        print("parse",response)
        for i in range(10):
            url = "https://www.baidu.com/"
            request = Request(url,callback=self.parse_page) # 连续回调
            yield request

    def parse_page(self,response):
        print("parse_page",response)
        # for i in range(10):
        #     url = "https://www.baidu.com/"
        #     request = Request(url,callback=self.parse_detail) # 连续回调
        #     yield request

    # def parse_detail(self,response):
    #     print("parse_detail",response)
    #     for i in range(10):
    #         url = "https://www.baidu.com/"
    #         request = Request(url,callback=self.parse) # 连续回调
    #         yield request
