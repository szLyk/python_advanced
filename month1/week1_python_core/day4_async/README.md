# Day 4: 异步编程 (Async Programming)

## 学习目标
- [x] 理解 `async/await` 语法
- [x] 掌握 `asyncio` 基础
- [x] 学会协程的使用
- [x] 掌握并发执行多个任务
- [x] 熟悉常用异步 API

## 目录

- [1. 异步编程基础](#1-异步编程基础)
- [2. async/await 语法](#2-asyncawait-语法)
- [3. 常用 asyncio API](#3-常用-asyncio-api)
- [4. 实战示例](#4-实战示例)
- [5. 最佳实践](#5-最佳实践)

---

## 1. 异步编程基础

### 同步 vs 异步

| 特性 | 同步 (Synchronous) | 异步 (Asynchronous) |
|------|-------------------|-------------------|
| **执行方式** | 顺序执行 | 并发执行 |
| **阻塞** | 阻塞等待 | 非阻塞 |
| **效率** | I/O 等待浪费时间 | I/O 等待时处理其他任务 |
| **适用场景** | CPU 密集型 | I/O 密集型 |

### 为什么需要异步？

```python
# 同步方式 - 耗时 3 秒
import time

def sync_download():
    time.sleep(1)  # 下载 1
    time.sleep(1)  # 下载 2
    time.sleep(1)  # 下载 3
    # 总耗时：3 秒

# 异步方式 - 耗时 1 秒
async def async_download():
    await asyncio.sleep(1)  # 下载 1
    await asyncio.sleep(1)  # 下载 2
    await asyncio.sleep(1)  # 下载 3
    # 并发执行，总耗时：1 秒
```

---

## 2. async/await 语法

### 2.1 定义协程

```python
# 使用 async 定义协程
async def my_coroutine():
    """这是一个协程函数"""
    return "Hello"

# 调用协程
coro = my_coroutine()  # 返回协程对象，不会执行
print(type(coro))  # <class 'coroutine'>

# 必须使用 await 或 asyncio.run() 执行
result = asyncio.run(my_coroutine())
```

### 2.2 await 关键字

```python
async def fetch_data():
    # await 只能用于可等待对象（协程、Task、Future）
    result = await some_async_function()
    return result

async def main():
    # await 必须在 async 函数中使用
    data = await fetch_data()
```

### 2.3 错误示例

```python
# ❌ 错误：在普通函数中使用 await
def normal_function():
    await fetch_data()  # SyntaxError!

# ✅ 正确：在 async 函数中使用 await
async def async_function():
    await fetch_data()

# ❌ 错误：直接调用协程不等待
async def bad_code():
    my_coroutine()  # 协程不会执行！

# ✅ 正确：使用 await 等待协程
async def good_code():
    await my_coroutine()
```

---

## 3. 常用 asyncio API

### 3.1 运行协程

#### `asyncio.run()`

```python
# Python 3.7+ 推荐使用
asyncio.run(main())

# 等价于
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
try:
    loop.run_until_complete(main())
finally:
    loop.close()
```

#### `loop.run_until_complete()`

```python
import asyncio

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close()
```

---

### 3.2 任务管理

#### `asyncio.create_task()`

```python
# 创建后台任务
async def background_task():
    await asyncio.sleep(1)
    return "done"

async def main():
    # 立即执行，不等待
    task = asyncio.create_task(background_task())
    
    # 可以做其他事情
    await asyncio.sleep(0.5)
    
    # 等待任务完成
    result = await task
```

#### `asyncio.gather()`

```python
# 并发执行多个协程
async def main():
    results = await asyncio.gather(
        task1(),
        task2(),
        task3(),
    )
    # results = [result1, result2, return3]

# 忽略异常
await asyncio.gather(
    task1(),
    task2(),
    return_exceptions=True  # 异常作为结果返回
)
```

#### `asyncio.wait()`

```python
# 更细粒度的控制
done, pending = await asyncio.wait(
    [task1(), task2(), task3()],
    timeout=5.0,  # 超时时间
    return_when=asyncio.FIRST_COMPLETED  # 完成条件
)

# return_when 选项：
# - FIRST_COMPLETED: 第一个完成就返回
# - FIRST_EXCEPTION: 第一个异常就返回
# - ALL_COMPLETED: 全部完成（默认）
```

---

### 3.3 超时控制

#### `asyncio.wait_for()`

```python
# 设置超时
try:
    result = await asyncio.wait_for(
        slow_operation(),
        timeout=5.0  # 5 秒超时
    )
except asyncio.TimeoutError:
    print("操作超时")
```

---

### 3.4 锁和同步

#### `asyncio.Lock()`

```python
lock = asyncio.Lock()

async def safe_operation():
    async with lock:
        # 临界区代码
        await shared_resource.modify()
```

#### `asyncio.Semaphore()`

```python
# 限制并发数为 3
semaphore = asyncio.Semaphore(3)

async def limited_task():
    async with semaphore:
        await process()  # 最多 3 个并发
```

#### `asyncio.Queue()`

```python
# 生产者 - 消费者模式
queue = asyncio.Queue(maxsize=10)

async def producer():
    await queue.put(item)  # 放入队列

async def consumer():
    item = await queue.get()  # 从队列取出
    queue.task_done()  # 标记完成

# 等待所有任务完成
await queue.join()
```

---

### 3.5 事件和条件变量

#### `asyncio.Event()`

```python
event = asyncio.Event()

async def waiter():
    await event.wait()  # 等待事件
    print("事件触发！")

async def trigger():
    await asyncio.sleep(1)
    event.set()  # 触发事件
```

#### `asyncio.Condition()`

```python
condition = asyncio.Condition()

async def worker():
    async with condition:
        await condition.wait()  # 等待条件
        # 条件满足，继续执行
```

#### `asyncio.Barrier()`

```python
# 等待所有参与者到达
barrier = asyncio.Barrier(3)

async def worker():
    print("准备就绪")
    await barrier.wait()  # 等待其他 2 个
    print("一起开始！")
```

---

### 3.6 异常处理

#### `asyncio.exceptions`

```python
from asyncio.exceptions import TimeoutError, CancelledError

try:
    await asyncio.wait_for(task(), timeout=5)
except TimeoutError:
    print("超时")
except CancelledError:
    print("任务被取消")
```

#### 任务取消

```python
task = asyncio.create_task(long_running())

# 取消任务
task.cancel()

try:
    await task
except asyncio.CancelledError:
    print("任务已取消")
```

---

### 3.7 异步上下文管理器

#### `async with`

```python
class AsyncResource:
    async def __aenter__(self):
        await self.connect()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

async def main():
    async with AsyncResource() as resource:
        await resource.use()
```

#### `asyncio.timeout()` (Python 3.11+)

```python
async with asyncio.timeout(5.0):
    await long_operation()
```

---

### 3.8 定时器和延迟

#### `asyncio.sleep()`

```python
# 延迟执行
await asyncio.sleep(1.0)  # 等待 1 秒

# 非阻塞等待
async def wait_and_print():
    await asyncio.sleep(1)
    print("1 秒后")
```

#### `loop.call_later()`

```python
loop = asyncio.get_event_loop()

def callback():
    print("延迟调用")

# 1 秒后调用
loop.call_later(1.0, callback)
```

---

## 4. 实战示例

### 4.1 并发下载

```python
import aiohttp
import asyncio

async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()

async def main():
    urls = [
        'https://api.example.com/users',
        'https://api.example.com/posts',
        'https://api.example.com/comments',
    ]
    
    async with aiohttp.ClientSession() as session:
        tasks = [fetch(session, url) for url in urls]
        results = await asyncio.gather(*tasks)
    
    return results

asyncio.run(main())
```

### 4.2 生产者 - 消费者

```python
async def producer(queue):
    for i in range(5):
        await queue.put(f"item-{i}")
        print(f"生产：item-{i}")
        await asyncio.sleep(0.5)

async def consumer(queue):
    while True:
        item = await queue.get()
        print(f"消费：{item}")
        queue.task_done()
        await asyncio.sleep(0.8)

async def main():
    queue = asyncio.Queue(maxsize=3)
    
    producers = [asyncio.create_task(producer(queue)) for _ in range(2)]
    consumers = [asyncio.create_task(consumer(queue)) for _ in range(3)]
    
    await asyncio.gather(*producers)
    await queue.join()
    
    for c in consumers:
        c.cancel()

asyncio.run(main())
```

### 4.3 限制并发数

```python
async def limited_task(semaphore, task_id):
    async with semaphore:
        print(f"任务 {task_id} 执行")
        await asyncio.sleep(2)

async def main():
    semaphore = asyncio.Semaphore(3)  # 最多 3 个并发
    tasks = [limited_task(semaphore, i) for i in range(10)]
    await asyncio.gather(*tasks)

asyncio.run(main())
```

---

## 5. 最佳实践

### ✅ 推荐做法

1. **使用 `asyncio.run()` 运行主协程**
   ```python
   asyncio.run(main())
   ```

2. **使用 `asyncio.gather()` 并发执行**
   ```python
   results = await asyncio.gather(task1(), task2(), task3())
   ```

3. **使用 `asyncio.create_task()` 创建后台任务**
   ```python
   task = asyncio.create_task(background_work())
   ```

4. **使用 `asyncio.wait_for()` 设置超时**
   ```python
   result = await asyncio.wait_for(operation(), timeout=5.0)
   ```

5. **使用 `asyncio.Semaphore()` 限制并发**
   ```python
   async with semaphore:
       await process()
   ```

### ❌ 避免的做法

1. **不要在普通函数中使用 `await`**
   ```python
   # ❌ 错误
   def normal_func():
       await async_func()
   
   # ✅ 正确
   async def async_func_wrapper():
       await async_func()
   ```

2. **不要直接调用协程而不等待**
   ```python
   # ❌ 错误
   async def bad_code():
       my_coroutine()  # 不会执行！
   
   # ✅ 正确
   async def good_code():
       await my_coroutine()
   ```

3. **不要阻塞事件循环**
   ```python
   # ❌ 错误
   async def bad_code():
       time.sleep(1)  # 阻塞整个事件循环
   
   # ✅ 正确
   async def good_code():
       await asyncio.sleep(1)  # 非阻塞
   ```

4. **不要在异步代码中使用同步 I/O**
   ```python
   # ❌ 错误
   async def bad_code():
       with open("file.txt") as f:  # 阻塞 I/O
           content = f.read()
   
   # ✅ 正确
   async def good_code():
       async with aiofiles.open("file.txt") as f:  # 异步 I/O
           content = await f.read()
   ```

---

## 6. 常用异步库

| 库 | 用途 | 安装 |
|----|------|------|
| **aiohttp** | HTTP 客户端/服务器 | `pip install aiohttp` |
| **aiomysql** | MySQL 数据库 | `pip install aiomysql` |
| **aioredis** | Redis 客户端 | `pip install aioredis` |
| **aiofiles** | 文件 I/O | `pip install aiofiles` |
| **asyncpg** | PostgreSQL | `pip install asyncpg` |

---

## 7. 调试技巧

### 启用调试模式

```python
import asyncio

asyncio.run(main(), debug=True)

# 或
loop = asyncio.get_event_loop()
loop.set_debug(True)
```

### 查看任务状态

```python
import asyncio

tasks = asyncio.all_tasks()
print(f"运行中的任务：{len(tasks)}")

for task in tasks:
    print(f"任务：{task.get_name()} - {task.done()}")
```

---

## 练习题

- [x] 并发下载多个 URL
- [x] 生产者 - 消费者模型
- [x] 超时控制
- [x] 任务取消
- [x] 信号量控制并发数
- [x] 异步上下文管理器
- [x] 批量处理任务
- [x] 异步事件处理

---

## 学习资源

- **官方文档**: https://docs.python.org/zh-cn/3/library/asyncio.html
- **Asyncio 文档**: https://docs.python.org/zh-cn/3/library/asyncio-task.html
- **Real Python**: https://realpython.com/async-io-python/
- **B 站**: Python 高级编程（黑马程序员）

---

## 今日产出

- [x] async_basic.py（基础示例）
- [x] async_exercises.py（8 个练习示例）
- [x] README.md（详细文档）

---

**状态：** ✅ 已完成  
**最后更新:** 2026-03-26