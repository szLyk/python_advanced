# Day 3: 上下文管理器 (Context Manager)

**状态：** ✅ 已完成

## 学习目标
- [x] 理解 with 语句的作用
- [x] 掌握 `__enter__` 和 `__exit__` 方法
- [x] 学会使用 `contextlib` 模块
- [x] 掌握自定义上下文管理器

---

## 目录

- [1. 上下文管理器基础](#1-上下文管理器基础)
- [2. 类实现方式](#2-类实现方式)
- [3. contextlib 装饰器方式](#3-contextlib-装饰器方式)
- [4. contextlib 常用工具](#4-contextlib-常用工具)
- [5. 异常处理](#5-异常处理)
- [6. 嵌套上下文管理器](#6-嵌套上下文管理器)
- [7. 异步上下文管理器](#7-异步上下文管理器)
- [8. 实战应用示例](#8-实战应用示例)

---

## 1. 上下文管理器基础

### 什么是上下文管理器？

上下文管理器是一种用于管理资源的对象，它可以：
- **进入时**：获取资源、设置环境
- **退出时**：释放资源、清理环境

### with 语句的工作流程

```python
with resource as r:
    # 使用资源
    pass
# 自动释放资源

# 等价于：
r = resource.__enter__()
try:
    # 使用资源
finally:
    resource.__exit__()
```

---

## 2. 类实现方式

### 基本模板

```python
class MyContextManager:
    def __enter__(self):
        # 进入上下文时的操作
        # 返回值会赋给 as 后面的变量
        return self  # 或返回其他对象

    def __exit__(self, exc_type, exc_val, exc_tb):
        # 退出上下文时的操作
        # exc_type: 异常类型（无异常时为 None）
        # exc_val: 异常值
        # exc_tb: 异常追踪信息
        return False  # True 表示抑制异常
```

### 示例 1：文件管理器

```python
class FileManager:
    """自动管理文件的打开和关闭"""

    def __init__(self, filename, mode):
        self.filename = filename
        self.mode = mode
        self.file = None

    def __enter__(self):
        self.file = open(self.filename, self.mode)
        print(f"打开文件: {self.filename}")
        return self.file

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.file:
            self.file.close()
            print(f"关闭文件: {self.filename}")
        return False  # 不抑制异常

# 使用
with FileManager("test.txt", "w") as f:
    f.write("Hello, World!")
# 文件自动关闭
```

### 示例 2：计时器

```python
import time

class Timer:
    """测量代码块执行时间"""

    def __enter__(self):
        self.start = time.perf_counter()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end = time.perf_counter()
        self.elapsed = self.end - self.start
        print(f"执行时间: {self.elapsed:.4f} 秒")
        return False

# 使用
with Timer() as t:
    # 执行一些耗时操作
    time.sleep(1)
print(f"总耗时: {t.elapsed:.4f} 秒")
```

### 示例 3：数据库连接管理器

```python
class DatabaseConnection:
    """管理数据库连接"""

    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None

    def __enter__(self):
        import pymysql  # 假设使用 MySQL
        self.connection = pymysql.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )
        print("数据库连接已建立")
        return self.connection

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.connection:
            if exc_type is None:
                self.connection.commit()  # 无异常时提交
                print("事务已提交")
            else:
                self.connection.rollback()  # 有异常时回滚
                print("事务已回滚")
            self.connection.close()
            print("数据库连接已关闭")
        return False

# 使用
with DatabaseConnection("localhost", "user", "pass", "db") as conn:
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users VALUES (1, 'Alice')")
```

### 示例 4：锁管理器

```python
import threading

class LockManager:
    """管理线程锁的获取和释放"""

    def __init__(self, lock):
        self.lock = lock

    def __enter__(self):
        self.lock.acquire()
        print("锁已获取")
        return self.lock

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.lock.release()
        print("锁已释放")
        return False

# 使用
my_lock = threading.Lock()
with LockManager(my_lock):
    # 临界区代码
    print("执行临界区操作")
```

---

## 3. contextlib 装饰器方式

### 使用 @contextmanager

```python
from contextlib import contextmanager

@contextmanager
def my_context():
    # 进入时的操作
    print("进入上下文")
    yield resource  # yield 的值赋给 as 变量
    # 退出时的操作
    print("退出上下文")
```

### 示例 5：计时器（装饰器版本）

```python
from contextlib import contextmanager
import time

@contextmanager
def timer(name="代码块"):
    """简洁的计时器"""
    start = time.perf_counter()
    yield  # 可以 yield 一个值，这里不需要
    end = time.perf_counter()
    print(f"{name} 执行时间: {end - start:.4f} 秒")

# 使用
with timer("数据处理"):
    data = [x**2 for x in range(1000000)]
```

### 示例 6：临时修改状态

```python
@contextmanager
def temporary_state(obj, attr, new_value):
    """临时修改对象属性"""
    old_value = getattr(obj, attr)
    setattr(obj, attr, new_value)
    yield old_value  # 返回旧值
    setattr(obj, attr, old_value)  # 恢复原值

# 使用
class Config:
    debug = False

config = Config()
print(f"原状态: debug={config.debug}")

with temporary_state(config, 'debug', True):
    print(f"临时状态: debug={config.debug}")
    # 在这里 debug=True

print(f"恢复后: debug={config.debug}")
```

### 示例 7：临时目录

```python
import os
import tempfile
from contextlib import contextmanager

@contextmanager
def temp_directory():
    """创建临时目录，使用后自动删除"""
    temp_dir = tempfile.mkdtemp()
    print(f"创建临时目录: {temp_dir}")
    yield temp_dir
    # 清理目录内容
    import shutil
    shutil.rmtree(temp_dir)
    print(f"删除临时目录: {temp_dir}")

# 使用
with temp_directory() as dirname:
    # 在临时目录中工作
    filepath = os.path.join(dirname, "temp.txt")
    with open(filepath, "w") as f:
        f.write("临时数据")
    print(f"临时文件路径: {filepath}")
```

---

## 4. contextlib 常用工具

### closing - 自动关闭对象

```python
from contextlib import closing

class MyResource:
    def close(self):
        print("资源已关闭")

# closing 会自动调用 close() 方法
with closing(MyResource()) as resource:
    print("使用资源")
```

### suppress - 抑制指定异常

```python
from contextlib import suppress

# 抑制 FileNotFoundError
with suppress(FileNotFoundError):
    os.remove("不存在的文件.txt")
    print("这行不会执行")  # 因为异常被抑制

# 抑制多个异常
with suppress(FileNotFoundError, PermissionError):
    os.remove("some_file.txt")
```

### redirect_stdout - 重定向输出

```python
from contextlib import redirect_stdout
import io

# 将标准输出重定向到字符串
output = io.StringIO()
with redirect_stdout(output):
    print("这行输出被捕获")
    print("不会显示在屏幕上")

captured = output.getvalue()
print(f"捕获的内容: {captured}")
```

### redirect_stderr - 重定向错误输出

```python
from contextlib import redirect_stderr
import sys
import io

error_output = io.StringIO()
with redirect_stderr(error_output):
    sys.stderr.write("错误信息被捕获\n")

print(f"捕获的错误: {error_output.getvalue()}")
```

### nullcontext - 空上下文管理器

```python
from contextlib import nullcontext

# 当不需要实际管理时使用
def process_data(data, use_lock=True):
    lock = threading.Lock() if use_lock else nullcontext()
    with lock:
        return data * 2

# 不需要锁时
result = process_data([1, 2, 3], use_lock=False)
```

---

## 5. 异常处理

### __exit__ 方法的异常处理

```python
class SafeOperation:
    """演示异常处理"""

    def __enter__(self):
        print("进入操作")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            print("操作成功完成")
        else:
            print(f"捕获异常: {exc_type.__name__}: {exc_val}")
            # return True 会抑制异常
            # return False 会继续传播异常
            return True  # 抑制异常

# 测试无异常情况
with SafeOperation():
    print("正常操作")

# 测试有异常情况（异常被抑制）
with SafeOperation():
    raise ValueError("测试异常")
print("程序继续执行")  # 因为异常被抑制
```

### contextmanager 装饰器的异常处理

```python
from contextlib import contextmanager

@contextmanager
def safe_context():
    print("进入上下文")
    try:
        yield
    except Exception as e:
        print(f"捕获异常: {e}")
        raise  # 可以选择重新抛出或抑制
    finally:
        print("清理资源")

# 使用
with safe_context():
    raise ValueError("测试异常")
```

---

## 6. 嵌套上下文管理器

### 多层嵌套

```python
# 方式 1：逐层嵌套
with Timer("外层"):
    with Timer("内层"):
        time.sleep(0.5)

# 方式 2：同一行（Python 3.10+ 更推荐）
with Timer("外层"), Timer("内层"):
    time.sleep(0.5)
```

### ExitStack - 动态管理多个上下文

```python
from contextlib import ExitStack

# 动态数量的上下文管理器
files = ["a.txt", "b.txt", "c.txt"]

with ExitStack() as stack:
    handles = [stack.enter_context(open(f, 'w')) for f in files]
    # 所有文件会在退出时自动关闭
    for handle in handles:
        handle.write("some content\n")

# 等价于：
with open("a.txt", 'w') as f1, \
     open("b.txt", 'w') as f2, \
     open("c.txt", 'w') as f3:
    f1.write("content")
    f2.write("content")
    f3.write("content")
```

---

## 7. 异步上下文管理器

### 使用 __aenter__ 和 __aexit__

```python
import asyncio

class AsyncTimer:
    """异步计时器"""

    async def __aenter__(self):
        self.start = asyncio.get_event_loop().time()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        self.end = asyncio.get_event_loop().time()
        print(f"异步执行时间: {self.end - self.start:.4f} 秒")
        return False

# 使用
async def main():
    async with AsyncTimer():
        await asyncio.sleep(1)

asyncio.run(main())
```

### 使用 asynccontextmanager

```python
from contextlib import asynccontextmanager
import asyncio

@asynccontextmanager
async def async_db_connection():
    """模拟异步数据库连接"""
    print("建立异步连接...")
    await asyncio.sleep(0.1)
    yield "connection"
    print("关闭异步连接...")
    await asyncio.sleep(0.1)

async def main():
    async with async_db_connection() as conn:
        print(f"使用连接: {conn}")

asyncio.run(main())
```

---

## 8. 实战应用示例

### 示例 8：性能分析器

```python
import time
import sys
from contextlib import contextmanager

@contextmanager
def profiler(name, threshold=0.1):
    """性能分析器，超过阈值时警告"""
    start = time.perf_counter()
    yield
    elapsed = time.perf_counter() - start

    if elapsed > threshold:
        print(f"⚠️ {name} 执行过慢: {elapsed:.4f}s > {threshold}s")
    else:
        print(f"✓ {name} 执行正常: {elapsed:.4f}s")

# 使用
with profiler("数据处理", threshold=0.5):
    data = [x**2 for x in range(100000)]
```

### 示例 9：日志记录器

```python
import logging
from contextlib import contextmanager

@contextmanager
def log_operation(operation_name):
    """记录操作开始和结束"""
    logging.info(f"开始操作: {operation_name}")
    try:
        yield
        logging.info(f"操作成功: {operation_name}")
    except Exception as e:
        logging.error(f"操作失败: {operation_name} - {e}")
        raise

# 使用
with log_operation("数据导入"):
    # 执行操作
    pass
```

### 示例 10：临时环境变量

```python
import os
from contextlib import contextmanager

@contextmanager
def temp_env_var(key, value):
    """临时设置环境变量"""
    old_value = os.environ.get(key)
    os.environ[key] = value
    yield value
    if old_value is None:
        os.environ.pop(key, None)
    else:
        os.environ[key] = old_value

# 使用
with temp_env_var("DEBUG", "true"):
    print(f"DEBUG = {os.environ['DEBUG']}")
print(f"退出后 DEBUG = {os.environ.get('DEBUG', '未设置')}")
```

### 示例 11：批量文件处理

```python
from contextlib import ExitStack, contextmanager

@contextmanager
def batch_file_writer(filenames):
    """批量打开多个文件"""
    with ExitStack() as stack:
        files = [stack.enter_context(open(f, 'w')) for f in filenames]
        yield dict(zip(filenames, files))

# 使用
with batch_file_writer(["log1.txt", "log2.txt", "log3.txt"]) as files:
    for filename, handle in files.items():
        handle.write(f"这是 {filename} 的内容\n")
```

### 示例 12：模拟事务

```python
from contextlib import contextmanager

class Transaction:
    """模拟数据库事务"""

    def __init__(self):
        self.operations = []
        self.committed = False

    def add(self, operation):
        self.operations.append(operation)

    def commit(self):
        self.committed = True
        print("事务提交成功")

    def rollback(self):
        print("事务回滚")

@contextmanager
def transaction():
    """事务上下文管理器"""
    tx = Transaction()
    try:
        yield tx
        if not tx.committed:
            tx.commit()
    except Exception as e:
        tx.rollback()
        raise

# 使用
with transaction() as tx:
    tx.add("INSERT INTO users VALUES (1)")
    tx.add("INSERT INTO users VALUES (2)")
    # 自动提交
```

---

## 练习题

1. 编写一个计时器上下文管理器（类和装饰器两种方式）
2. 编写一个数据库连接管理器，支持事务回滚
3. 使用 `contextlib` 实现临时目录管理器
4. 实现一个性能分析器，超过阈值时打印警告
5. 实现一个临时修改对象属性的上下文管理器

---

## 最佳实践

### ✅ 推荐做法

1. **使用 contextlib**：对于简单场景，`@contextmanager` 更简洁
2. **异常处理**：在 `__exit__` 中正确处理异常
3. **资源清理**：确保在 `finally` 或 `__exit__` 中清理资源
4. **嵌套管理**：使用 `ExitStack` 管理动态数量的上下文

### ❌ 避免的做法

1. 在 `__enter__` 中抛出异常（可能导致资源泄漏）
2. 忽略 `__exit__` 的返回值含义
3. 在上下文管理器中执行耗时操作

---

## 学习资源
- Python 官方文档：https://docs.python.org/zh-cn/3/library/contextlib.html
- B 站：Python 高级编程（黑马程序员）

## 今日产出
- [x] context_manager.py（已完成）
- [x] 学习笔记