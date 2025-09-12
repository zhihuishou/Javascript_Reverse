import random
import asyncio
# from YRX.自建框架.bald_spider import Request
import requests
class Downloader:
    def __init__(self):

        self._active = set()
    async def download(self,request):
        # 这里就是设置下载时间的逻辑随机数，随机数来自在主方法里输入的count

        await asyncio.sleep(random.uniform(0,1))
        # 接受download处理的结果
        # 需要有承接的engine
        return request

    async def fetch(self,request):
        self._active.add(request)
        response = await self.download(request)
        self._active.remove(request)
        return response
    def idle(self) -> bool:
        return len(self._active) == 0


    def __len__(self):
        return len(self._active)