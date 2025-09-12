import asyncio
from asyncio import PriorityQueue,TimeoutError,CancelledError
from typing import Optional
from YRX.自建框架.bald_spider.utils.pqeue import Spider_PriorityQueue
class Scheduler:
    def __init__(self):
        self.request_queue: Optional[Spider_PriorityQueue] = None

    def open(self):
        self.request_queue = Spider_PriorityQueue()

# 定义一个异步函数，用于获取下一个请求
    async def next_request(self):
        # 从请求队列中获取下一个请求
        # 这里设置了超时控制，原因：
        # 避免永久阻塞：如果队列长期为空，协程会一直挂起，导致程序 "卡死"。
        #
        # 释放资源：超时后协程可处理其他任务（如心跳检测、清理资源等）。
        #
        # 响应外部事件：例如用户取消操作或系统信号。

        # 返回获取到的请求
        request = await self.request_queue.get()
        return request

    async def enqueue_request(self, request):
        # 将请求添加到请求队列中
        await self.request_queue.put(request)

    def idle(self) -> bool:
        return len(self) == 0
    def __len__(self):
        return self.request_queue.qsize()
