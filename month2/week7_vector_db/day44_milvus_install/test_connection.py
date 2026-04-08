"""
Day 44: Milvus 安装

学习目标:
- 了解 Milvus 架构
- 完成 Docker 部署
- 验证安装成功
- 熟悉配置文件
"""

import subprocess
import sys


def check_docker():
    """检查 Docker 安装"""
    print("=" * 50)
    print("检查 Docker 安装")
    print("=" * 50)

    try:
        # 检查 Docker
        result = subprocess.run(
            ["docker", "--version"],
            capture_output=True,
            text=True,
            timeout=10
        )
        print(f"\n✅ Docker: {result.stdout.strip()}")
    except (subprocess.TimeoutExpired, FileNotFoundError):
        print("\n❌ Docker 未安装或超时")
        print("请安装 Docker Desktop: https://www.docker.com/products/docker-desktop/")
        return False

    try:
        # 检查 Docker Compose
        result = subprocess.run(
            ["docker", "compose", "version"],
            capture_output=True,
            text=True,
            timeout=10
        )
        print(f"✅ Docker Compose: {result.stdout.strip()}")
    except (subprocess.TimeoutExpired, FileNotFoundError):
        print("\n⚠️  Docker Compose 未安装（使用 docker-compose 命令）")

    return True


def check_milvus_connection():
    """检查 Milvus 连接"""
    print("\n" + "=" * 50)
    print("检查 Milvus 连接")
    print("=" * 50)

    try:
        from pymilvus import connections, utility

        # 尝试连接
        connections.connect(
            host="localhost",
            port="19530",
            timeout=5
        )

        # 获取版本
        version = utility.get_version()
        print(f"\n✅ Milvus 连接成功！")
        print(f"   版本：{version}")

        # 检查服务器状态
        try:
            status = utility.get_server_status()
            print(f"   状态：{status}")
        except:
            print(f"   状态：运行中")

        return True

    except ImportError:
        print("\n❌ pymilvus 未安装")
        print("请运行：pip install pymilvus")
        return False

    except Exception as e:
        print(f"\n❌ Milvus 连接失败：{e}")
        print("\n请确保 Milvus 已启动:")
        print("  cd milvus_docker")
        print("  docker-compose up -d")
        return False


def show_install_guide():
    """显示安装指南"""
    print("\n" + "=" * 50)
    print("Milvus 安装指南")
    print("=" * 50)

    print("""
【步骤 1: 创建目录】
mkdir -p milvus_docker
cd milvus_docker

【步骤 2: 下载配置】
# Windows PowerShell:
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/milvus-io/milvus/master/deployments/docker/standalone/docker-compose.yml" -OutFile "docker-compose.yml"

# 或使用提供的 docker-compose.yml 文件

【步骤 3: 启动 Milvus】
docker-compose up -d

【步骤 4: 查看状态】
docker-compose ps
# 等待所有服务变为 healthy

【步骤 5: 验证安装】
python day44_milvus_install/test_connection.py

【系统要求】
- Docker Desktop 已安装
- 至少 4GB 可用内存
- 至少 10GB 可用磁盘空间
""")


def show_troubleshooting():
    """显示故障排除指南"""
    print("\n" + "=" * 50)
    print("故障排除")
    print("=" * 50)

    print("""
【问题 1: Docker 启动失败】
解决：
1. 确保 Docker Desktop 正在运行
2. 检查资源分配（至少 4GB 内存）

【问题 2: 端口被占用】
解决:
netstat -ano | findstr 19530
# 关闭占用端口的进程

【问题 3: 下载镜像太慢】
解决：配置 Docker 镜像加速器
https://registry.docker-cn.com

【问题 4: 连接超时】
解决:
1. 等待 2-3 分钟让 Milvus 完全启动
2. docker-compose logs -f 查看日志
""")


def main():
    """主函数"""
    print("=" * 60)
    print("Day 44: Milvus 安装检查")
    print("=" * 60)

    # 检查 Docker
    docker_ok = check_docker()

    if docker_ok:
        # 检查 Milvus 连接
        milvus_ok = check_milvus_connection()

        if milvus_ok:
            print("\n🎉 Milvus 安装成功！可以开始学习了！")
        else:
            show_install_guide()
    else:
        show_install_guide()

    # 显示故障排除
    show_troubleshooting()

    print("\n" + "=" * 60)
    print("✅ Day 44 检查完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()
