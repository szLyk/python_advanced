"""
yield from 示例 - chain 函数
"""


def chain(*iterables):
    """连接多个可迭代对象"""
    print(f"开始处理 {len(iterables)} 个可迭代对象")
    for iterable in iterables:
        print(f"  处理：{iterable}")
        yield from iterable


def chain_manual(*iterables):
    """手动实现版本（不使用 yield from）"""
    for iterable in iterables:
        for item in iterable:
            yield item


if __name__ == "__main__":
    print("=" * 50)
    print("示例 1：连接列表和字符串")
    print("=" * 50)

    result = chain([1, 2, 3], 'abc', [4, 5])
    print(f"结果类型：{type(result)}")
    print(f"连接结果：{list(result)}")

    print("\n" + "=" * 50)
    print("示例 2：对比手动实现版本")
    print("=" * 50)

    result1 = list(chain([1, 2], [3, 4]))
    result2 = list(chain_manual([1, 2], [3, 4]))

    print(f"yield from 版本：{result1}")
    print(f"手动实现版本：{result2}")
    print(f"结果相同：{result1 == result2}")

    print("\n" + "=" * 50)
    print("示例 3：混合不同类型的可迭代对象")
    print("=" * 50)

    mixed = chain(
        [1, 2, 3],  # 列表
        'xyz',  # 字符串
        range(4, 6),  # range
        {'a', 'b'},  # 集合
        {'key': 'value'}  # 字典（迭代键）
    )

    print(f"混合结果：{list(mixed)}")

    print("\n" + "=" * 50)
    print("示例 4：空的可迭代对象")
    print("=" * 50)

    with_empty = chain([1, 2], [], [3, 4])
    print(f"包含空列表：{list(with_empty)}")

    print("\n" + "=" * 50)
    print("示例 5：使用 itertools.chain 对比")
    print("=" * 50)

    from itertools import chain as itertools_chain

    our_chain = list(chain([1, 2], 'abc'))
    std_chain = list(itertools_chain([1, 2], 'abc'))

    print(f"我们的实现：{our_chain}")
    print(f"标准库实现：{std_chain}")
    print(f"结果相同：{our_chain == std_chain}")
