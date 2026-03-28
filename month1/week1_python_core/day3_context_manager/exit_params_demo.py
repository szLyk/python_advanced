"""
演示 __exit__ 方法的参数来源
"""

class SafeOperation:
    """演示异常处理"""

    def __enter__(self):
        print("[SafeOperation] 进入操作")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print(f"\n[__exit__] 参数详情:")
        print(f"  exc_type (异常类型): {exc_type}")
        print(f"  exc_val (异常值): {exc_val}")
        print(f"  exc_tb (traceback): {exc_tb}")
        
        if exc_type is None:
            print("[__exit__] 操作成功完成，无异常")
        else:
            print(f"[__exit__] 捕获异常：{exc_type.__name__}: {exc_val}")
            return True  # 抑制异常，程序继续执行


if __name__ == "__main__":
    print("=" * 50)
    print("场景 1：没有异常")
    print("=" * 50)
    
    with SafeOperation() as op:
        print("执行正常操作")
    
    print("\n" + "=" * 50)
    print("场景 2：发生除零异常")
    print("=" * 50)
    
    with SafeOperation() as op:
        print("执行会抛出异常的操作")
        result = 10 / 0  # ZeroDivisionError
    
    print("\n程序继续执行（异常被抑制）")
    
    print("\n" + "=" * 50)
    print("场景 3：发生值错误异常")
    print("=" * 50)
    
    with SafeOperation() as op:
        print("执行另一个异常操作")
        int("abc")  # ValueError
    
    print("\n程序继续执行（异常被抑制）")
