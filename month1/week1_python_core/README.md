# Week 1: Python 核心语法

## 本周目标
- [ ] 掌握装饰器原理和应用
- [ ] 理解生成器和迭代器
- [ ] 掌握上下文管理器
- [ ] 学会异步编程基础
- [ ] 完成异步爬虫项目

## 学习计划

| 天数 | 主题 | 文件 | 状态 |
|------|------|------|------|
| Day 1 | 装饰器 | day1_decorator/decorator_practice.py | ✅ |
| Day 2 | 生成器 | day2_generator/generator_practice.py | ✅ |
| Day 3 | 上下文管理器 | day3_context_manager/context_manager.py | ⬜ |
| Day 4 | 异步编程 | day4_async/async_basic.py | ⬜ |
| Day 5 | 弹性/休息 | - | - |
| Day 6 | 综合项目 | day6_project/async_crawler.py | ⬜ |
| Day 7 | 休息 | - | - |

## 核心知识点

### 装饰器
```python
@decorator
def func():
    pass
```
- 装饰器本质：闭包 + 语法糖
- `@wraps` 保留函数元信息

### 生成器
```python
def gen():
    yield value
```
- `yield` 暂停函数执行
- 惰性求值，节省内存

### 上下文管理器
```python
with resource:
    # 使用资源
# 自动释放
```
- `__enter__` 和 `__exit__` 协议

### 异步编程
```python
async def func():
    await operation
```
- `async/await` 语法
- `asyncio` 并发执行

## 学习资源
- B 站：Python 高级编程（黑马程序员）
- Python 官方文档：https://docs.python.org/zh-cn/3/