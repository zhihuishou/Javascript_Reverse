# 这里做了一个基类init方法，主要是判定是否start_urls是否为列表，如果为列表则遍历，否则判断是否存在start_url属性以及是否为字符串，是则返回，否则报错
from YRX.自建框架.bald_spider import Request


class Spider:
    def __init__(self):
        if not hasattr(self, 'start_urls'):
            self.start_urls = []
    def start_requests(self):
        if self.start_urls:
            for url in self.start_urls:
                yield Request(url=url)
        else:
         # 是否存在start_urls属性以及未列表
            if hasattr(self, 'start_urls') and isinstance(getattr(self,'start_urls'),str):
                yield  Request(getattr(self,'start_urls'))

    def parse(self, response):
        raise NotImplementedError