# Day 6: 异步爬虫教程

## 学习目标

1. 理解网络爬虫的基本原理
2. 掌握 `aiohttp` 异步 HTTP 请求
3. 学会使用 `asyncio` 实现并发爬取
4. 综合应用装饰器、生成器、上下文管理器

## 目录

- [爬虫基础概念](#爬虫基础概念)
- [同步 vs 异步爬虫](#同步-vs-异步爬虫)
- [aiohttp 基础](#aiohttp-基础)
- [并发控制](#并发控制)
- [实战案例](#实战案例)
- [反爬虫策略](#反爬虫策略)

---

## 爬虫基础概念

### 什么是网络爬虫？

网络爬虫（Web Crawler）是一种自动化程序，用于：
- **抓取网页内容**：从互联网获取数据
- **解析数据**：提取有用的信息
- **存储数据**：保存到文件或数据库

### 爬虫工作流程

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  发送请求   │ ──▶ │  获取响应   │ ──▶ │  解析数据   │
└─────────────┘     └─────────────┘     └─────────────┘
       │                   │                   │
       ▼                   ▼                   ▼
   构造 URL           HTML/JSON          提取字段
   设置 Headers        内容存储           存储结果
```

### 爬虫常用库对比

| 库 | 类型 | 特点 | 适用场景 |
|---|---|---|---|
| `requests` | 同步 | 简单易用，API友好 | 少量请求、学习入门 |
| `aiohttp` | 异步 | 高并发，高性能 | 大量请求、生产环境 |
| `httpx` | 混合 | 同步异步都支持 | 现代项目首选 |
| `scrapy` | 框架 | 功能完整，分布式爬虫 | 大型爬虫项目 |

---

## 同步 vs 异步爬虫

### 同步爬虫（requests）

```python
import requests
import time

def sync_crawler(urls):
    """同步爬虫 - 逐个请求"""
    results = []
    for url in urls:
        response = requests.get(url)
        results.append(response.text)
    return results

# 10个URL，每个耗时1秒 = 总耗时10秒
urls = ["https://httpbin.org/delay/1"] * 10
start = time.time()
sync_crawler(urls)
print(f"同步耗时: {time.time() - start:.2f}秒")  # ~10秒
```

### 异步爬虫（aiohttp）

```python
import aiohttp
import asyncio
import time

async def async_crawler(urls):
    """异步爬虫 - 并发请求"""
    async with aiohttp.ClientSession() as session:
        tasks = [session.get(url) for url in urls]
        responses = await asyncio.gather(*tasks)
        results = [await r.text() for r in responses]
    return results

# 10个URL，并发请求 = 总耗时约1秒
urls = ["https://httpbin.org/delay/1"] * 10
start = time.time()
asyncio.run(async_crawler(urls))
print(f"异步耗时: {time.time() - start:.2f}秒")  # ~1秒
```

### 性能对比

```
同步爬虫：10个URL × 1秒 = 10秒
异步爬虫：10个URL ÷ 并发数 ≈ 1秒

性能提升：10倍！
```

---

## aiohttp 基础

### 安装

```bash
pip install aiohttp
```

### 基本用法

#### 1. GET 请求

```python
import aiohttp
import asyncio

async def fetch_get():
    async with aiohttp.ClientSession() as session:
        async with session.get('https://httpbin.org/get') as response:
            # 获取文本
            text = await response.text()

            # 获取 JSON
            json_data = await response.json()

            # 获取字节
            bytes_data = await response.read()

            # 状态码
            status = response.status

            # 响应头
            headers = response.headers

            print(f"状态码: {status}")
            print(f"JSON: {json_data}")

asyncio.run(fetch_get())
```

#### 2. POST 请求

```python
async def fetch_post():
    async with aiohttp.ClientSession() as session:
        # 发送表单数据
        data = {'key': 'value', 'name': 'test'}
        async with session.post('https://httpbin.org/post', data=data) as response:
            result = await response.json()
            print(result)

        # 发送 JSON 数据
        json_data = {'user': 'admin', 'password': '123456'}
        async with session.post('https://httpbin.org/post', json=json_data) as response:
            result = await response.json()
            print(result)

asyncio.run(fetch_post())
```

#### 3. 带参数的请求

```python
async def fetch_with_params():
    async with aiohttp.ClientSession() as session:
        # URL 参数
        params = {'page': 1, 'size': 10}
        async with session.get('https://httpbin.org/get', params=params) as response:
            print(await response.json())

        # 请求头
        headers = {'User-Agent': 'MyCrawler/1.0', 'Authorization': 'Bearer token'}
        async with session.get('https://httpbin.org/headers', headers=headers) as response:
            print(await response.json())

        # 超时设置
        timeout = aiohttp.ClientTimeout(total=10)  # 总超时10秒
        async with session.get('https://httpbin.org/delay/5', timeout=timeout) as response:
            print(await response.text())

asyncio.run(fetch_with_params())
```

### Session 管理

**重要：** `ClientSession` 应该复用，不要每个请求都创建新的！

```python
# ❌ 错误做法 - 每次创建新 Session
async def bad_example():
    for url in urls:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                # 处理响应
                pass
    # 每次创建/销毁 Session，性能差

# ✅ 正确做法 - 复用 Session
async def good_example():
    async with aiohttp.ClientSession() as session:
        for url in urls:
            async with session.get(url) as response:
                # 处理响应
                pass
    # 只创建一次 Session，性能好
```

---

## 并发控制

### 为什么需要并发控制？

```
无限制并发的问题：
1. 目标服务器压力大，可能被封 IP
2. 本地资源耗尽（内存、连接数）
3. 请求失败率上升

解决方案：使用信号量(Semaphore)限制并发数
```

### 使用 Semaphore

```python
import aiohttp
import asyncio

async def fetch_with_semaphore(session, url, semaphore):
    """带信号量限制的请求"""
    async with semaphore:  # 获取信号量
        async with session.get(url) as response:
            return await response.text()

async def controlled_crawler(urls, max_concurrent=5):
    """限制并发数的爬虫"""
    semaphore = asyncio.Semaphore(max_concurrent)

    async with aiohttp.ClientSession() as session:
        tasks = [
            fetch_with_semaphore(session, url, semaphore)
            for url in urls
        ]
        results = await asyncio.gather(*tasks)

    return results

# 示例
urls = [f"https://httpbin.org/delay/1?page={i}" for i in range(20)]
asyncio.run(controlled_crawler(urls, max_concurrent=5))
# 20个请求，并发5，总耗时约4秒（而不是20秒）
```

### asyncio.gather vs asyncio.as_completed

```python
import aiohttp
import asyncio

async def demo_gather_vs_as_completed():
    urls = ["https://httpbin.org/delay/3",
            "https://httpbin.org/delay/1",
            "https://httpbin.org/delay/2"]

    async with aiohttp.ClientSession() as session:

        # gather - 等待所有完成，按顺序返回结果
        print("使用 gather:")
        tasks = [session.get(url) for url in urls]
        responses = await asyncio.gather(*tasks)
        # 结果顺序与 urls 顺序一致

        # as_completed - 按完成顺序返回
        print("\n使用 as_completed:")
        tasks = [asyncio.create_task(session.get(url)) for url in urls]
        for coro in asyncio.as_completed(tasks):
            response = await coro
            print(f"完成: {response.url}")  # 先完成先返回

asyncio.run(demo_gather_vs_as_completed())
```

---

## 实战案例

### 案例 1：爬取新闻标题

```python
import aiohttp
import asyncio
import re

async def fetch_news(session, url):
    """爬取单个页面"""
    async with session.get(url) as response:
        return await response.text()

async def parse_news(html):
    """解析 HTML 提取标题（简单示例）"""
    # 实际应使用 BeautifulSoup 或 lxml
    titles = re.findall(r'<title>(.*?)</title>', html)
    return titles

async def news_crawler(urls):
    """新闻爬虫"""
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_news(session, url) for url in urls]
        htmls = await asyncio.gather(*tasks)

        results = []
        for url, html in zip(urls, htmls):
            titles = await parse_news(html)
            results.append({'url': url, 'titles': titles})

        return results

# 运行
urls = [
    "https://httpbin.org/html",
    "https://httpbin.org/html",
]
results = asyncio.run(news_crawler(urls))
```

### 案例 2：爬取 API 数据

```python
import aiohttp
import asyncio
import json

async def api_crawler():
    """爬取 JSON API 数据"""
    # 假设的分页 API
    base_url = "https://httpbin.org/get"

    async with aiohttp.ClientSession() as session:
        all_data = []

        # 爬取多页数据
        for page in range(1, 4):  # 3页
            params = {'page': page, 'size': 10}
            async with session.get(base_url, params=params) as response:
                data = await response.json()
                all_data.append(data)
                print(f"第 {page} 页数据获取成功")

        return all_data

asyncio.run(api_crawler())
```

### 案例 3：带重试机制

```python
import aiohttp
import asyncio
from functools import wraps

def retry(max_retries=3, delay=1):
    """重试装饰器"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    if attempt < max_retries - 1:
                        print(f"第 {attempt+1} 次失败，重试中...")
                        await asyncio.sleep(delay)
                    else:
                        raise e
        return wrapper
    return decorator

@retry(max_retries=3, delay=0.5)
async def fetch_with_retry(session, url):
    """带重试的请求"""
    async with session.get(url) as response:
        if response.status != 200:
            raise Exception(f"HTTP {response.status}")
        return await response.text()

async def robust_crawler(urls):
    """健壮的爬虫"""
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_with_retry(session, url) for url in urls]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        for url, result in zip(urls, results):
            if isinstance(result, Exception):
                print(f"❌ {url} 失败: {result}")
            else:
                print(f"✅ {url} 成功")

# 测试
urls = [
    "https://httpbin.org/get",
    "https://httpbin.org/status/500",  # 会触发重试
    "https://httpbin.org/status/404",  # 会触发重试
]
asyncio.run(robust_crawler(urls))
```

---

## 反爬虫策略

### 常见反爬虫机制

| 类型 | 原理 | 应对策略 |
|---|---|---|
| User-Agent 检测 | 检查 UA 是否为浏览器 | 设置随机 UA |
| 请求频率限制 | 限制单位时间请求数 | 添加延迟/使用代理 |
| IP 封禁 | 封禁异常 IP | 代理池轮换 |
| Cookie/Session | 需要登录状态 | 维护 Cookie |
| 验证码 | 人机验证 | OCR/打码平台 |
| JavaScript 渲染 | 动态加载内容 | Selenium/Playwright |

### 应对示例

```python
import aiohttp
import asyncio
import random

# User-Agent 池
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/91.0.4472.124',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) Firefox/89.0',
]

async def anti_detect_crawler(urls):
    """反检测爬虫"""
    async with aiohttp.ClientSession() as session:
        for url in urls:
            # 随机 User-Agent
            headers = {'User-Agent': random.choice(USER_AGENTS)}

            # 添加随机延迟
            await asyncio.sleep(random.uniform(0.5, 2))

            async with session.get(url, headers=headers) as response:
                print(f"状态: {response.status}")
                # 处理响应...

# 代理示例
async def proxy_crawler(url, proxy="http://127.0.0.1:7890"):
    """使用代理"""
    async with aiohttp.ClientSession() as session:
        async with session.get(url, proxy=proxy) as response:
            return await response.text()
```

### 爬虫礼仪

```
✅ 遵守 robots.txt
✅ 合理的请求频率
✅ 添加 User-Agent 标识
✅ 避免高峰期爬取
✅ 不爬取敏感信息
✅ 数据仅用于学习/研究
```

---

## 本项目综合运用

本项目代码 `async_crawler.py` 综合运用了 Week 1 所有知识点：

### 装饰器应用

```python
@async_timer          # 计时装饰器
@async_retry(3)       # 重试装饰器
@log_calls            # 日志装饰器
async def fetch():
    ...
```

### 生成器应用

```python
# 过滤有效结果
for valid in filter_valid_results(results):
    process(valid)

# 分批处理
for chunk in chunk_urls(urls, 10):
    await crawl_batch(chunk)
```

### 上下文管理器应用

```python
# 资源管理
async with AsyncSessionManager("Crawler") as manager:
    # 自动管理 session
    ...

# 统计信息
with crawl_session_stats() as stats:
    ...
    # 自动打印统计
```

### 异步编程应用

```python
# 并发请求
results = await asyncio.gather(*tasks)

# 并发控制
async with semaphore:
    await fetch()
```

---

## 练习题

### 练习 1：基础爬虫
编写一个爬虫，爬取 `https://httpbin.org/get` 并打印返回的 JSON。

### 练习 2：并发爬虫
使用 `asyncio.gather` 并发爬取 10 个 URL，计时对比同步爬虫。

### 练习 3：限速爬虫
使用 Semaphore 限制并发数为 3，爬取 20 个 URL。

### 练习 4：健壮爬虫
为爬虫添加重试机制，最多重试 3 次，每次间隔 1 秒。

### 练习 5：分页爬虫
编写一个爬虫，爬取一个分页 API 的前 10 页数据。

---

## 运行项目

```bash
# 进入项目目录
cd month1/week1_python_core/day6_project

# 运行爬虫
python async_crawler.py
```

## 预期输出

```
============================================================
Day 6: 异步爬虫项目 - 综合测试
============================================================

本项目综合运用了 Week 1 所有知识点：
- 装饰器：计时(@async_timer)、重试(@async_retry)、日志(@log_calls)
- 生成器：过滤结果(filter_valid_results)、分批处理(chunk_urls)
- 上下文管理器：资源管理(AsyncSessionManager)、统计(crawl_session_stats)
- 异步编程：并发请求(asyncio.gather)、信号量控制(Semaphore)

============================================================
测试1: 基础异步爬虫
============================================================
[Log] 调用 crawl_batch
[Crawler] 创建 aiohttp 会话
[Crawler] 关闭 aiohttp 会话
[Timer] crawl_batch 执行时间: 1.19 秒
[Log] crawl_batch 完成

✅ Day 6 异步爬虫项目完成！
```

---

## 扩展阅读

- [aiohttp 官方文档](https://docs.aiohttp.org/)
- [asyncio 官方文档](https://docs.python.org/zh-cn/3/library/asyncio.html)
- [Python 爬虫实战](https://www.bilibili.com/video/BV1...B站教程)

---

**学习成果：**
- ✅ 理解爬虫工作原理
- ✅ 掌握 aiohttp 异步请求
- ✅ 学会并发控制
- ✅ 综合运用装饰器、生成器、上下文管理器
- ✅ 完成异步爬虫项目

**下一步：Week 2 数据处理库 (numpy/pandas)**
