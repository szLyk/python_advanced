"""
对比 with open() 和自定义 with open_file()
"""

from contextlib import contextmanager

# ============================================================
# 自定义 open_file（模拟 open 的行为）
# ============================================================

@contextmanager
def open_file(filename, mode):
    """自定义文件管理器"""
    print(f"[open_file] 准备打开：{filename}")
    f = open(filename, mode, encoding='utf-8')
    print(f"[open_file] 文件已打开")
    try:
        yield f
    finally:
        print(f"[open_file] 准备关闭文件")
        f.close()
        print(f"[open_file] 文件已关闭")


# ============================================================
# 测试
# ============================================================

if __name__ == "__main__":
    test_file = "test_compare.txt"
    
    print("=" * 50)
    print("测试 1：使用 with open()")
    print("=" * 50)
    
    with open(test_file, "w", encoding='utf-8') as f:
        print("  with 块内部")
        f.write("Hello from open()\n")
        print("  写入完成")
    
    print("  with 块结束，文件已自动关闭\n")
    
    print("=" * 50)
    print("测试 2：使用 with open_file()")
    print("=" * 50)
    
    with open_file(test_file, "a") as f:
        print("  with 块内部")
        f.write("Hello from open_file()\n")
        print("  写入完成")
    
    print("  with 块结束，文件已自动关闭\n")
    
    print("=" * 50)
    print("验证文件内容")
    print("=" * 50)
    
    # 直接读取文件
    with open(test_file, "r", encoding='utf-8') as f:
        content = f.read()
        print(f"文件内容：\n{content}")
    
    print("=" * 50)
    print("测试 3：异常情况下自动关闭")
    print("=" * 50)
    
    try:
        with open_file(test_file, "r") as f:
            print("  读取文件...")
            content = f.read()
            print("  执行会出错的操作")
            1 / 0  # 抛出异常
    except ZeroDivisionError:
        print("  捕获到异常，但文件已经被自动关闭了！\n")
    
    print("=" * 50)
    print("测试 4：不使用 with 的对比")
    print("=" * 50)
    
    print("不使用 with 的写法：")
    f = open(test_file, "r", encoding='utf-8')
    print("  文件已打开")
    content = f.read()
    print("  读取完成")
    # 如果忘记 f.close()，文件会一直占用！
    f.close()  # 必须手动关闭
    print("  手动关闭文件\n")
    
    print("✅ 所有测试完成！")
