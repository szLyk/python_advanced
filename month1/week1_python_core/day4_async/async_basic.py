"""
Day 4: 异步编程 (Async Programming)

学习目标：
1. ✅ 理解 async/await 语法
2. ✅ 掌握 asyncio 基础
3. ✅ 学会协程的使用
4. ✅ 掌握异步 I/O 操作

作者：AI Agent 工程师学习者
日期：2026-03-26
"""

import asyncio
import time


# ============================================================
# 1. 协程基础
# ============================================================

async def hello():
    """简单的协程示例"""
    print("Hello")
    await asyncio.sleep(1)  # 非阻塞等待
    print("World")


async def demo_coroutine():
    """演示协程基础"""
    print("\n" + "=" * 50)
    print("1. 协程基础")
    print("=" * 50)
    
    # 调用协程
    await hello()
    
    print("协程执行完成")


# ============================================================
# 2. 并发执行多个协程
# ============================================================

async def task(name, delay):
    """模拟耗时任务"""
    print(f"任务 {name} 开始")
    await asyncio.sleep(delay)
    print(f"任务 {name} 完成")
    return f"结果-{name}"


async def demo_gather():
    """演示并发执行"""
    print("\n" + "=" * 50)
    print("2. 并发执行多个任务")
    print("=" * 50)
    
    start = time.time()
    
    # 并发执行多个任务
    results = await asyncio.gather(
        task("A", 1),
        task("B", 2),
        task("C", 1),
    )
    
    elapsed = time.time() - start
    print(f"所有结果: {results}")
    print(f"总耗时: {elapsed:.2f} 秒（并发执行，不是 4 秒）")


# ============================================================
# 3. 创建后台任务
# ============================================================

async def background_task(name, duration):
    """后台任务"""
    for i in range(duration):
        print(f"  [后台-{name}] 执行中... {i+1}/{duration}")
        await asyncio.sleep(0.5)
    return f"后台-{name}-完成"


async def demo_create_task():
    """演示创建后台任务"""
    print("\n" + "=" * 50)
    print("3. 创建后台任务")
    print("=" * 50)
    
    # 创建后台任务（立即开始执行）
    task1 = asyncio.create_task(background_task("A", 4))
    task2 = asyncio.create_task(background_task("B", 3))
    
    print("主线程可以继续做其他事情...")
    await asyncio.sleep(1)
    print("主线程处理其他任务完成")
    
    # 等待后台任务完成
    results = await asyncio.gather(task1, task2)
    print(f"后台任务结果: {results}")


# ============================================================
# 4. 超时控制
# ============================================================

async def slow_operation(duration):
    """模拟慢速操作"""
    print(f"开始执行 {duration} 秒操作...")
    await asyncio.sleep(duration)
    return f"操作完成（耗时 {duration} 秒）"


async def demo_timeout():
    """演示超时控制"""
    print("\n" + "=" * 50)
    print("4. 超时控制")
    print("=" * 50)
    
    # 场景 1：正常完成
    try:
        result = await asyncio.wait_for(slow_operation(2), timeout=5)
        print(f"✅ {result}")
    except asyncio.TimeoutError:
        print("❌ 操作超时")
    
    # 场景 2：超时
    print("\n测试超时情况:")
    try:
        result = await asyncio.wait_for(slow_operation(5), timeout=2)
        print(f"✅ {result}")
    except asyncio.TimeoutError:
        print("❌ 操作超时（预期）")


# ============================================================
# 5. 异步上下文管理器
# ============================================================

class AsyncTimer:
    """异步计时器"""

    async def __aenter__(self):
        self.start = time.time()
        print("⏱️ 计时开始")
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        self.end = time.time()
        print(f"⏱️ 计时结束: {self.end - self.start:.4f} 秒")


async def demo_async_context():
    """演示异步上下文管理器"""
    print("\n" + "=" * 50)
    print("5. 异步上下文管理器")
    print("=" * 50)
    
    async with AsyncTimer():
        print("执行耗时操作...")
        await asyncio.sleep(1)
        print("操作完成")


# ============================================================
# 6. 信号量控制并发
# ============================================================

async def limited_task(semaphore, task_id):
    """受信号量限制的任务"""
    async with semaphore:
        print(f"🔧 任务 {task_id} 开始执行")
        await asyncio.sleep(1)
        print(f"✅ 任务 {task_id} 完成")
        return f"结果-{task_id}"


async def demo_semaphore():
    """演示信号量控制并发"""
    print("\n" + "=" * 50)
    print("6. 信号量控制并发（最多 3 个同时执行）")
    print("=" * 50)
    
    semaphore = asyncio.Semaphore(3)
    
    # 创建 10 个任务，但同时只有 3 个执行
    tasks = [limited_task(semaphore, i) for i in range(10)]
    results = await asyncio.gather(*tasks)
    print(f"\n所有结果: {results}")


# ============================================================
# 主程序 - 运行所有示例
# ============================================================

async def main():
    """主函数 - 运行所有示例"""
    print("=" * 60)
    print("Day 4: 异步编程基础示例")
    print("=" * 60)
    
    await demo_coroutine()
    await demo_gather()
    await demo_create_task()
    await demo_timeout()
    await demo_async_context()
    await demo_semaphore()
    
    print("\n" + "=" * 60)
    print("✅ 所有示例运行完成！")
    print("=" * 60)


if __name__ == "__main__":
    # 运行异步主函数
    asyncio.run(main())