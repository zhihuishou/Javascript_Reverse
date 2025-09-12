from asyncio import Semaphore,BoundedSemaphore
import asyncio
Semaphore = BoundedSemaphore(3)

async def demo():

    await Semaphore.acquire()
    print(11111)
    await Semaphore.acquire()
    print(11111)
    await Semaphore.acquire()
    print(11111)
    Semaphore.release()
    await Semaphore.acquire()
    print(11111)


asyncio.run(demo())
# async.run(demo())