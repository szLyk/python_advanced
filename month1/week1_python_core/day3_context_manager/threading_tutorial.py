"""
Python 多线程完整教程
"""

import threading
import time
import os

# ============================================================
# 1. 基础线程创建
# ============================================================

def simple_task(name, delay=1):
    """简单的任务函数"""
    for i in range(3):
        print(f"[{name}] 第 {i+1} 次执行")
        time.sleep(delay)

# 创建线程
t1 = threading.Thread(target=simple_task, args=("线程 A", 0.5))
t2 = threading.Thread(target=simple_task, args=("线程 B", 0.8))

# 启动线程
t1.start()
t2.start()

# 等待线程完成
t1.join()
t2.join()

print("=" * 50)


# ============================================================
# 2. 使用类创建线程
# ============================================================

class MyThread(threading.Thread):
    """继承 Thread 类"""
    
    def __init__(self, name, count):
        super().__init__()
        self.name = name
        self.count = count
    
    def run(self):
        """线程执行的代码"""
        for i in range(self.count):
            print(f"[{self.name}] 执行第 {i+1} 次")
            time.sleep(0.3)

# 使用类创建线程
thread1 = MyThread("自定义线程 1", 3)
thread2 = MyThread("自定义线程 2", 3)

thread1.start()
thread2.start()
thread1.join()
thread2.join()

print("=" * 50)


# ============================================================
# 3. 共享数据问题（无锁）
# ============================================================

# 共享变量
shared_counter = 0

def increment_without_lock():
    """不使用锁 - 会有问题"""
    global shared_counter
    for _ in range(10000):
        temp = shared_counter
        temp += 1
        shared_counter = temp

# 创建多个线程
threads = []
for _ in range(5):
    t = threading.Thread(target=increment_without_lock)
    threads.append(t)
    t.start()

for t in threads:
    t.join()

print(f"无锁情况下的 counter: {shared_counter}")
print("（应该接近 50000，但实际会小于这个值 - 数据竞争）")

print("=" * 50)


# ============================================================
# 4. 使用 Lock 解决数据竞争
# ============================================================

shared_counter_with_lock = 0
lock = threading.Lock()

def increment_with_lock():
    """使用锁 - 安全"""
    global shared_counter_with_lock
    for _ in range(10000):
        with lock:  # 自动获取和释放锁
            temp = shared_counter_with_lock
            temp += 1
            shared_counter_with_lock = temp

# 创建多个线程
threads = []
for _ in range(5):
    t = threading.Thread(target=increment_with_lock)
    threads.append(t)
    t.start()

for t in threads:
    t.join()

print(f"有锁情况下的 counter: {shared_counter_with_lock}")
print("（正确等于 50000）")

print("=" * 50)


# ============================================================
# 5. 使用 RLock（可重入锁）
# ============================================================

rlock = threading.RLock()

def recursive_function(n):
    """递归函数需要 RLock"""
    with rlock:
        if n <= 0:
            return
        print(f"递归层数：{n}")
        recursive_function(n - 1)

# 使用 RLock 可以多次获取同一把锁
recursive_function(5)

print("=" * 50)


# ============================================================
# 6. 使用 Condition（条件变量）
# ============================================================

class ProducerConsumer:
    """生产者 - 消费者模型"""
    
    def __init__(self):
        self.buffer = []
        self.condition = threading.Condition()
        self.max_size = 5
    
    def produce(self, item):
        """生产者"""
        with self.condition:
            while len(self.buffer) >= self.max_size:
                print("缓冲区满，等待...")
                self.condition.wait()
            
            self.buffer.append(item)
            print(f"生产：{item}, 当前库存：{len(self.buffer)}")
            self.condition.notify_all()
    
    def consume(self):
        """消费者"""
        with self.condition:
            while len(self.buffer) == 0:
                print("缓冲区空，等待...")
                self.condition.wait()
            
            item = self.buffer.pop(0)
            print(f"消费：{item}, 当前库存：{len(self.buffer)}")
            self.condition.notify_all()
            return item

# 测试生产者消费者
pc = ProducerConsumer()

def producer_task():
    for i in range(10):
        pc.produce(i)
        time.sleep(0.1)

def consumer_task():
    for i in range(10):
        pc.consume()
        time.sleep(0.15)

p = threading.Thread(target=producer_task)
c = threading.Thread(target=consumer_task)
p.start()
c.start()
p.join()
c.join()

print("=" * 50)


# ============================================================
# 7. 使用 Event（事件）
# ============================================================

event = threading.Event()

def waiter():
    """等待事件"""
    print("等待事件触发...")
    event.wait()  # 阻塞等待
    print("事件已触发，继续执行！")

def trigger():
    """触发事件"""
    time.sleep(2)
    print("触发事件！")
    event.set()

w = threading.Thread(target=waiter)
t = threading.Thread(target=trigger)
w.start()
t.start()
w.join()
t.join()

print("=" * 50)


# ============================================================
# 8. 使用 Semaphore（信号量）
# ============================================================

class DatabasePool:
    """数据库连接池（限制并发数）"""
    
    def __init__(self, max_connections=3):
        self.semaphore = threading.Semaphore(max_connections)
        self.active_connections = 0
        self.lock = threading.Lock()
    
    def execute_query(self, query_id):
        with self.semaphore:
            with self.lock:
                self.active_connections += 1
                current = self.active_connections
            
            print(f"查询 {query_id} 开始 (活跃连接：{current})")
            time.sleep(0.5)
            
            with self.lock:
                self.active_connections -= 1
            
            print(f"查询 {query_id} 完成")

# 测试连接池
pool = DatabasePool(max_connections=3)
threads = []

for i in range(10):
    t = threading.Thread(target=pool.execute_query, args=(i,))
    threads.append(t)
    t.start()

for t in threads:
    t.join()

print("=" * 50)
print("所有线程完成！")
