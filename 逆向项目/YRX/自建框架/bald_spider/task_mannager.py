
from typing import Set,Final
from asyncio import Task,Future,Semaphore
import asyncio


class TaskManager:
    def __init__(self,totall_concurrency=4):
        self.current_task : Final[Set] = set()
        self.semaphore: Semaphore = Semaphore(totall_concurrency)

    def create_task(self,coroutine) -> Task:
        task = asyncio.create_task(coroutine)
        self.current_task.add(task)
        def done_callback(_fut: Future):
            self.current_task.remove(task)
            self.semaphore.release()
        task.add_done_callback(done_callback)
        return task

    def all_done(self):
        return len(self.current_task) == 0


    def remove_task(self) -> Task:
        pass