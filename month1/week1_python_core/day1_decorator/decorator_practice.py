"""
Day 1: 装饰器 (Decorator)

学习目标：
1. 理解装饰器的本质（闭包 + 语法糖）
2. 掌握装饰器的基本用法
3. 学会带参数的装饰器
4. 了解 functools.wraps 的作用
5. 掌握类装饰器

作者：AI Agent 工程师学习者
日期：2026-03-25
"""

from functools import wraps
import time


# ============================================================
# 1. 装饰器基础 - 什么是装饰器
# ============================================================

def my_decorator(func):
    """最简单的装饰器"""

    def wrapper():
        print("函数执行前...")
        func()
        print("函数执行后...")

    return wrapper


@my_decorator
def say_hello():
    print("Hello, World!")


# ============================================================
# 2. 装饰器处理带参数的函数
# ============================================================

def log_calls(func):
    """记录函数调用的装饰器"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"调用函数: {func.__name__}")
        print(f"参数: args={args}, kwargs={kwargs}")
        result = func(*args, **kwargs)
        print(f"返回值: {result}")
        return result

    return wrapper


@log_calls
def add(a, b):
    """加法函数"""
    return a + b


@log_calls
def greet(name, greeting="Hello"):
    """问候函数"""
    return f"{greeting}, {name}!"


# ============================================================
# 3. 带参数的装饰器
# ============================================================

def repeat(times):
    """重复执行函数的装饰器"""

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            results = []
            for i in range(times):
                print(f"第 {i + 1} 次执行")
                result = func(*args, **kwargs)
                results.append(result)
            return results

        return wrapper

    return decorator


@repeat(times=3)
def say_hi(name):
    return f"Hi, {name}!"


# ============================================================
# 4. 实用装饰器示例
# ============================================================

def timer(func=None, *, unit="s"):
    """计时器装饰器"""
    factor = {"s": 1, "ms": 1000, "us": 1000000}

    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            start = time.perf_counter()
            result = f(*args, **kwargs)
            end = time.perf_counter()
            elapsed = (end - start) * factor[unit]
            print(f"[{f.__name__}] 执行时间: {elapsed:.4f} {unit}")
            return result

        return wrapper

    if func is not None:
        return decorator(func)
    return decorator


@timer
def slow_function():
    """模拟耗时操作"""
    time.sleep(0.1)
    return "完成"


def retry(max_attempts=3, delay=1, exceptions=(Exception,)):
    """重试装饰器"""

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            current_delay = delay
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    if attempt == max_attempts:
                        raise
                    print(f"[{func.__name__}] 第 {attempt} 次失败: {e}")
                    time.sleep(current_delay)
                    current_delay *= 2

        return wrapper

    return decorator


# ============================================================
# 5. 类装饰器
# ============================================================

class CountCalls:
    """统计调用次数的类装饰器"""

    def __init__(self, func):
        self.func = func
        self.count = 0

    def __call__(self, *args, **kwargs):
        self.count += 1
        print(f"第 {self.count} 次调用 {self.func.__name__}")
        return self.func(*args, **kwargs)


@CountCalls
def my_function():
    print("执行函数")


def decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Hi, {kwargs.get('name')}!")
        return func(*args, **kwargs)
    return wrapper


@decorator
def say_bye(name):
    print(f"Bye, {name}!")


if __name__ == '__main__':
    say_bye(name='luo')
#
# # ============================================================
# # 主程序 - 运行示例
# # ============================================================
#
# if __name__ == "__main__":
#     print("=" * 50)
#     print("1. 基础装饰器")
#     print("=" * 50)
#     say_hello()
#
#     print("\n" + "=" * 50)
#     print("2. 处理带参数的函数")
#     print("=" * 50)
#     add(3, 5)
#     print()
#     greet("Alice", greeting="Hi")
#
#     print("\n" + "=" * 50)
#     print("3. 带参数的装饰器")
#     print("=" * 50)
#     results = say_hi("Bob")
#     print(f"所有结果: {results}")
#
#     print("\n" + "=" * 50)
#     print("4. 计时器装饰器")
#     print("=" * 50)
#     slow_function()
#
#     print("\n" + "=" * 50)
#     print("5. 类装饰器 - 统计调用次数")
#     print("=" * 50)
#     my_function()
#     my_function()
#     my_function()
#
#     print("\n" + "=" * 50)
#     print("学习要点总结：")
#     print("=" * 50)
#     print("""
# 1. 装饰器本质：接受一个函数，返回一个新函数
# 2. @语法糖：@decorator 等价于 func = decorator(func)
# 3. *args, **kwargs：让装饰器适用于任何函数
# 4. @wraps：保留原函数的元信息（__name__, __doc__等）
# 5. 带参数的装饰器：需要三层嵌套
# 6. 类装饰器：通过 __call__ 方法实现
#     """)
