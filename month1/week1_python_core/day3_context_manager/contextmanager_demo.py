"""
@contextmanager 装饰器详解
对比传统方式和装饰器方式
"""

from contextlib import contextmanager
import time

# ============================================================
# 方式 1：传统类方式
# ============================================================

class TimerClass:
    """传统方式实现的计时器"""
    
    def __init__(self, name="代码块"):
        self.name = name
    
    def __enter__(self):
        self.start = time.time()
        print(f"[TimerClass] 开始：{self.name}")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end = time.time()
        print(f"[TimerClass] 结束：耗时 {self.end - self.start:.2f}秒")
        return False


# ============================================================
# 方式 2：@contextmanager 装饰器方式
# ============================================================

@contextmanager
def timer_context(name="代码块"):
    """使用 @contextmanager 实现的计时器"""
    start = time.time()
    print(f"[timer_context] 开始：{name}")
    
    try:
        yield  # 不需要返回值，或者可以 yield 一些状态
        
        end = time.time()
        print(f"[timer_context] 结束：耗时 {end - start:.2f}秒")
    except Exception as e:
        print(f"[timer_context] 发生异常：{e}")
        raise
    finally:
        end = time.time()
        print(f"[timer_context] 清理：耗时 {end - start:.2f}秒")


# ============================================================
# 方式 3：@contextmanager 管理文件
# ============================================================

@contextmanager
def open_file(filename, mode):
    """文件管理器"""
    print(f"打开文件：{filename}")
    f = open(filename, mode, encoding='utf-8')
    try:
        yield f
    finally:
        print(f"关闭文件：{filename}")
        f.close()


# ============================================================
# 测试
# ============================================================

if __name__ == "__main__":
    print("=" * 50)
    print("测试 1：传统类方式")
    print("=" * 50)
    
    with TimerClass("传统方式") as timer:
        time.sleep(0.5)
        print("执行任务...")
    
    print("\n" + "=" * 50)
    print("测试 2：@contextmanager 方式")
    print("=" * 50)
    
    with timer_context("装饰器方式"):
        time.sleep(0.5)
        print("执行任务...")
    
    print("\n" + "=" * 50)
    print("测试 3：文件管理")
    print("=" * 50)
    
    # 使用 @contextmanager 管理文件
    with open_file("test_contextmanager.txt", "w") as f:
        f.write("Hello from @contextmanager!")
        print("写入文件...")
    
    # 验证文件
    with open_file("test_contextmanager.txt", "r") as f:
        content = f.read()
        print(f"文件内容：{content}")
    
    print("\n" + "=" * 50)
    print("测试 4：异常处理")
    print("=" * 50)
    
    try:
        with timer_context("异常测试"):
            time.sleep(0.3)
            print("执行任务...")
            1 / 0  # 抛出异常
    except ZeroDivisionError:
        print("捕获到除零异常")
    
    print("\n✅ 所有测试完成！")


