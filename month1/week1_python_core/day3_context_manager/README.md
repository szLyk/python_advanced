# Day 3: 上下文管理器 (Context Manager)

## 学习目标
- [ ] 理解 with 语句的作用
- [ ] 掌握 `__enter__` 和 `__exit__` 方法
- [ ] 学会使用 `contextlib` 模块
- [ ] 掌握自定义上下文管理器

## 核心概念

### with 语句
```python
with resource as r:
    # 使用资源
    pass
# 自动释放资源
```

### 类实现方式
```python
class MyContext:
    def __enter__(self):
        # 获取资源
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # 释放资源
        return False  # 是否抑制异常
```

### contextlib 方式
```python
from contextlib import contextmanager

@contextmanager
def my_context():
    # 进入时执行
    yield resource
    # 退出时执行
```

## 常见应用场景
- 文件操作
- 数据库连接
- 锁的获取和释放
- 计时器

## 练习题

1. 编写一个计时器上下文管理器
2. 编写一个数据库连接管理器
3. 使用 `contextlib` 实现临时目录

## 学习资源
- Python 官方文档：https://docs.python.org/zh-cn/3/library/contextlib.html
- B 站：Python 高级编程（黑马程序员）

## 今日产出
- [ ] context_manager.py（待完成）
- [ ] 学习笔记