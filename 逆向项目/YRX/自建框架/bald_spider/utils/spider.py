from inspect import iscoroutine,isgenerator,isasyncgen
from 爬虫逆向工程.YRX.自建框架.bald_spider import TrsansoforTypeError
async def transform(func_result):
    if isgenerator(func_result):
        for r in func_result:
            yield r
    elif isasyncgen(func_result):
        async for r in func_result:
            yield r
    else:
        raise TrsansoforTypeError("func_result must be generator or async generator")