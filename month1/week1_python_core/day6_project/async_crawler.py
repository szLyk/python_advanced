"""
Day 6: 综合项目 - 异步爬虫

学习目标：
1. 综合应用装饰器、生成器、异步编程
2. 实现一个异步网络爬虫
3. 掌握异步 HTTP 请求

作者：AI Agent 工程师学习者
日期：待定
"""

import asyncio
import aiohttp
from functools import wraps
import time


# ============================================================
# 计时装饰器
# ============================================================

def async_timer(func):
    """异步函数计时装饰器"""
    @wraps(func)
    async def wrapper(*args, **kwargs):
        start = time.time()
        result = await func(*args, **kwargs)
        end = time.time()
        print(f"[{func.__name__}] 执行时间: {end - start:.2f} 秒")
        return result
    return wrapper


# ============================================================
# 异步爬虫类
# ============================================================

class AsyncCrawler:
    """异步网络爬虫"""

    def __init__(self, max_concurrent=5):
        self.max_concurrent = max_concurrent
        self.semaphore = None

    async def fetch(self, session, url):
        """获取单个URL的内容"""
        async with self.semaphore:
            try:
                async with session.get(url) as response:
                    return await response.text()
            except Exception as e:
                print(f"获取 {url} 失败: {e}")
                return None

    @async_timer
    async def crawl(self, urls):
        """爬取多个URL"""
        self.semaphore = asyncio.Semaphore(self.max_concurrent)

        async with aiohttp.ClientSession() as session:
            tasks = [self.fetch(session, url) for url in urls]
            results = await asyncio.gather(*tasks)

        # 使用生成器过滤有效结果
        valid_results = (r for r in results if r is not None)
        return list(valid_results)


# ============================================================
# 主程序
# ============================================================

if __name__ == "__main__":
    print("Day 6: 异步爬虫项目（待完成）")
    print("=" * 50)
    print("""
项目要求：
1. 使用 aiohttp 发送异步 HTTP 请求
2. 使用 asyncio.gather 并发请求
3. 使用信号量控制并发数量
4. 使用装饰器记录执行时间
5. 使用生成器处理结果

TODO: 完成爬虫实现
    """)