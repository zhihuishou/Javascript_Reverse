from asyncio import PriorityQueue,TimeoutError,CancelledError
import asyncio

class Spider_PriorityQueue(PriorityQueue):# 继承了优先级队列的方法

    def __init__(self, maxsize=0):
        super(Spider_PriorityQueue,self).__init__(maxsize=maxsize)

    async def get(self):
        f = super().get() # 获取原生get()返回的协程对象
        try:
            # 直接传递队列get()的协程给wait_for
            return await asyncio.wait_for(f, timeout=1.0)
        except TimeoutError:
            return None
        except CancelledError:
            print("任务被取消")
