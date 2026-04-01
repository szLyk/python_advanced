"""
Day 13: 新闻采集模块

核心知识点应用：
- 装饰器：@timer 计时、@retry 重试、@cache_result 缓存
- 上下文管理器：APISessionManager 管理 aiohttp Session
- 异步编程：asyncio.gather 并发请求
- 生成器：流式返回新闻数据

数据源：
- NewsAPI / GNews API
- Reuters / BBC RSS 源

作者：AI Agent 工程师学习者
日期：2026-04-01
"""

import asyncio
import aiohttp
import json
import time
import hashlib
from functools import wraps
from contextlib import contextmanager
from typing import AsyncGenerator, Generator, Optional
from datetime import datetime, timedelta
import random
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET

from config import (
    USE_REAL_API,
    API_KEYS,
    API_ENDPOINTS,
    API_PARAMS,
    RSS_SOURCES,
    MOCK_NEWS_COUNT,
    MOCK_NEWS_TEMPLATES,
)


# ============================================================
# 装饰器部分
# ============================================================

def timer(unit: str = 's'):
    """
    计时装饰器（支持同步和异步函数）

    Args:
        unit: 时间单位，'s'（秒）、'ms'（毫秒）、'us'（微秒）
    """
    factor = {'s': 1, 'ms': 1000, 'us': 1000000}

    def decorator(func):
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            start = time.perf_counter()
            result = await func(*args, **kwargs)
            end = time.perf_counter()
            elapsed = (end - start) * factor[unit]
            print(f"[Timer] {func.__name__} 执行时间: {elapsed:.4f} {unit}")
            return result

        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            start = time.perf_counter()
            result = func(*args, **kwargs)
            end = time.perf_counter()
            elapsed = (end - start) * factor[unit]
            print(f"[Timer] {func.__name__} 执行时间: {elapsed:.4f} {unit}")
            return result

        # 根据函数类型选择包装器
        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        return sync_wrapper

    return decorator


def retry(max_attempts: int = 3, delay: float = 1.0, exceptions: tuple = (Exception,)):
    """
    重试装饰器（支持异步函数）

    Args:
        max_attempts: 最大重试次数
        delay: 初始延迟时间（秒）
        exceptions: 需要捕获的异常类型
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            current_delay = delay
            for attempt in range(1, max_attempts + 1):
                try:
                    return await func(*args, **kwargs)
                except exceptions as e:
                    if attempt == max_attempts:
                        print(f"[Retry] {func.__name__} 重试 {max_attempts} 次后失败")
                        raise
                    print(f"[Retry] {func.__name__} 第 {attempt} 次失败: {e}")
                    await asyncio.sleep(current_delay)
                    current_delay *= 2  # 指数退避
            return None
        return wrapper
    return decorator


def cache_result(expire_seconds: int = 300):
    """
    结果缓存装饰器（基于内存的简单缓存）

    Args:
        expire_seconds: 缓存过期时间（秒）
    """
    cache_dict = {}

    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # 生成缓存键
            key_parts = [func.__name__, str(args), str(sorted(kwargs.items()))]
            cache_key = hashlib.md5(''.join(key_parts).encode()).hexdigest()

            # 检查缓存
            if cache_key in cache_dict:
                cached_data, cached_time = cache_dict[cache_key]
                if time.time() - cached_time < expire_seconds:
                    print(f"[Cache] {func.__name__} 使用缓存数据")
                    return cached_data

            # 执行函数并缓存结果
            result = await func(*args, **kwargs)
            cache_dict[cache_key] = (result, time.time())
            print(f"[Cache] {func.__name__} 结果已缓存")
            return result
        return wrapper
    return decorator


def rate_limit(calls_per_second: float = 2.0):
    """
    限速装饰器（防止 API 被封）

    Args:
        calls_per_second: 每秒最大调用次数
    """
    min_interval = 1.0 / calls_per_second
    last_call_time = {}

    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            func_name = func.__name__
            now = time.time()

            # 检查上次调用时间
            if func_name in last_call_time:
                elapsed = now - last_call_time[func_name]
                if elapsed < min_interval:
                    wait_time = min_interval - elapsed
                    print(f"[RateLimit] {func_name} 等待 {wait_time:.2f}s")
                    await asyncio.sleep(wait_time)

            last_call_time[func_name] = time.time()
            return await func(*args, **kwargs)
        return wrapper
    return decorator


# ============================================================
# 上下文管理器部分
# ============================================================

class APISessionManager:
    """
    异步 API Session 管理器（类实现）

    功能：
    - 自动创建和关闭 aiohttp ClientSession
    - 统计请求次数、成功/失败数
    """

    def __init__(self, name: str = "API"):
        self.name = name
        self.session: Optional[aiohttp.ClientSession] = None
        self.stats = {
            'requests': 0,
            'success': 0,
            'failed': 0,
            'start_time': None,
        }

    async def __aenter__(self):
        print(f"[{self.name}] 创建 aiohttp Session")
        self.session = aiohttp.ClientSession()
        self.stats['start_time'] = time.time()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        print(f"[{self.name}] 关闭 aiohttp Session")
        if self.session:
            await self.session.close()

        # 输出统计信息
        duration = time.time() - self.stats['start_time']
        print(f"[{self.name}] 统计: 耗时 {duration:.2f}s, "
              f"请求 {self.stats['requests']}, "
              f"成功 {self.stats['success']}, "
              f"失败 {self.stats['failed']}")


@contextmanager
def fetch_stats_context() -> Generator[dict, None, None]:
    """
    采集统计上下文管理器（@contextmanager 实现）

    功能：
    - 记录采集开始/结束时间
    - 统计采集数据量
    """
    stats = {
        'start_time': time.time(),
        'news_count': 0,
        'sources': [],
        'requests': 0,
        'success': 0,
        'failed': 0,
    }
    print("[Stats] 新闻采集开始")
    try:
        yield stats
    finally:
        stats['end_time'] = time.time()
        stats['duration'] = stats['end_time'] - stats['start_time']
        print(f"[Stats] 新闻采集结束，耗时 {stats['duration']:.2f}s，"
              f"采集 {stats['news_count']} 条新闻，来源: {stats['sources']}")


# ============================================================
# 生成器部分
# ============================================================

def chunk_sources(sources: list, chunk_size: int) -> Generator[list, None, None]:
    """
    生成器：分批处理数据源

    Args:
        sources: 数据源列表
        chunk_size: 每批数量
    """
    for i in range(0, len(sources), chunk_size):
        yield sources[i:i + chunk_size]


async def stream_news_results(results: list) -> AsyncGenerator[dict, None]:
    """
    异步生成器：流式返回新闻结果

    Args:
        results: 新闻结果列表
    """
    for result in results:
        await asyncio.sleep(0.01)  # 模拟处理延迟
        if result and result.get('status') == 'success':
            yield result


# ============================================================
# 模拟数据生成
# ============================================================

def generate_mock_news(count: int = MOCK_NEWS_COUNT) -> list:
    """
    生成模拟新闻数据

    Args:
        count: 新闻数量

    Returns:
        新闻列表
    """
    print(f"[Mock] 生成 {count} 条模拟新闻")

    news_list = []
    base_date = datetime.now() - timedelta(days=count)

    for i in range(count):
        # 从模板随机选择
        template_idx = i % len(MOCK_NEWS_TEMPLATES)
        title, base_sentiment = MOCK_NEWS_TEMPLATES[template_idx]

        # 添加随机变化
        random_factor = random.uniform(-0.1, 0.1)
        sentiment = base_sentiment + random_factor
        sentiment = max(-1.0, min(1.0, sentiment))  # 限制在 [-1, 1]

        # 生成日期（每天1-3条新闻）
        days_offset = i // 3
        hours_offset = (i % 3) * 8
        published_at = base_date + timedelta(days=days_offset, hours=hours_offset)

        # 构建新闻数据
        news = {
            'title': title,
            'description': f"Detailed analysis: {title}. Market experts provide insights on potential impacts.",
            'source': random.choice(['Reuters', 'Bloomberg', 'CNBC', 'MarketWatch', 'Yahoo Finance']),
            'published_at': published_at.isoformat(),
            'url': f"https://example.com/news/{i}",
            'sentiment_hint': sentiment,  # 模拟数据自带情绪提示
        }
        news_list.append(news)

    return news_list


# ============================================================
# API 调用
# ============================================================

@timer(unit='s')
@retry(max_attempts=3, delay=1.0)
@rate_limit(calls_per_second=1.0)
async def fetch_from_api(
    session: aiohttp.ClientSession,
    api_name: str,
    stats: dict
) -> dict:
    """
    从 API 获取新闻数据

    Args:
        session: aiohttp Session
        api_name: API 名称 ('newsapi' 或 'gnews')
        stats: 统计字典

    Returns:
        API 响应数据
    """
    if not API_KEYS.get(api_name):
        print(f"[API] {api_name} 未配置 API Key")
        return {'status': 'failed', 'error': 'no_api_key', 'source': api_name}

    url = API_ENDPOINTS[api_name]
    params = API_PARAMS[api_name].copy()
    params['apiKey'] = API_KEYS[api_name] if api_name == 'newsapi' else None
    params['token'] = API_KEYS[api_name] if api_name == 'gnews' else None

    stats['requests'] += 1

    try:
        async with session.get(url, params=params, timeout=aiohttp.ClientTimeout(total=10)) as response:
            data = await response.json()

            if response.status == 200:
                stats['success'] += 1
                return {
                    'status': 'success',
                    'source': api_name,
                    'data': data,
                    'count': len(data.get('articles', [])),
                }
            else:
                stats['failed'] += 1
                return {
                    'status': 'failed',
                    'error': f'http_{response.status}',
                    'source': api_name,
                }

    except asyncio.TimeoutError:
        stats['failed'] += 1
        return {'status': 'failed', 'error': 'timeout', 'source': api_name}
    except Exception as e:
        stats['failed'] += 1
        return {'status': 'failed', 'error': str(e), 'source': api_name}


# ============================================================
# 主采集类
# ============================================================

class NewsFetcher:
    """
    新闻采集器 - 综合运用所有知识点
    """

    def __init__(self):
        self.news_data = []

    @timer(unit='s')
    async def fetch_all(self) -> list:
        """
        采集所有新闻数据（主入口）
        """
        with fetch_stats_context() as stats:
            if USE_REAL_API:
                # 使用真实 API
                news = await self._fetch_from_real_api(stats)
            else:
                # 使用模拟数据
                news = await self._fetch_from_mock(stats)

            stats['news_count'] = len(news)
            self.news_data = news
            return news

    async def _fetch_from_real_api(self, stats: dict) -> list:
        """
        从真实 API 和 RSS 源获取数据
        """
        all_news = []

        # 1. 获取 API 数据
        api_sources = ['gnews']  # 可以添加 'newsapi'
        for api_name in api_sources:
            if API_KEYS.get(api_name):
                print(f"[API] 正在请求 {api_name}...")
                try:
                    result = self._fetch_sync(api_name, stats)
                    if result['status'] == 'success':
                        stats['sources'].append(api_name)
                        articles = result['data'].get('articles', [])
                        all_news.extend(self._normalize_articles(articles, api_name))
                        print(f"[API] {api_name} 返回 {len(articles)} 条新闻")
                except Exception as e:
                    print(f"[API] {api_name} 请求失败: {e}")

        # 2. 获取 RSS 数据
        rss_sources = ['bbc_business', 'cnbc_markets', 'marketwatch']  # 可添加更多
        for rss_name in rss_sources:
            if rss_name in RSS_SOURCES:
                print(f"[RSS] 正在获取 {RSS_SOURCES[rss_name]['name']}...")
                try:
                    articles = self._fetch_rss(rss_name, stats)
                    if articles:
                        stats['sources'].append(rss_name)
                        all_news.extend(articles)
                        print(f"[RSS] {RSS_SOURCES[rss_name]['name']} 返回 {len(articles)} 条新闻")
                except Exception as e:
                    print(f"[RSS] {rss_name} 获取失败: {e}")

        return all_news

    def _fetch_rss(self, rss_name: str, stats: dict) -> list:
        """
        获取并解析 RSS 源

        Args:
            rss_name: RSS 源名称
            stats: 统计字典

        Returns:
            标准化的新闻列表
        """
        rss_config = RSS_SOURCES.get(rss_name)
        if not rss_config:
            return []

        url = rss_config['url']
        source_name = rss_config['name']
        stats['requests'] += 1

        try:
            req = urllib.request.Request(url)
            req.add_header('User-Agent', 'Mozilla/5.0 (compatible; NewsBot/1.0)')

            with urllib.request.urlopen(req, timeout=15) as response:
                xml_content = response.read().decode('utf-8')
                stats['success'] += 1

                # 解析 XML
                articles = self._parse_rss_xml(xml_content, source_name)
                return articles

        except Exception as e:
            stats['failed'] += 1
            print(f"[RSS] 解析失败: {e}")
            return []

    def _parse_rss_xml(self, xml_content: str, source_name: str) -> list:
        """
        解析 RSS XML 内容

        Args:
            xml_content: XML 字符串
            source_name: 来源名称

        Returns:
            标准化的新闻列表
        """
        articles = []

        try:
            root = ET.fromstring(xml_content)

            # RSS 2.0 格式: rss -> channel -> item
            channel = root.find('channel')
            if channel is None:
                # Atom 格式: feed -> entry
                items = root.findall('{http://www.w3.org/2005/Atom}entry')
                for entry in items:
                    article = self._parse_atom_entry(entry, source_name)
                    if article:
                        articles.append(article)
            else:
                items = channel.findall('item')
                for item in items:
                    article = self._parse_rss_item(item, source_name)
                    if article:
                        articles.append(article)

        except ET.ParseError as e:
            print(f"[RSS] XML 解析错误: {e}")

        return articles

    def _parse_rss_item(self, item, source_name: str) -> dict:
        """
        解析 RSS item 元素

        Args:
            item: XML item 元素
            source_name: 来源名称

        Returns:
            标准化的新闻字典
        """
        title_elem = item.find('title')
        desc_elem = item.find('description')
        link_elem = item.find('link')
        pubdate_elem = item.find('pubDate')

        title = title_elem.text if title_elem is not None and title_elem.text else ''
        description = desc_elem.text if desc_elem is not None and desc_elem.text else ''
        link = link_elem.text if link_elem is not None and link_elem.text else ''
        pub_date = pubdate_elem.text if pubdate_elem is not None and pubdate_elem.text else ''

        # 清理 HTML 标签
        import re
        description = re.sub(r'<[^>]+>', '', description)

        if not title:
            return None

        return {
            'title': title.strip(),
            'description': description.strip()[:500],  # 限制描述长度
            'source': source_name,
            'published_at': pub_date.strip(),
            'url': link.strip(),
        }

    def _parse_atom_entry(self, entry, source_name: str) -> dict:
        """
        解析 Atom entry 元素

        Args:
            entry: XML entry 元素
            source_name: 来源名称

        Returns:
            标准化的新闻字典
        """
        ns = {'atom': 'http://www.w3.org/2005/Atom'}

        title_elem = entry.find('atom:title', ns)
        summary_elem = entry.find('atom:summary', ns)
        link_elem = entry.find('atom:link', ns)
        published_elem = entry.find('atom:published', ns)

        title = title_elem.text if title_elem is not None and title_elem.text else ''
        description = summary_elem.text if summary_elem is not None and summary_elem.text else ''
        link = link_elem.get('href', '') if link_elem is not None else ''
        pub_date = published_elem.text if published_elem is not None and published_elem.text else ''

        import re
        description = re.sub(r'<[^>]+>', '', description)

        if not title:
            return None

        return {
            'title': title.strip(),
            'description': description.strip()[:500],
            'source': source_name,
            'published_at': pub_date.strip(),
            'url': link.strip(),
        }

    def _fetch_sync(self, api_name: str, stats: dict) -> dict:
        """
        同步获取 API 数据（Windows 兼容）
        """
        if not API_KEYS.get(api_name):
            print(f"[API] {api_name} 未配置 API Key")
            return {'status': 'failed', 'error': 'no_api_key', 'source': api_name}

        url = API_ENDPOINTS[api_name]
        params = API_PARAMS[api_name].copy()

        # 设置 API Key
        if api_name == 'newsapi':
            params['apiKey'] = API_KEYS[api_name]
        elif api_name == 'gnews':
            params['token'] = API_KEYS[api_name]

        stats['requests'] += 1

        try:
            full_url = url + '?' + urllib.parse.urlencode(params)
            req = urllib.request.Request(full_url)
            req.add_header('User-Agent', 'Mozilla/5.0')

            with urllib.request.urlopen(req, timeout=15) as response:
                data = json.loads(response.read().decode())
                stats['success'] += 1
                return {
                    'status': 'success',
                    'source': api_name,
                    'data': data,
                    'count': len(data.get('articles', [])),
                }

        except Exception as e:
            stats['failed'] += 1
            return {'status': 'failed', 'error': str(e), 'source': api_name}

    async def _fetch_from_mock(self, stats: dict) -> list:
        """
        使用模拟数据（异步包装）
        """
        stats['sources'].append('mock_data')
        await asyncio.sleep(0.1)  # 模拟网络延迟
        return generate_mock_news()

    def _normalize_articles(self, articles: list, source: str) -> list:
        """
        标准化 API 返回的文章数据
        """
        normalized = []
        for article in articles:
            normalized.append({
                'title': article.get('title', ''),
                'description': article.get('description', ''),
                'source': source,
                'published_at': article.get('publishedAt', ''),
                'url': article.get('url', ''),
            })
        return normalized

    def get_news_stream(self) -> Generator[dict, None, None]:
        """
        生成器：流式返回新闻数据
        """
        for news in self.news_data:
            yield news


# ============================================================
# 测试用例
# ============================================================

async def test_decorators():
    """测试装饰器"""
    print("\n" + "=" * 50)
    print("测试装饰器")
    print("=" * 50)

    @timer(unit='ms')
    async def slow_task():
        await asyncio.sleep(0.1)
        return "完成"

    result = await slow_task()
    print(f"结果: {result}")


async def test_context_manager():
    """测试上下文管理器"""
    print("\n" + "=" * 50)
    print("测试上下文管理器")
    print("=" * 50)

    async with APISessionManager("Test") as manager:
        print(f"Session 创建成功: {manager.session is not None}")
        manager.stats['requests'] = 1
        manager.stats['success'] = 1


async def test_mock_fetcher():
    """测试模拟数据采集"""
    print("\n" + "=" * 50)
    print("测试模拟数据采集")
    print("=" * 50)

    fetcher = NewsFetcher()
    news = await fetcher.fetch_all()

    print(f"\n采集到 {len(news)} 条新闻")
    print("\n前 3 条新闻:")
    for i, n in enumerate(news[:3]):
        print(f"  {i+1}. {n['title']} ({n['source']})")


async def test_generator():
    """测试生成器"""
    print("\n" + "=" * 50)
    print("测试生成器流式处理")
    print("=" * 50)

    fetcher = NewsFetcher()
    await fetcher.fetch_all()

    print("\n流式输出前 5 条:")
    count = 0
    for news in fetcher.get_news_stream():
        if count >= 5:
            break
        print(f"  {news['title']}")
        count += 1


# ============================================================
# 主程序
# ============================================================

async def main():
    """运行所有测试"""
    print("=" * 60)
    print("Day 13: news_fetcher.py 模块测试")
    print("=" * 60)

    await test_decorators()
    await test_context_manager()
    await test_mock_fetcher()
    await test_generator()

    print("\n" + "=" * 60)
    print("✅ news_fetcher.py 模块测试完成！")
    print("=" * 60)
    print("""
知识点应用总结：
1. ✅ 装饰器：@timer 计时、@retry 重试、@rate_limit 限速、@cache_result 缓存
2. ✅ 上下文管理器：APISessionManager（类实现）、fetch_stats_context（@contextmanager）
3. ✅ 异步编程：asyncio.gather 并发请求、aiohttp 异步 HTTP
4. ✅ 生成器：get_news_stream 流式返回、chunk_sources 分批处理
    """)


if __name__ == "__main__":
    asyncio.run(main())