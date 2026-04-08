"""
敏感信息检查脚本

在提交 Git 之前运行此脚本，检查是否有敏感信息泄露
"""

import os
import re
import sys

# 需要检查的文件类型
CHECKED_EXTENSIONS = [".py", ".md", ".txt", ".json", ".yml", ".yaml", ".env"]

# 敏感信息模式
SENSITIVE_PATTERNS = [
    # API Key 模式
    (r"sk-[a-zA-Z0-9]{20,}", "可能的 API Key"),
    (r"api[_-]?key\s*[=:]\s*[\"'][a-zA-Z0-9]{20,}[\"']", "硬编码的 API Key"),

    # 密码模式
    (r"password\s*[=:]\s*[\"'][^\"']{8,}[\"']", "硬编码的密码"),
    (r"passwd\s*[=:]\s*[\"'][^\"']{8,}[\"']", "硬编码的密码"),

    # 私钥模式
    (r"-----BEGIN (RSA |DSA |EC )?PRIVATE KEY-----", "私钥"),

    # 数据库连接字符串
    (r"mongodb(\+srv)?://[^\"']+", "MongoDB 连接字符串"),
    (r"postgres(?:ql)?://[^\"']+", "PostgreSQL 连接字符串"),
    (r"mysql://[^\"']+", "MySQL 连接字符串"),

    # 令牌/密钥模式
    (r"ghp_[a-zA-Z0-9]{36}", "GitHub Personal Access Token"),
    (r"xox[baprs]-[0-9]{10,13}-[a-zA-Z0-9-]{10,13}", "Slack Token"),
]

# 白名单文件（不检查）
WHITELIST_FILES = [
    "config.local.py",
    "config.py",
    "config_template.py",
    ".gitignore",
    "check_sensitive.py",
]


def check_file(filepath):
    """检查单个文件"""
    issues = []

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
            lines = content.split("\n")
    except Exception as e:
        return [(0, f"读取失败：{e}")]

    for line_num, line in enumerate(lines, 1):
        # 跳过注释和空行
        stripped = line.strip()
        if stripped.startswith("#") or not stripped:
            continue

        # 检查每个模式
        for pattern, description in SENSITIVE_PATTERNS:
            if re.search(pattern, line, re.IGNORECASE):
                # 跳过占位符
                if "your-" in line.lower() or "xxx" in line.lower() or "placeholder" in line.lower():
                    continue
                issues.append((line_num, f"{description}: {line.strip()[:80]}..."))

    return issues


def check_directory(root_dir):
    """递归检查目录"""
    all_issues = {}

    for dirpath, dirnames, filenames in os.walk(root_dir):
        # 跳过特定目录
        if any(ignored in dirpath for ignored in [".git", "__pycache__", "venv", "env", ".venv", "node_modules"]):
            continue

        for filename in filenames:
            # 检查文件扩展名
            if not any(filename.endswith(ext) for ext in CHECKED_EXTENSIONS):
                continue

            # 跳过白名单文件
            if filename in WHITELIST_FILES:
                continue

            filepath = os.path.join(dirpath, filename)

            # 跳过 month2 目录（代码文件中的占位符是预期的）
            if "month2" in filepath:
                continue

            # 检查文件
            issues = check_file(filepath)

            if issues:
                all_issues[filepath] = issues

    return all_issues


def print_report(all_issues):
    """打印检查报告"""
    if not all_issues:
        print("\n✅ 未发现敏感信息！")
        return True

    print("\n" + "=" * 70)
    print("⚠️  发现潜在敏感信息！")
    print("=" * 70)

    total_issues = 0
    for filepath, issues in all_issues.items():
        print(f"\n📁 {filepath}")
        for line_num, issue in issues:
            print(f"   行 {line_num}: {issue}")
            total_issues += 1

    print("\n" + "=" * 70)
    print(f"共发现 {total_issues} 个潜在问题")
    print("=" * 70)

    print("\n💡 建议:")
    print("   1. 使用 config.local.py 存储 API Key")
    print("   2. 使用环境变量存储敏感配置")
    print("   3. 确保 config.local.py 在 .gitignore 中")
    print("   4. 不要提交包含真实密钥的文件")

    return False


def main():
    """主函数"""
    print("=" * 70)
    print("敏感信息检查工具")
    print("=" * 70)

    # 检查当前目录
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    print(f"\n正在检查：{root_dir}")

    all_issues = check_directory(root_dir)
    is_clean = print_report(all_issues)

    # 返回退出码
    sys.exit(0 if is_clean else 1)


if __name__ == "__main__":
    main()
