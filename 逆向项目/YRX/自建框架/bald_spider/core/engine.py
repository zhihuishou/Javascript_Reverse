import asyncio
from typing import Optional,Generator,Callable
from inspect import iscoroutine

from YRX.自建框架.bald_spider import Spider
from 爬虫逆向工程.YRX.自建框架.bald_spider.core.downloader import Downloader
from 爬虫逆向工程.YRX.自建框架.bald_spider.core.scheduler import Scheduler

from YRX.自建框架.bald_spider.utils.spider import transform
from YRX.自建框架.bald_spider import Request
from YRX.自建框架.bald_spider.task_mannager import TaskManager
class Engine:

    def __init__(self):
        self.downloader:Optional[Downloader] = Downloader() # 这里使用Downloader类来下载
        self.start_request:Optional[Generator] = None #这里使用Optional表示start_request可能为空
        self.task_manager:TaskManager = TaskManager()
        self.scheduler:Optional[Scheduler] = None
        self.spider:Optional[Spider] = None
        self.running = False

    async def Spider_start(self,spider):
        self.running = True
        self.spider = spider
        self.scheduler = Scheduler()
        if hasattr(self.scheduler,'open'):
            self.scheduler.open()
        self.downloader = Downloader()
        self.start_request = iter(spider.start_requests())
        await self._open_spider()



    #这里需要注意的是，迭代器是次数调用，如果只调用单个next只会走单步运行
    async def crawl(self): # 这里改为协程函数
        # 主逻辑
        while self.running:
            if (request:=await self._get_next_request()) is not None:
                #如果存在请求，那么就让其传入_crawl捕获进行下载
                await self._crawl(request)
            else:
                try:
                    # 获取下一个请求
                    start_request = next(self.start_request)
                    # 下载请求
                except StopIteration:
                    # 如果没有更多的请求，则停止迭代
                    self.start_request = None
                except Exception as e:
                    # 调度器是否空闲？
                    if not await self._exit():
                # 如果空闲，则停止迭代
                        continue
                    self.running = False
                else:
                    # 入队
                    await self.enqueue_request(start_request) #协程入队
    async def _crawl(self,request):

        async def crawl_task():
            outputs = await self._fetch_response(request)
        #处理output
            #管理并发？
            if outputs:
                await self._handle_spider_output(outputs)
        # await asyncio.create_task((crawl_task()))
        await self.task_manager.semaphore.acquire()
        self.task_manager.create_task(crawl_task())


    async def _handle_spider_output(self,outputs):
        # 处理爬虫输出
        async for spider_output in outputs:
            #这里就要开始判断是否是数据还是请求
            if isinstance(spider_output,Request):
                # 如果是请求，则将其加入调度器

                await self.enqueue_request(spider_output)
            else:
                # 如果是数据，则将其交给管道处理
                raise NotImplementedError("请实现管道处理")

    async def enqueue_request(self,request):
        # 将请求加入调度器队列
        # await self.scheduler.enqueue_request(request)
        # 将请求加入调度器
        await self._schedule_request(request)

    async def _schedule_request(self,request):
        # 为什么要这么做？这边需要做一个去重
        await self.scheduler.enqueue_request(request)



    async def _fetch_response(self,request):
        # 下载请求
        async def _success(_response):
            #判断是否成功请求与回调
            callback:Callable = request.callback or self.spider.parse
            if _output := callback(_response):
                if iscoroutine(_output):#判断是否传入的parse为协程任务
                    await _output
                else:
                    #有可能只是生成器 or 异步
                    return transform(_output)

        _response = await self.downloader.fetch(request)
        output = await _success(_response)
        return output

    async def _get_next_request(self):
        # 下载请求
        return await self.scheduler.next_request()

    async def _open_spider(self):
        crawling = asyncio.create_task(self.crawl())# 创建一个task任务
        #这里可以运行其他项目
        await crawling

    async def _exit(self):
        if self.scheduler.idle() and self.downloader.idle() and self.task_manager.all_done():
            return True
        return False