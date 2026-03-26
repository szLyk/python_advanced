"""
Day 4: 异步编程 (Async Programming)

学习目标：
1. 理解 async/await 语法
2. 掌握 asyncio 基础
3. 学会协程的使用
4. 掌握异步 I/O 操作

作者：AI Agent 工程师学习者
日期：待定
"""

import asyncio


# ============================================================
# 1. 协程基础
# ============================================================

async def hello():
    """简单的协程"""
    print("Hello")
    await asyncio.sleep(1)
    print("World")


# ============================================================
# 2. 并发执行多个协程
# ============================================================

async def task(name, delay):
    """模拟耗时任务"""
    print(f"任务 {name} 开始")
    await asyncio.sleep(delay)
    print(f"任务 {name} 完成")
    return f"结果-{name}"


async def main():
    # 并发执行多个任务
    results = await asyncio.gather(
        task("A", 1),
        task("B", 2),
        task("C", 1),
    )
    print(f"所有结果: {results}")


# ============================================================
# 3. 异步上下文管理器
# ============================================================

class AsyncTimer:
    """异步计时器"""

    async def __aenter__(self):
        import time
        self.start = time.time()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        import time
        self.end = time.time()
        print(f"执行时间: {self.end - self.start:.4f} 秒")


# ============================================================
# 主程序 - 运行示例
# ============================================================

if __name__ == "__main__":
    print("Day 4: 异步编程学习内容（待完成）")
    print("请参考学习计划完成练习")

    # 运行异步主函数
    # asyncio.run(main())