# Day 4: 异步编程 (Async Programming)

## 学习目标
- [ ] 理解 `async/await` 语法
- [ ] 掌握 `asyncio` 基础
- [ ] 学会协程的使用
- [ ] 掌握并发执行多个任务

## 核心概念

### 协程定义
```python
async def my_coroutine():
    await some_async_operation()
```

### 并发执行
```python
import asyncio

async def main():
    results = await asyncio.gather(
        task1(),
        task2(),
        task3(),
    )
```

### 运行协程
```python
# Python 3.7+
asyncio.run(main())

# 或者
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
```

## 核心概念对比

| 同步 | 异步 |
|------|------|
| 顺序执行 | 并发执行 |
| 阻塞等待 | 非阻塞 |
| 一个任务一个任务完成 | 多任务交替执行 |

## 练习题

1. 编写异步下载函数
2. 使用 `asyncio.gather` 并发执行多个任务
3. 实现异步超时控制

## 学习资源
- Python 官方文档：https://docs.python.org/zh-cn/3/library/asyncio.html
- B 站：Python 高级编程（黑马程序员）

## 今日产出
- [ ] async_basic.py（待完成）
- [ ] 学习笔记