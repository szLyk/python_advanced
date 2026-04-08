# Day 44: Milvus 安装

> **日期**: 2026-05-16（周五）  
> **周次**: Week 7 - 向量数据库  
> **预计耗时**: 2 小时

---

## 今日学习目标

- [ ] 了解 Milvus 架构
- [ ] 完成 Docker 部署
- [ ] 验证安装成功
- [ ] 熟悉配置文件

---

## 学习内容

### 1. Milvus 简介

**Milvus** 是一款开源的向量数据库，专门用于处理大规模向量相似度搜索。

**核心特点**：
- 🚀 高性能：十亿级向量毫秒级搜索
- 🔧 易扩展：支持水平扩展
- 📦 易部署：Docker 一键启动
- 🌐 社区活跃：LF AI & Data 基金会项目

### 2. Milvus 架构

```
┌─────────────────────────────────────────────────────────┐
│                   Milvus 架构                           │
├─────────────────────────────────────────────────────────┤
│  接入层 (Access Layer)                                  │
│  - SDK (Python/Java/Go/Node.js)                         │
│  - REST API                                             │
│                          ↓                              │
│  协调服务 (Coordinator Services)                         │
│  - Root Coordinator: 集群管理                            │
│  - Query Coordinator: 查询协调                           │
│  - Data Coordinator: 数据管理                            │
│                          ↓                              │
│  执行层 (Worker Nodes)                                  │
│  - Proxy Node: 请求代理                                  │
│  - Query Node: 查询执行                                  │
│  - Data Node: 数据处理                                   │
│                          ↓                              │
│  存储层 (Storage)                                       │
│  - etcd: 元数据存储                                       │
│  - MinIO: 对象存储                                       │
│  - Pulsar: 消息队列                                      │
└─────────────────────────────────────────────────────────┘
```

### 3. Docker 部署 Milvus

#### 前置要求

```bash
# 检查 Docker 安装
docker --version
docker-compose --version

# 确保 Docker 运行中
docker ps

# 分配至少 4GB 内存给 Docker（Mac/Windows）
```

#### 安装步骤

**步骤 1: 创建目录**
```bash
# 进入项目目录
cd month2/week7_vector_db/

# 创建 Milvus 目录
mkdir -p milvus_docker
cd milvus_docker
```

**步骤 2: 下载配置文件**
```bash
# 下载 docker-compose.yml
curl https://raw.githubusercontent.com/milvus-io/milvus/master/deployments/docker/standalone/docker-compose.yml -o docker-compose.yml

# 或使用提供的文件
# （已复制到 day44_milvus_install/docker-compose.yml）
```

**步骤 3: 启动 Milvus**
```bash
# 启动所有服务
docker-compose up -d

# 查看启动日志
docker-compose logs -f

# 等待约 2 分钟，所有服务启动完成
```

**步骤 4: 验证安装**
```bash
# 检查容器状态
docker-compose ps

# 应该看到所有服务都是 healthy 状态
```

### 4. 测试连接

```python
# test_connection.py

from pymilvus import connections, utility

# 连接 Milvus
connections.connect(
    alias="default",
    host="localhost",
    port="19530"
)

# 测试连接
print(f"Milvus 版本：{utility.get_version()}")

# 检查服务器状态
print(f"服务器状态：{utility.get_server_status()}")

print("✅ Milvus 连接成功！")
```

### 5. 配置文件说明

**docker-compose.yml 关键配置**：
```yaml
version: '3.5'

services:
  etcd:
    image: quay.io/coreos/etcd:v3.5.5
    # etcd 用于存储元数据

  minio:
    image: minio/minio:RELEASE.2023-03-20T20-16-10Z
    # MinIO 用于对象存储

  milvus-standalone:
    image: milvusdb/milvus:v2.3.0
    ports:
      - "19530:19530"  # gRPC 端口
      - "9091:9091"    # HTTP 端口
    depends_on:
      - etcd
      - minio
```

---

## 实践任务

### 任务 1: Docker 环境检查 ✅

```bash
# 检查 Docker 安装
docker --version
docker-compose --version

# 测试 Docker 运行
docker run hello-world
```

### 任务 2: 安装 Milvus ✅

```bash
# 1. 创建目录
mkdir -p milvus_docker && cd milvus_docker

# 2. 下载配置
curl https://raw.githubusercontent.com/milvus-io/milvus/master/deployments/docker/standalone/docker-compose.yml -o docker-compose.yml

# 3. 启动
docker-compose up -d

# 4. 查看状态
docker-compose ps

# 5. 查看日志（可选）
docker-compose logs -f milvus-standalone
```

### 任务 3: 测试连接 ✅

```python
# test_connection.py

from pymilvus import connections, utility

try:
    connections.connect(host="localhost", port="19530")
    print("✅ 连接成功！")
    print(f"版本：{utility.get_version()}")
except Exception as e:
    print(f"❌ 连接失败：{e}")
    print("请检查 Milvus 是否正常运行")
```

### 任务 4: 记录安装过程 ✅

创建 `milvus_installed.txt` 记录：
- [ ] Docker 版本
- [ ] Milvus 版本
- [ ] 启动时间
- [ ] 遇到的问题
- [ ] 截图/日志

---

## 常见问题

### Q1: Docker 启动失败？

```bash
# 检查 Docker 是否运行
docker ps

# 检查端口是否被占用
netstat -an | grep 19530
netstat -an | grep 9091

# 重启 Docker
# Windows: 右键 Docker 图标 → Restart
# Mac: Docker → Troubleshoot → Restart
```

### Q2: 内存不足？

```bash
# Milvus  standalone 需要约 2GB 内存
# 检查可用内存
free -h  # Linux
# 或任务管理器（Windows）

# 关闭不必要的容器
docker stop $(docker ps -q)
```

### Q3: 下载镜像太慢？

```bash
# 使用国内镜像加速
# 编辑 /etc/docker/daemon.json (Linux)
# 或 Docker Desktop 设置中添加：
# https://registry.docker-cn.com
```

### Q4: Windows 权限问题？

```bash
# 以管理员身份运行 PowerShell
# 或使用 WSL2
```

---

## 代码文件

```
day44_milvus_install/
├── README.md                    # 本文件
├── docker-compose.yml           # Docker 配置
├── test_connection.py           # 连接测试
├── milvus_installed.txt         # 安装记录
└── install_guide.md             # 详细安装指南
```

---

## 参考资源

- [Milvus 官方安装文档](https://milvus.io/docs/install_standalone-docker.md)
- [Milvus GitHub](https://github.com/milvus-io/milvus)
- [Docker 官方文档](https://docs.docker.com/)

---

## 下一步

- **Day 45**: Milvus 基本操作（Collection、CRUD）
- **明日任务**: 学习向量数据库的基本使用

---

**💡 今日格言**: "好的开始是成功的一半，Milvus 已就绪！"
