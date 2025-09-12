from 爬虫逆向工程.YRX.自建框架.bald_spider.core.engine import Engine
from 爬虫逆向工程.YRX.自建框架.test.baidu_spider.start_spider import Baidu_spider
import asyncio



async def main():
    baidu_spider = Baidu_spider()
    engine = Engine()
    await engine.Spider_start(baidu_spider)

asyncio.run(main())