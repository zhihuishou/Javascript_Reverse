import scrapy


class WencaiSpiderSpider(scrapy.Spider):
    name = "wencai_spider"
    allowed_domains = ["www.iwencai.com"]
    start_urls = ["https://www.iwencai.com/customized/chart/get-robot-data"]

    def parse(self, response):
        pass
