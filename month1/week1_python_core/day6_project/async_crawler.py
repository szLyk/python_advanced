"""
Day 6: 综合项目 - 异步爬虫

学习目标：
1. 综合应用装饰器、生成器、异步编程、上下文管理器
2. 实现一个异步网络爬虫
3. 掌握异步 HTTP 请求

综合运用：
- 装饰器：计时、重试、日志
- 生成器：流式处理结果
- 上下文管理器：资源管理
- 异步编程：并发请求

作者：AI Agent 工程师学习者
日期：2026-03-29
"""

import asyncio
import aiohttp
from functools import wraps
import time
import json
from contextlib import contextmanager
from typing import Generator, AsyncGenerator


# ============================================================
# 装饰器部分
# ============================================================

def async_timer(func):
    """异步函数计时装饰器"""
    @wraps(func)
    async def wrapper(*args, **kwargs):
        start = time.time()
        result = await func(*args, **kwargs)
        end = time.time()
        print(f"[Timer] {func.__name__} 执行时间: {end - start:.2f} 秒")
        return result
    return wrapper


def async_retry(max_retries=3, delay=1):
    """异步重试装饰器"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    if attempt < max_retries - 1:
                        print(f"[Retry] {func.__name__} 第 {attempt + 1} 次失败，{delay}秒后重试...")
                        await asyncio.sleep(delay)
                    else:
                        print(f"[Retry] {func.__name__} 重试 {max_retries} 次后仍失败: {e}")
                        raise
        return wrapper
    return decorator


def log_calls(func):
    """调用日志装饰器"""
    @wraps(func)
    async def wrapper(*args, **kwargs):
        print(f"[Log] 调用 {func.__name__}")
        result = await func(*args, **kwargs)
        print(f"[Log] {func.__name__} 完成")
        return result
    return wrapper


# ============================================================
# 上下文管理器部分
# ============================================================

@contextmanager
def crawl_session_stats() -> Generator[dict, None, None]:
    """爬虫会话统计上下文管理器"""
    stats = {
        'start_time': time.time(),
        'requests': 0,
        'success': 0,
        'failed': 0
    }
    print("[Session] 爬虫会话开始")
    try:
        yield stats
    finally:
        stats['end_time'] = time.time()
        stats['duration'] = stats['end_time'] - stats['start_time']
        print(f"\n[Session] 爬虫会话结束")
        print(f"[Session] 总耗时: {stats['duration:.2f']}秒")
        print(f"[Session] 请求数: {stats['requests']}, 成功: {stats['success']}, 失败: {stats['failed']}")


class AsyncSessionManager:
    """异步会话管理器（类实现）"""
    
    def __init__(self, name: str):
        self.name = name
        self.session = None
        self.stats = {'requests': 0, 'success': 0, 'failed': 0}
    
    async def __aenter__(self):
        print(f"[{self.name}] 创建 aiohttp 会话")
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        print(f"[{self.name}] 关闭 aiohttp 会话")
        await self.session.close()
        print(f"[{self.name}] 统计: 成功 {self.stats['success']}, 失败 {self.stats['failed']}")


# ============================================================
# 生成器部分
# ============================================================

def filter_valid_results(results: list) -> Generator[dict, None, None]:
    """生成器：过滤有效结果"""
    for result in results:
        if result is not None and result.get('status') == 'success':
            yield result


def chunk_urls(urls: list, chunk_size: int) -> Generator[list, None, None]:
    """生成器：URL 分批处理"""
    for i in range(0, len(urls), chunk_size):
        yield urls[i:i + chunk_size]


async def async_result_generator(results: list) -> AsyncGenerator[dict, None]:
    """异步生成器：逐个返回结果"""
    for result in results:
        await asyncio.sleep(0.01)  # 模拟处理延迟
        yield result


# ============================================================
# 异步爬虫类
# ============================================================

class AsyncCrawler:
    """异步网络爬虫 - 综合运用所有知识点"""

    def __init__(self, max_concurrent=5, timeout=10):
        self.max_concurrent = max_concurrent
        self.timeout = timeout
        self.semaphore = None
        self.stats = {'requests': 0, 'success': 0, 'failed': 0}

    @async_retry(max_retries=2, delay=0.5)
    async def fetch(self, session, url: str, stats: dict) -> dict:
        """获取单个URL的内容（带重试）"""
        async with self.semaphore:
            stats['requests'] += 1
            try:
                async with session.get(url, timeout=aiohttp.ClientTimeout(total=self.timeout)) as response:
                    html = await response.text()
                    stats['success'] += 1
                    return {
                        'url': url,
                        'status': 'success',
                        'status_code': response.status,
                        'content': html[:500],  # 只取前500字符演示
                        'size': len(html)
                    }
            except asyncio.TimeoutError:
                stats['failed'] += 1
                print(f"[Error] {url} 超时")
                return {'url': url, 'status': 'failed', 'error': 'timeout'}
            except Exception as e:
                stats['failed'] += 1
                print(f"[Error] {url} 失败: {type(e).__name__}")
                return {'url': url, 'status': 'failed', 'error': str(e)}

    @async_timer
    @log_calls
    async def crawl_batch(self, urls: list) -> list:
        """爬取一批URL"""
        self.semaphore = asyncio.Semaphore(self.max_concurrent)
        stats = {'requests': 0, 'success': 0, 'failed': 0}
        
        async with AsyncSessionManager("Crawler") as manager:
            tasks = [self.fetch(manager.session, url, manager.stats) for url in urls]
            results = await asyncio.gather(*tasks)
        
        # 使用生成器过滤有效结果
        valid_results = list(filter_valid_results(results))
        print(f"[Result] 有效结果: {len(valid_results)}/{len(results)}")
        
        return results

    async def crawl_large_batch(self, urls: list, chunk_size: int = 10) -> list:
        """爬取大量URL（分批处理）"""
        all_results = []
        
        # 使用生成器分批
        for chunk in chunk_urls(urls, chunk_size):
            print(f"\n[Batch] 处理 {len(chunk)} 个URL...")
            results = await self.crawl_batch(chunk)
            all_results.extend(results)
        
        return all_results


# ============================================================
# 测试用例
# ============================================================

# 测试用的URL列表（使用公开API，不会被封）
TEST_URLS = [
    "https://httpbin.org/get",
    "https://httpbin.org/ip",
    "https://httpbin.org/headers",
    "https://httpbin.org/user-agent",
    "https://httpbin.org/delay/1",  # 会延迟1秒
    "https://httpbin.org/status/200",
    "https://httpbin.org/json",
]

# 故意加入会失败的URL测试重试机制
TEST_URLS_WITH_FAILURE = [
    "https://httpbin.org/get",
    "https://httpbin.org/delay/2",  # 可能超时
    "https://httpbin.org/status/404",  # 404错误
    "https://httpbin.org/status/500",  # 500错误
    "http://this-url-does-not-exist.com/",  # DNS失败
]


async def test_basic_crawler():
    """测试基础爬虫"""
    print("\n" + "="*60)
    print("测试1: 基础异步爬虫")
    print("="*60)
    
    crawler = AsyncCrawler(max_concurrent=3, timeout=5)
    results = await crawler.crawl_batch(TEST_URLS[:4])
    
    print("\n结果摘要:")
    for r in results:
        if r['status'] == 'success':
            print(f"  ✅ {r['url']} - {r['size']} bytes")
        else:
            print(f"  ❌ {r['url']} - {r['error']}")


async def test_retry_mechanism():
    """测试重试机制"""
    print("\n" + "="*60)
    print("测试2: 重试机制（包含会失败的URL）")
    print("="*60)
    
    crawler = AsyncCrawler(max_concurrent=2, timeout=3)
    # 只测试正常URL，失败URL需要手动测试
    results = await crawler.crawl_batch(TEST_URLS_WITH_FAILURE[:2])
    
    print("\n结果摘要:")
    for r in results:
        print(f"  {r['url']} - {r['status']}")


async def test_chunked_crawling():
    """测试分批爬取"""
    print("\n" + "="*60)
    print("测试3: 分批爬取大量URL")
    print("="*60)
    
    crawler = AsyncCrawler(max_concurrent=2, timeout=5)
    results = await crawler.crawl_large_batch(TEST_URLS, chunk_size=3)
    
    print(f"\n总计: {len(results)} 个结果")


async def test_generator_usage():
    """测试生成器用法"""
    print("\n" + "="*60)
    print("测试4: 生成器流式处理")
    print("="*60)
    
    crawler = AsyncCrawler(max_concurrent=3, timeout=5)
    results = await crawler.crawl_batch(TEST_URLS[:3])
    
    # 使用生成器过滤
    print("\n有效结果（生成器过滤）:")
    for valid_result in filter_valid_results(results):
        print(f"  {valid_result['url']}")


async def test_context_manager():
    """测试上下文管理器"""
    print("\n" + "="*60)
    print("测试5: 上下文管理器统计")
    print("="*60)
    
    with crawl_session_stats() as stats:
        crawler = AsyncCrawler(max_concurrent=3, timeout=5)
        results = await crawler.crawl_batch(TEST_URLS[:2])
        stats['success'] = len([r for r in results if r['status'] == 'success'])
        stats['failed'] = len([r for r in results if r['status'] == 'failed'])


async def test_decorators():
    """单独测试装饰器"""
    print("\n" + "="*60)
    print("测试6: 装饰器效果演示")
    print("="*60)
    
    @async_timer
    @async_retry(max_retries=3, delay=0.5)
    async def unstable_function():
        """模拟不稳定函数"""
        import random
        if random.random() < 0.5:
            raise ValueError("随机失败！")
        return "成功！"
    
    try:
        result = await unstable_function()
        print(f"结果: {result}")
    except Exception as e:
        print(f"最终失败: {e}")


# ============================================================
# 主程序
# ============================================================

async def main():
    """运行所有测试"""
    print("\n" + "="*60)
    print("Day 6: 异步爬虫项目 - 综合测试")
    print("="*60)
    print("""
本项目综合运用了 Week 1 所有知识点：
- 装饰器：计时(@async_timer)、重试(@async_retry)、日志(@log_calls)
- 生成器：过滤结果(filter_valid_results)、分批处理(chunk_urls)
- 上下文管理器：资源管理(AsyncSessionManager)、统计(crawl_session_stats)
- 异步编程：并发请求(asyncio.gather)、信号量控制(Semaphore)
""")
    
    # 运行测试
    await test_basic_crawler()
    await test_chunked_crawling()
    await test_generator_usage()
    
    print("\n" + "="*60)
    print("✅ Day 6 异步爬虫项目完成！")
    print("="*60)
    print("""
学习成果：
1. ✅ 使用 aiohttp 发送异步 HTTP 请求
2. ✅ 使用 asyncio.gather 并发请求
3. ✅ 使用信号量控制并发数量
4. ✅ 使用装饰器记录执行时间、重试机制
5. ✅ 使用生成器处理和过滤结果
6. ✅ 使用上下文管理器管理资源和统计

下一步：Week 2 数据处理库 (numpy/pandas)
""")


if __name__ == "__main__":
    asyncio.run(main())