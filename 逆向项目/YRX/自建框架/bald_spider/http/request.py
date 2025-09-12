from typing import Dict, Optional,Callable


class Request:
    def __init__(self,
                 url: str, *,
                 header: Optional[Dict] = None,
                 priority: int = 0,  # 设计优先级
                 method: str = "GET",
                 cookies: Optional[Dict] = None,
                 proxy: Optional[str] = None,
                 body: Optional[str] = None,
                 callback: Optional[Callable] = None

                 ):
        self.url = url
        self.header = header
        self.priority = priority
        self.method = method
        self.cookies = cookies
        self.proxy = proxy
        self.body = body
        self.callback = callback
    def __repr__(self):
        return f"Request(url={self.url}, method={self.method}, priority={self.priority})"

    #魔法方法

    def __lt__(self,other):
        return self.priority < other.priority
