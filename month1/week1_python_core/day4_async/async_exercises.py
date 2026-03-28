"""
Day 4: 异步编程练习示例

包含多个实用的异步编程练习场景
"""

import asyncio
import aiohttp
import time
from typing import List


# ============================================================
# 练习 1: 并发下载多个 URL
# ============================================================

async def fetch_url(session: aiohttp.ClientSession, url: str, delay: int = 1) -> str:
    """模拟从 URL 获取数据"""
    print(f"开始获取：{url}")
    await asyncio.sleep(delay)  # 模拟网络延迟
    print(f"完成获取：{url}")
    return f"数据来自 {url}"


async def exercise1_download_urls():
    """练习 1：并发下载多个 URL"""
    print("\n" + "=" * 50)
    print("练习 1：并发下载多个 URL")
    print("=" * 50)
    
    urls = [
        "https://api.example.com/users",
        "https://api.example.com/posts",
        "https://api.example.com/comments",
        "https://api.example.com/photos",
    ]
    
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_url(session, url, delay=i % 2 + 1) for i, url in enumerate(urls)]
        results = await asyncio.gather(*tasks)
    
    print(f"\n下载结果：{results}")


# ============================================================
# 练习 2: 生产者 - 消费者模型
# ============================================================

async def producer(queue: asyncio.Queue, name: str):
    """生产者：生产数据"""
    for i in range(5):
        item = f"{name}-产品-{i}"
        await queue.put(item)
        print(f"📦 {name} 生产：{item}")
        await asyncio.sleep(0.5)
    
    # 生产完成标记
    await queue.put(None)


async def consumer(queue: asyncio.Queue, name: str):
    """消费者：消费数据"""
    while True:
        item = await queue.get()
        
        if item is None:  # 完成标记
            queue.task_done()
            print(f"🛒 {name} 收到完成标记")
            break
        
        print(f"🛒 {name} 消费：{item}")
        await asyncio.sleep(0.8)  # 消费需要时间
        queue.task_done()


async def exercise2_producer_consumer():
    """练习 2：生产者 - 消费者模型"""
    print("\n" + "=" * 50)
    print("练习 2：生产者 - 消费者模型")
    print("=" * 50)
    
    queue = asyncio.Queue(maxsize=3)
    
    # 创建生产者和消费者
    producers = [
        asyncio.create_task(producer(queue, "工厂 A")),
        asyncio.create_task(producer(queue, "工厂 B")),
    ]
    
    consumers = [
        asyncio.create_task(consumer(queue, "商店 1")),
        asyncio.create_task(consumer(queue, "商店 2")),
    ]
    
    # 等待所有生产者完成
    await asyncio.gather(*producers)
    
    # 等待队列处理完成
    await queue.join()
    
    # 取消所有消费者
    for c in consumers:
        c.cancel()


# ============================================================
# 练习 3: 超时控制
# ============================================================

async def slow_operation(delay: float) -> str:
    """模拟慢速操作"""
    await asyncio.sleep(delay)
    return f"操作完成（耗时 {delay} 秒）"


async def exercise3_timeout_control():
    """练习 3：超时控制"""
    print("\n" + "=" * 50)
    print("练习 3：超时控制")
    print("=" * 50)
    
    # 场景 1：操作在超时时间内完成
    try:
        result = await asyncio.wait_for(
            slow_operation(2.0),
            timeout=5.0
        )
        print(f"✅ {result}")
    except asyncio.TimeoutError:
        print("❌ 操作超时")
    
    # 场景 2：操作超时
    try:
        result = await asyncio.wait_for(
            slow_operation(5.0),
            timeout=2.0
        )
        print(f"✅ {result}")
    except asyncio.TimeoutError:
        print("❌ 操作超时（预期）")


# ============================================================
# 练习 4: 任务取消
# ============================================================

async def long_running_task(name: str, duration: float):
    """长时间运行的任务"""
    try:
        for i in range(int(duration)):
            print(f"任务 {name} 执行中... {i+1}/{int(duration)}")
            await asyncio.sleep(1)
        return f"任务 {name} 完成"
    except asyncio.CancelledError:
        print(f"⚠️ 任务 {name} 被取消")
        raise


async def exercise4_task_cancellation():
    """练习 4：任务取消"""
    print("\n" + "=" * 50)
    print("练习 4：任务取消")
    print("=" * 50)
    
    # 创建任务
    task1 = asyncio.create_task(long_running_task("A", 10))
    task2 = asyncio.create_task(long_running_task("B", 10))
    
    # 等待 3 秒后取消
    await asyncio.sleep(3)
    task1.cancel()
    
    # 等待另一个任务完成
    try:
        await task1
    except asyncio.CancelledError:
        pass
    
    try:
        result = await task2
        print(f"✅ {result}")
    except asyncio.CancelledError:
        pass


# ============================================================
# 练习 5: 信号量控制并发数
# ============================================================

async def limited_task(semaphore: asyncio.Semaphore, task_id: int):
    """受信号量限制的任务"""
    async with semaphore:
        print(f"🔧 任务 {task_id} 开始执行")
        await asyncio.sleep(2)
        print(f"✅ 任务 {task_id} 完成")
        return f"结果-{task_id}"


async def exercise5_semaphore():
    """练习 5：信号量控制并发数"""
    print("\n" + "=" * 50)
    print("练习 5：信号量控制并发数（最多 3 个并发）")
    print("=" * 50)
    
    semaphore = asyncio.Semaphore(3)
    
    # 创建 10 个任务，但同时只有 3 个执行
    tasks = [
        limited_task(semaphore, i)
        for i in range(10)
    ]
    
    results = await asyncio.gather(*tasks)
    print(f"\n所有结果：{results}")


# ============================================================
# 练习 6: 异步上下文管理器
# ============================================================

class AsyncResource:
    """异步资源管理"""
    
    def __init__(self, name: str):
        self.name = name
    
    async def __aenter__(self):
        print(f"🔓 获取资源：{self.name}")
        await asyncio.sleep(0.5)
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        print(f"🔒 释放资源：{self.name}")
        await asyncio.sleep(0.5)
    
    async def use(self):
        print(f"💼 使用资源：{self.name}")
        await asyncio.sleep(1)


async def exercise6_async_context_manager():
    """练习 6：异步上下文管理器"""
    print("\n" + "=" * 50)
    print("练习 6：异步上下文管理器")
    print("=" * 50)
    
    async with AsyncResource("数据库连接") as resource:
        await resource.use()
        await resource.use()


# ============================================================
# 练习 7: 批量处理任务（分批执行）
# ============================================================

async def batch_process(semaphore: asyncio.Semaphore, items: List[int], batch_size: int = 5):
    """批量处理任务"""
    
    async def process_item(item: int):
        async with semaphore:
            print(f"处理项目：{item}")
            await asyncio.sleep(0.5)
            return item * 2
    
    # 分批处理
    results = []
    for i in range(0, len(items), batch_size):
        batch = items[i:i + batch_size]
        print(f"\n📦 处理批次：{batch}")
        batch_results = await asyncio.gather(*[process_item(x) for x in batch])
        results.extend(batch_results)
    
    return results


async def exercise7_batch_processing():
    """练习 7：批量处理任务"""
    print("\n" + "=" * 50)
    print("练习 7：批量处理任务（每批 5 个，最多 3 个并发）")
    print("=" * 50)
    
    items = list(range(15))
    semaphore = asyncio.Semaphore(3)
    
    results = await batch_process(semaphore, items, batch_size=5)
    print(f"\n最终结果：{results}")


# ============================================================
# 练习 8: 异步事件监听
# ============================================================

async def event_listener(event: asyncio.Event, name: str):
    """事件监听器"""
    print(f"👂 {name} 等待事件...")
    await event.wait()
    print(f"✅ {name} 事件触发！")


async def exercise8_event_handling():
    """练习 8：异步事件处理"""
    print("\n" + "=" * 50)
    print("练习 8：异步事件处理")
    print("=" * 50)
    
    event = asyncio.Event()
    
    # 创建多个监听器
    listeners = [
        asyncio.create_task(event_listener(event, f"监听器-{i}"))
        for i in range(3)
    ]
    
    # 等待 2 秒后触发事件
    await asyncio.sleep(2)
    print("\n🎯 触发事件！")
    event.set()
    
    # 等待所有监听器完成
    await asyncio.gather(*listeners)


# ============================================================
# 主程序 - 选择运行练习
# ============================================================

async def run_all_exercises():
    """运行所有练习"""
    exercises = [
        ("并发下载", exercise1_download_urls),
        ("生产者 - 消费者", exercise2_producer_consumer),
        ("超时控制", exercise3_timeout_control),
        ("任务取消", exercise4_task_cancellation),
        ("信号量控制", exercise5_semaphore),
        ("异步上下文管理器", exercise6_async_context_manager),
        ("批量处理", exercise7_batch_processing),
        ("事件处理", exercise8_event_handling),
    ]
    
    for name, exercise_func in exercises:
        try:
            await exercise_func()
            await asyncio.sleep(1)  # 练习之间间隔
        except Exception as e:
            print(f"❌ 练习 {name} 出错：{e}")


if __name__ == "__main__":
    print("=" * 60)
    print("Day 4: 异步编程练习示例")
    print("=" * 60)
    print("\n可运行的练习：")
    print("1. 并发下载多个 URL")
    print("2. 生产者 - 消费者模型")
    print("3. 超时控制")
    print("4. 任务取消")
    print("5. 信号量控制并发数")
    print("6. 异步上下文管理器")
    print("7. 批量处理任务")
    print("8. 异步事件处理")
    print("\n运行所有练习请按 Ctrl+C 然后执行：python async_exercises.py")
    print("=" * 60)
    
    # 运行所有练习
    asyncio.run(run_all_exercises())
