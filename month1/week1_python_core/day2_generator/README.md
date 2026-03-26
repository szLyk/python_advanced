# Day 2: 生成器 (Generator)

**学习目标：**
1. 理解 yield 关键字
2. 掌握生成器表达式
3. 理解生成器 vs 迭代器
4. 掌握生成器的实际应用

**作者：** AI Agent 工程师学习者  
**日期：** 2026-03-26

---

## 目录

- [1. 生成器基础](#1-生成器基础)
- [2. yield 关键字](#2-yield-关键字)
- [3. 生成器表达式](#3-生成器表达式)
- [4. 生成器 vs 迭代器](#4-生成器-vs-迭代器)
- [5. 实际应用](#5-实际应用)
- [6. 高级用法](#6-高级用法)

---

## 1. 生成器基础

### 什么是生成器？

生成器是一种**特殊的迭代器**，它可以让你逐个产生值，而不是一次性创建所有值。

**核心特点：**
- **惰性求值**：只在需要时才计算下一个值
- **节省内存**：不需要一次性存储所有数据
- **自动迭代**：自动实现 `__iter__()` 和 `__next__()` 方法

### 创建生成器的两种方式

```python
# 方式 1：生成器函数（使用 yield）
def my_generator():
    yield 1
    yield 2
    yield 3

# 方式 2：生成器表达式
gen = (x for x in range(1, 4))
```

---

## 2. yield 关键字

### yield vs return

| 特性 | return | yield |
|------|--------|-------|
| **返回值** | 返回一个值，函数结束 | 返回一个值，函数暂停 |
| **状态保存** | 不保存 | 保存局部变量和执行位置 |
| **再次调用** | 从头开始 | 从暂停处继续 |

### 示例：理解 yield 的执行流程

```python
def countdown(n):
    """倒数计数器"""
    print(f"开始倒数：{n}")
    while n > 0:
        yield n
        n -= 1
    print("倒数结束！")

# 使用生成器
gen = countdown(3)
print(type(gen))  # <class 'generator'>

# 逐个获取值
print(next(gen))  # 输出：开始倒数：3 \n 3
print(next(gen))  # 输出：2
print(next(gen))  # 输出：1
print(next(gen))  # 输出：倒数结束！\n StopIteration 异常
```

### yield 的工作原理

```python
def simple_yield():
    print("第一次执行")
    yield 1
    print("第二次执行")
    yield 2
    print("第三次执行")
    yield 3

gen = simple_yield()

# 每次调用 next() 时：
# 1. 执行到下一个 yield
# 2. 返回 yield 后的值
# 3. 暂停并保存状态
```

---

## 3. 生成器表达式

### 语法

```python
# 生成器表达式
gen = (x * 2 for x in range(10))

# 列表推导式（对比）
lst = [x * 2 for x in range(10)]
```

### 内存效率对比

```python
import sys

# 列表推导式 - 立即创建所有元素
list_comp = [x for x in range(1000000)]
print(f"列表内存：{sys.getsizeof(list_comp)} bytes")  # 约 8MB

# 生成器表达式 - 按需生成
gen_comp = (x for x in range(1000000))
print(f"生成器内存：{sys.getsizeof(gen_comp)} bytes")  # 约 120 bytes
```

### 示例

```python
# 平方数生成器
squares = (x**2 for x in range(1, 6))

for num in squares:
    print(num)  # 1, 4, 9, 16, 25

# 带条件的生成器
even_squares = (x**2 for x in range(10) if x % 2 == 0)
# 等价于：0, 4, 16, 36, 64
```

---

## 4. 生成器 vs 迭代器

### 概念关系

```
迭代器 (Iterator)
├── 实现 __iter__() 和 __next__()
└── 生成器 (Generator) - 自动实现这两个方法
```

### 手动实现迭代器 vs 生成器

```python
# 方式 1：手动实现迭代器类
class CountDown:
    def __init__(self, start):
        self.start = start
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.start <= 0:
            raise StopIteration
        self.start -= 1
        return self.start + 1

# 方式 2：使用生成器（更简洁）
def count_down(n):
    while n > 0:
        yield n
        n -= 1
```

### 对比总结

| 特性 | 迭代器类 | 生成器函数 |
|------|---------|-----------|
| **代码量** | 多 | 少 |
| **状态管理** | 手动 | 自动 |
| **可读性** | 较低 | 较高 |
| **灵活性** | 高 | 中等 |

---

## 5. 实际应用

### 5.1 文件逐行读取

```python
def read_lines(filename):
    """逐行读取文件，节省内存"""
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            yield line.strip()

# 使用
for line in read_lines('large_file.txt'):
    print(line)
```

### 5.2 无限序列

```python
def fibonacci():
    """生成斐波那契数列（无限）"""
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

# 获取前 10 个斐波那契数
fib = fibonacci()
for _ in range(10):
    print(next(fib), end=' ')  # 0, 1, 1, 2, 3, 5, 8, 13, 21, 34
```

### 5.3 数据管道

```python
def read_data(filename):
    """读取数据"""
    with open(filename, 'r') as f:
        for line in f:
            yield line.strip()

def filter_data(data):
    """过滤数据"""
    for item in data:
        if item and not item.startswith('#'):
            yield item

def parse_data(data):
    """解析数据"""
    for item in data:
        yield int(item)

# 组合使用
data = read_data('data.txt')
filtered = filter_data(data)
parsed = parse_data(filtered)

for value in parsed:
    print(value)
```

### 5.4 分块处理大数据

```python
def chunk_processor(data, chunk_size=1000):
    """分块处理大数据"""
    chunk = []
    for item in data:
        chunk.append(item)
        if len(chunk) == chunk_size:
            yield chunk
            chunk = []
    if chunk:
        yield chunk

# 使用
large_dataset = range(10000)
for chunk in chunk_processor(large_dataset, 1000):
    print(f"处理块：{len(chunk)} 条数据")
    # 处理每一块数据
```

---

## 6. 高级用法

### 6.1 send() - 向生成器发送值

```python
def accumulator():
    """累加器"""
    total = 0
    while True:
        value = yield total
        if value is not None:
            total += value

acc = accumulator()
print(next(acc))      # 0 (初始化)
print(acc.send(5))    # 5 (发送 5，total=5)
print(acc.send(3))    # 8 (发送 3，total=8)
print(acc.send(10))   # 18 (发送 10，total=18)
```

### 6.2 throw() - 向生成器抛出异常

```python
def robust_generator():
    try:
        yield 1
        yield 2
        yield 3
    except ValueError:
        print("捕获到 ValueError")

gen = robust_generator()
print(next(gen))  # 1
print(next(gen))  # 2
gen.throw(ValueError("测试异常"))  # 输出：捕获到 ValueError
```

### 6.3 委托生成器（yield from）

```python
def sub_generator():
    yield 'a'
    yield 'b'
    yield 'c'

def main_generator():
    yield from sub_generator()
    yield 'd'
    yield 'e'

# 使用
for item in main_generator():
    print(item)  # a, b, c, d, e
```

### 6.4 生成器链式调用

```python
def chain_generators(*generators):
    """链式组合多个生成器"""
    for gen in generators:
        yield from gen

gen1 = (x for x in range(3))
gen2 = (x for x in range(3, 6))
gen3 = (x for x in range(6, 9))

for value in chain_generators(gen1, gen2, gen3):
    print(value, end=' ')  # 0 1 2 3 4 5 6 7 8
```

---

## 实战练习

### 练习 1：实现 range 生成器

```python
def my_range(start, stop=None, step=1):
    """自定义 range 生成器"""
    if stop is None:
        stop = start
        start = 0
    
    current = start
    while (step > 0 and current < stop) or (step < 0 and current > stop):
        yield current
        current += step

# 测试
print(list(my_range(5)))        # [0, 1, 2, 3, 4]
print(list(my_range(1, 5)))     # [1, 2, 3, 4]
print(list(my_range(1, 10, 2))) # [1, 3, 5, 7, 9]
```

### 练习 2：滑动窗口

```python
def sliding_window(data, window_size):
    """滑动窗口生成器"""
    if len(data) < window_size:
        return
    
    for i in range(len(data) - window_size + 1):
        yield data[i:i + window_size]

# 使用
data = [1, 2, 3, 4, 5, 6]
for window in sliding_window(data, 3):
    print(window)  # [1,2,3], [2,3,4], [3,4,5], [4,5,6]
```

### 练习 3：扁平化嵌套列表

```python
def flatten(nested_list):
    """扁平化嵌套列表"""
    for item in nested_list:
        if isinstance(item, list):
            yield from flatten(item)
        else:
            yield item

# 使用
nested = [1, [2, 3, [4, 5]], 6, [7, [8, 9]]]
print(list(flatten(nested)))  # [1, 2, 3, 4, 5, 6, 7, 8, 9]
```

---

## 性能对比

### 生成器 vs 列表

```python
import time
import sys

# 生成大量数据
def generate_list(n):
    return [x * 2 for x in range(n)]

def generate_generator(n):
    return (x * 2 for x in range(n))

n = 1000000

# 内存对比
list_mem = sys.getsizeof(generate_list(n))
gen_mem = sys.getsizeof(generate_generator(n))

print(f"列表内存：{list_mem} bytes")
print(f"生成器内存：{gen_mem} bytes")
print(f"节省：{(1 - gen_mem/list_mem) * 100:.2f}%")

# 时间对比（只取前 10 个）
start = time.time()
gen = generate_generator(n)
for _ in range(10):
    next(gen)
print(f"生成器时间：{time.time() - start:.6f}s")

start = time.time()
lst = generate_list(n)
for i in range(10):
    _ = lst[i]
print(f"列表时间：{time.time() - start:.6f}s")
```

---

## 最佳实践

### ✅ 何时使用生成器

1. **处理大数据集**：文件、数据库查询结果
2. **无限序列**：斐波那契、随机数
3. **数据管道**：流式处理
4. **节省内存**：只需要逐个访问元素

### ❌ 何时不使用生成器

1. **需要多次遍历**：生成器只能遍历一次
2. **需要索引访问**：生成器不支持 `gen[5]`
3. **需要长度信息**：`len(gen)` 会报错
4. **数据量小**：直接用列表更简单

---

## 常见陷阱

### 陷阱 1：生成器只能用一次

```python
gen = (x for x in range(3))
print(list(gen))  # [0, 1, 2]
print(list(gen))  # [] (已耗尽)
```

### 陷阱 2：延迟求值的陷阱

```python
# 错误示例
generators = [lambda: i for i in range(3)]
print([g() for g in generators])  # [2, 2, 2] (闭包陷阱)

# 正确做法
generators = [(lambda i=i: i) for i in range(3)]
print([g() for g in generators])  # [0, 1, 2]
```

### 陷阱 3：忘记初始化

```python
def counter():
    count = 0
    while True:
        yield count
        count += 1

c = counter()
print(next(c))  # 0
# 如果重新创建 counter()，会从 0 开始
```

---

## 总结

### 核心要点

1. **yield**：暂停函数执行并返回值，保存状态
2. **生成器表达式**：`(x for x in iterable)`，节省内存
3. **惰性求值**：只在需要时计算
4. **一次性**：生成器只能遍历一次

### 关键优势

- ✅ 内存效率高
- ✅ 代码简洁
- ✅ 适合流式处理
- ✅ 自动状态管理

### 下一步

- 练习使用生成器处理实际数据
- 理解 `send()`、`throw()`、`close()` 方法
- 探索 `yield from` 在复杂场景的应用

---

## 参考资源

- [Python 官方文档 - 生成器](https://docs.python.org/zh-cn/3/howto/functional.html#generators)
- [PEP 255 - Simple Generators](https://www.python.org/dev/peps/pep-0255/)
- [PEP 342 - Coroutines via Enhanced Generators](https://www.python.org/dev/peps/pep-0342/)
