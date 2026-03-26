# Day 1: 装饰器 (Decorator)

## 学习目标
- [ ] 理解装饰器的本质（闭包 + 语法糖）
- [ ] 掌握装饰器的基本用法
- [ ] 学会带参数的装饰器
- [ ] 了解 functools.wraps 的作用
- [ ] 掌握类装饰器

## 核心概念

### 装饰器本质
```python
@decorator
def func():
    pass

# 等价于
func = decorator(func)
```

### 装饰器模板
```python
from functools import wraps

def my_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # 前置操作
        result = func(*args, **kwargs)
        # 后置操作
        return result
    return wrapper
```

### 带参数的装饰器
```python
def repeat(times):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for _ in range(times):
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator

@repeat(times=3)
def say_hello():
    print("Hello!")
```

## 练习题

1. 编写一个 `@timer` 装饰器，测量函数执行时间
2. 编写一个 `@log` 装饰器，记录函数的调用信息
3. 编写一个 `@cache` 装饰器，缓存函数结果
4. 编写一个 `@retry` 装饰器，失败时自动重试

## 学习资源
- Python 官方文档：https://docs.python.org/zh-cn/3/glossary.html#term-decorator
- B 站：Python 高级编程（黑马程序员）

## 今日产出
- [ ] decorator_practice.py（已完成）
- [ ] 学习笔记