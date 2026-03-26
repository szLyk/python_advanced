"""
Day 3: 上下文管理器 (Context Manager)

学习目标：
1. 理解 with 语句
2. 掌握 __enter__ 和 __exit__ 方法
3. 学会使用 contextlib 模块
4. 掌握自定义上下文管理器

作者：AI Agent 工程师学习者
日期：待定
"""


# ============================================================
# 1. 上下文管理器基础
# ============================================================

class FileManager:
    """自定义文件管理器"""

    def __init__(self, filename, mode):
        self.filename = filename
        self.mode = mode
        self.file = None

    def __enter__(self):
        self.file = open(self.filename, self.mode)
        return self.file

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.file:
            self.file.close()
        return False  # 不抑制异常


# ============================================================
# 2. 使用 contextlib
# ============================================================

from contextlib import contextmanager

@contextmanager
def timer_context():
    """计时上下文管理器"""
    import time
    start = time.time()
    yield
    end = time.time()
    print(f"执行时间: {end - start:.4f} 秒")


# ============================================================
# 主程序 - 运行示例
# ============================================================

if __name__ == "__main__":
    print("Day 3: 上下文管理器学习内容（待完成）")
    print("请参考学习计划完成练习")