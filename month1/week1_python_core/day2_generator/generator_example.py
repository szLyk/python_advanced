"""
生成器执行示例
"""

def simple_generator():
    """简单生成器示例"""
    print("第一次执行")
    yield 1
    print("第二次执行")
    yield 2
    print("第三次执行")
    yield 3


if __name__ == "__main__":
    print("=" * 50)
    print("方式 1：使用 next() 逐个获取值")
    print("=" * 50)
    
    gen = simple_generator()
    print(f"生成器类型：{type(gen)}")
    print()
    
    try:
        print("调用 next(gen):")
        value1 = next(gen)
        print(f"返回值：{value1}\n")
        
        print("再次调用 next(gen):")
        value2 = next(gen)
        print(f"返回值：{value2}\n")
        
        print("再次调用 next(gen):")
        value3 = next(gen)
        print(f"返回值：{value3}\n")
        
        # 第四次调用会抛出异常
        print("第四次调用 next(gen):")
        next(gen)
    except StopIteration:
        print("生成器已耗尽，抛出 StopIteration 异常\n")
    
    print("=" * 50)
    print("方式 2：使用 for 循环（推荐）")
    print("=" * 50)
    
    for value in simple_generator():
        print(f"获取到：{value}")
    
    print()
    print("=" * 50)
    print("方式 3：转换为列表")
    print("=" * 50)
    
    result_list = list(simple_generator())
    print(f"转换为列表：{result_list}")
    
    print()
    print("=" * 50)
    print("方式 4：使用解包")
    print("=" * 50)
    
    a, b, c = simple_generator()
    print(f"a={a}, b={b}, c={c}")
