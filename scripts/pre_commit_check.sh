#!/bin/bash
# 提交前检查脚本

echo "======================================"
echo "提交前检查"
echo "======================================"

# 1. 检查 .env 文件
echo ""
echo "1. 检查 .env 文件..."
if [ -f ".env" ]; then
    if git ls-files --error-unmatch .env &>/dev/null; then
        echo "   ❌ .env 已被 Git 追踪！请运行:"
        echo "      git rm --cached .env"
        exit 1
    else
        echo "   ✅ .env 未被 Git 追踪"
    fi
fi

# 2. 检查敏感信息
echo ""
echo "2. 检查敏感信息..."
python scripts/check_sensitive.py
if [ $? -ne 0 ]; then
    echo "   ❌ 发现敏感信息！请处理后再提交"
    exit 1
fi

# 3. Git 状态
echo ""
echo "3. Git 状态:"
git status

echo ""
echo "======================================"
echo "✅ 检查通过！可以提交"
echo "======================================"
