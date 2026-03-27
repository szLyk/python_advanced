"""
Day 3: 上下文管理器 (Context Manager)

学习目标：
1. 理解 with 语句
2. 掌握 __enter__ 和 __exit__ 方法
3. 学会使用 contextlib 模块
4. 掌握自定义上下文管理器

作者：AI Agent 工程师学习者
日期：2026-03-28
"""

import time
import threading
import os
import tempfile
import shutil
import io
import sys
import asyncio
from contextlib import (
    contextmanager,
    closing,
    suppress,
    redirect_stdout,
    redirect_stderr,
    nullcontext,
    ExitStack,
    asynccontextmanager
)


# ============================================================
# 1. 类实现方式 - 文件管理器
# ============================================================

class FileManager:
    """自动管理文件的打开和关闭"""

    def __init__(self, filename, mode):
        self.filename = filename
        self.mode = mode
        self.file = None

    def __enter__(self):
        self.file = open(self.filename, self.mode)
        print(f"[FileManager] 打开文件: {self.filename}")
        return self.file

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.file:
            self.file.close()
            print(f"[FileManager] 关闭文件: {self.filename}")
        return False  # 不抑制异常


# ============================================================
# 2. 类实现方式 - 计时器
# ============================================================

class Timer:
    """测量代码块执行时间"""

    def __init__(self, name="代码块"):
        self.name = name
        self.start = 0
        self.end = 0
        self.elapsed = 0

    def __enter__(self):
        self.start = time.perf_counter()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end = time.perf_counter()
        self.elapsed = self.end - self.start
        print(f"[Timer] {self.name} 执行时间: {self.elapsed:.4f} 秒")
        return False


# ============================================================
# 3. 类实现方式 - 锁管理器
# ============================================================

class LockManager:
    """管理线程锁的获取和释放"""

    def __init__(self, lock, name="锁"):
        self.lock = lock
        self.name = name

    def __enter__(self):
        self.lock.acquire()
        print(f"[LockManager] {self.name} 已获取")
        return self.lock

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.lock.release()
        print(f"[LockManager] {self.name} 已释放")
        return False


# ============================================================
# 4. 类实现方式 - 异常处理演示
# ============================================================

class SafeOperation:
    """演示异常处理"""

    def __enter__(self):
        print("[SafeOperation] 进入操作")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            print("[SafeOperation] 操作成功完成")
        else:
            print(f"[SafeOperation] 捕获异常: {exc_type.__name__}: {exc_val}")
            return True  # 抑制异常，程序继续执行


# ============================================================
# 5. contextlib 装饰器 - 计时器
# ============================================================

@contextmanager
def timer_context(name="代码块"):
    """简洁的计时器"""
    start = time.perf_counter()
    yield
    end = time.perf_counter()
    print(f"[timer_context] {name} 执行时间: {end - start:.4f} 秒")


# ============================================================
# 6. contextlib 装饰器 - 临时修改状态
# ============================================================

@contextmanager
def temporary_state(obj, attr, new_value):
    """临时修改对象属性"""
    old_value = getattr(obj, attr)
    setattr(obj, attr, new_value)
    print(f"[temporary_state] {attr}: {old_value} -> {new_value}")
    yield old_value
    setattr(obj, attr, old_value)
    print(f"[temporary_state] {attr}: {new_value} -> {old_value} (恢复)")


# ============================================================
# 7. contextlib 装饰器 - 临时目录
# ============================================================

@contextmanager
def temp_directory():
    """创建临时目录，使用后自动删除"""
    temp_dir = tempfile.mkdtemp()
    print(f"[temp_directory] 创建临时目录: {temp_dir}")
    yield temp_dir
    shutil.rmtree(temp_dir)
    print(f"[temp_directory] 删除临时目录: {temp_dir}")


# ============================================================
# 8. contextlib 装饰器 - 性能分析器
# ============================================================

@contextmanager
def profiler(name, threshold=0.1):
    """性能分析器，超过阈值时警告"""
    start = time.perf_counter()
    yield
    elapsed = time.perf_counter() - start

    if elapsed > threshold:
        print(f"[profiler] WARNING: {name} 执行过慢: {elapsed:.4f}s > {threshold}s")
    else:
        print(f"[profiler] OK: {name} 执行正常: {elapsed:.4f}s")


# ============================================================
# 9. contextlib 装饰器 - 临时环境变量
# ============================================================

@contextmanager
def temp_env_var(key, value):
    """临时设置环境变量"""
    old_value = os.environ.get(key)
    os.environ[key] = value
    print(f"[temp_env_var] 设置 {key}={value}")
    yield value
    if old_value is None:
        os.environ.pop(key, None)
        print(f"[temp_env_var] 移除 {key}")
    else:
        os.environ[key] = old_value
        print(f"[temp_env_var] 恢复 {key}={old_value}")


# ============================================================
# 10. contextlib 常用工具示例
# ============================================================

class CloseableResource:
    """演示 closing 工具"""
    def close(self):
        print("[CloseableResource] 资源已关闭")


# ============================================================
# 11. 嵌套上下文管理器 - ExitStack
# ============================================================

@contextmanager
def batch_file_writer(filenames):
    """批量打开多个文件"""
    with ExitStack() as stack:
        files = [stack.enter_context(open(f, 'w')) for f in filenames]
        print(f"[batch_file_writer] 打开了 {len(files)} 个文件")
        yield dict(zip(filenames, files))
    print(f"[batch_file_writer] 所有文件已关闭")


# ============================================================
# 12. 异步上下文管理器
# ============================================================

class AsyncTimer:
    """异步计时器"""

    async def __aenter__(self):
        self.start = asyncio.get_event_loop().time()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        self.end = asyncio.get_event_loop().time()
        self.elapsed = self.end - self.start
        print(f"[AsyncTimer] 异步执行时间: {self.elapsed:.4f} 秒")
        return False


@asynccontextmanager
async def async_db_connection():
    """模拟异步数据库连接"""
    print("[async_db_connection] 建立异步连接...")
    await asyncio.sleep(0.1)
    yield "connection_object"
    print("[async_db_connection] 关闭异步连接...")
    await asyncio.sleep(0.1)


# ============================================================
# 主程序 - 运行所有示例
# ============================================================

def demo_file_manager():
    """演示文件管理器"""
    print("\n" + "=" * 50)
    print("1. 文件管理器示例")
    print("=" * 50)

    # 创建测试文件
    test_file = "test_filemanager.txt"

    with FileManager(test_file, "w") as f:
        f.write("Hello, Context Manager!")

    # 验证文件已关闭
    with open(test_file, "r") as f:
        print(f"文件内容: {f.read()}")

    # 清理
    os.remove(test_file)


def demo_timer():
    """演示计时器"""
    print("\n" + "=" * 50)
    print("2. 计时器示例（类实现）")
    print("=" * 50)

    with Timer("数据计算") as t:
        data = [x**2 for x in range(100000)]
    print(f"可访问耗时: {t.elapsed:.4f} 秒")


def demo_timer_context():
    """演示计时器装饰器"""
    print("\n" + "=" * 50)
    print("3. 计时器示例（装饰器实现）")
    print("=" * 50)

    with timer_context("列表生成"):
        data = [x**2 for x in range(100000)]


def demo_lock_manager():
    """演示锁管理器"""
    print("\n" + "=" * 50)
    print("4. 锁管理器示例")
    print("=" * 50)

    my_lock = threading.Lock()
    with LockManager(my_lock, "线程锁"):
        print("执行临界区操作")


def demo_safe_operation():
    """演示异常处理"""
    print("\n" + "=" * 50)
    print("5. 异常处理示例")
    print("=" * 50)

    # 无异常情况
    print("\n--- 无异常 ---")
    with SafeOperation():
        print("正常操作")

    # 有异常情况（异常被抑制）
    print("\n--- 有异常（被抑制）---")
    with SafeOperation():
        raise ValueError("测试异常")
    print("程序继续执行（异常被抑制）")


def demo_temporary_state():
    """演示临时修改状态"""
    print("\n" + "=" * 50)
    print("6. 临时修改状态示例")
    print("=" * 50)

    class Config:
        debug = False
        timeout = 30

    config = Config()
    print(f"原状态: debug={config.debug}")

    with temporary_state(config, 'debug', True):
        print(f"临时状态: debug={config.debug}")

    print(f"恢复后: debug={config.debug}")


def demo_temp_directory():
    """演示临时目录"""
    print("\n" + "=" * 50)
    print("7. 临时目录示例")
    print("=" * 50)

    with temp_directory() as dirname:
        filepath = os.path.join(dirname, "temp.txt")
        with open(filepath, "w") as f:
            f.write("临时数据")
        print(f"临时文件路径: {filepath}")


def demo_profiler():
    """演示性能分析器"""
    print("\n" + "=" * 50)
    print("8. 性能分析器示例")
    print("=" * 50)

    # 正常情况
    with profiler("快速操作", threshold=0.5):
        data = [x**2 for x in range(1000)]

    # 超过阈值
    with profiler("慢速操作", threshold=0.5):
        time.sleep(0.6)


def demo_contextlib_tools():
    """演示 contextlib 常用工具"""
    print("\n" + "=" * 50)
    print("9. contextlib 常用工具示例")
    print("=" * 50)

    # closing
    print("\n--- closing ---")
    with closing(CloseableResource()) as resource:
        print("使用资源")

    # suppress
    print("\n--- suppress ---")
    with suppress(FileNotFoundError):
        os.remove("不存在的文件.txt")
        print("这行不会执行")

    # redirect_stdout
    print("\n--- redirect_stdout ---")
    output = io.StringIO()
    with redirect_stdout(output):
        print("这行输出被捕获")
    print(f"捕获的内容: {output.getvalue().strip()}")


def demo_exit_stack():
    """演示 ExitStack"""
    print("\n" + "=" * 50)
    print("10. ExitStack 批量文件管理示例")
    print("=" * 50)

    files = ["temp_a.txt", "temp_b.txt", "temp_c.txt"]

    with batch_file_writer(files) as handles:
        for filename, handle in handles.items():
            handle.write(f"这是 {filename} 的内容\n")

    # 清理
    for f in files:
        if os.path.exists(f):
            os.remove(f)


async def demo_async_context():
    """演示异步上下文管理器"""
    print("\n" + "=" * 50)
    print("11. 异步上下文管理器示例")
    print("=" * 50)

    async with AsyncTimer():
        await asyncio.sleep(0.5)

    print("\n--- async_db_connection ---")
    async with async_db_connection() as conn:
        print(f"使用连接: {conn}")


async def async_main():
    """异步主函数"""
    await demo_async_context()


if __name__ == "__main__":
    print("=" * 60)
    print("Day 3: 上下文管理器完整示例")
    print("=" * 60)

    demo_file_manager()
    demo_timer()
    demo_timer_context()
    demo_lock_manager()
    demo_safe_operation()
    demo_temporary_state()
    demo_temp_directory()
    demo_profiler()
    demo_contextlib_tools()
    demo_exit_stack()

    # 运行异步示例
    asyncio.run(async_main())

    print("\n" + "=" * 60)
    print("所有示例运行完成！")
    print("=" * 60)