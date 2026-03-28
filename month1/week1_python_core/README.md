# Week 1: Python 核心语法

**状态：** 🔄 进行中（4/6 完成）

## 本周目标
- [x] 掌握装饰器原理和应用
- [x] 理解生成器和迭代器
- [x] 掌握上下文管理器
- [x] 学会异步编程基础
- [ ] 完成异步爬虫项目

## 学习计划

| 天数 | 主题 | 文件 | 状态 |
|------|------|------|------|
| Day 1 | 装饰器 | [day1_decorator/](./day1_decorator/) | ✅ 已完成 |
| Day 2 | 生成器 | [day2_generator/](./day2_generator/) | ✅ 已完成 |
| Day 3 | 上下文管理器 | [day3_context_manager/](./day3_context_manager/) | ✅ 已完成 |
| Day 4 | 异步编程 | [day4_async/](./day4_async/) | ✅ 已完成 |
| Day 5 | 弹性/休息 | - | - |
| Day 6 | 综合项目 | [day6_project/](./day6_project/) | ⬜ 待完成 |
| Day 7 | 休息 | - | - |

## 学习产出

### Day 1: 装饰器 ✅
- `decorator_practice.py` - 装饰器完整教程
- 学习内容：
  - 装饰器基础和本质
  - `@wraps` 保留函数元信息
  - 带参数的装饰器
  - 类装饰器
  - 实用装饰器示例（timer, retry, log_calls）

### Day 2: 生成器 ✅
- `generator_practice.py` - 生成器练习
- `README.md` - 详细生成器文档
- 学习内容：
  - `yield` 关键字
  - 生成器表达式
  - 生成器 vs 迭代器
  - 流式处理大数据
  - `yield from` 委托生成器

### Day 3: 上下文管理器 ✅
- `context_manager.py` - 上下文管理器完整教程
- `threading_tutorial.py` - 多线程教程
- `contextmanager_demo.py` - @contextmanager 示例
- 学习内容：
  - `__enter__` 和 `__exit__` 协议
  - `@contextmanager` 装饰器
  - `yield` 在上下文管理器中的作用
  - 异常处理
  - 多线程和锁

### Day 4: 异步编程 ✅
- `async_basic.py` - 异步编程基础示例
- `async_exercises.py` - 8 个实用练习
- `README.md` - 详细 async/await 文档
- 学习内容：
  - `async/await` 语法
  - `asyncio` 常用 API
  - 并发执行 (`gather`, `create_task`)
  - 超时控制 (`wait_for`)
  - 信号量 (`Semaphore`)
  - 生产者 - 消费者模式

### Day 6: 综合项目 ⬜
- 异步爬虫项目（待完成）

## 核心知识点

### 装饰器
```python
@decorator
def func():
    pass
```
- 装饰器本质：闭包 + 语法糖
- `@wraps` 保留函数元信息
- 应用场景：日志、计时、缓存、权限验证

### 生成器
```python
def gen():
    yield value
```
- `yield` 暂停函数执行，保存状态
- 惰性求值，节省内存
- 适合流式处理大数据

### 上下文管理器
```python
with resource:
    # 使用资源
# 自动释放
```
- `__enter__` 和 `__exit__` 协议
- `@contextmanager` 简化实现
- `yield` 分隔准备和清理阶段

### 异步编程
```python
async def func():
    await operation
```
- `async/await` 语法
- `asyncio` 并发执行
- 适合 I/O 密集型任务

## 学习进度

```
总进度: ████████████░░░░░░░░ 66% (4/6)

Day 1: ████████████████████ 100% ✅
Day 2: ████████████████████ 100% ✅
Day 3: ████████████████████ 100% ✅
Day 4: ████████████████████ 100% ✅
Day 5: ░░░░░░░░░░░░░░░░░░░░   0% - (休息)
Day 6: ░░░░░░░░░░░░░░░░░░░░   0% ⬜
```

## 学习资源
- B 站：Python 高级编程（黑马程序员）
- Python 官方文档：https://docs.python.org/zh-cn/3/
- asyncio 文档：https://docs.python.org/zh-cn/3/library/asyncio.html

---
**最后更新：** 2026-03-26