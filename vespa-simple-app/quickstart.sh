#!/bin/bash
# Vespa Cloud 快速开始脚本

set -e

echo "================================"
echo "Vespa Cloud 快速开始"
echo "================================"
echo ""

# 检查 Python
if ! command -v python3 &> /dev/null; then
    echo "错误: 未找到 Python 3"
    exit 1
fi

# 安装依赖
echo "1. 安装 Python 依赖..."
pip3 install -r requirements.txt
echo "✓ 依赖安装完成"
echo ""

# 检查配置
if [ ! -f "config.py" ]; then
    echo "2. 创建配置文件..."
    echo "请复制 config.example.py 为 config.py 并填入你的配置"
    echo ""
    echo "运行以下命令："
    echo "  cp config.example.py config.py"
    echo "  # 然后编辑 config.py 填入你的 Vespa Cloud 端点"
    echo ""
else
    echo "2. ✓ 配置文件已存在"
    echo ""
fi

# 检查 Vespa CLI
if command -v vespa &> /dev/null; then
    echo "3. ✓ Vespa CLI 已安装"
    echo ""
else
    echo "3. Vespa CLI 未安装"
    echo "安装方法："
    echo "  macOS: brew install vespa-cli"
    echo "  Linux: 访问 https://github.com/vespa-engine/vespa/releases"
    echo ""
fi

echo "================================"
echo "下一步："
echo "================================"
echo ""
echo "1. 登录 Vespa Cloud:"
echo "   vespa auth login"
echo ""
echo "2. 配置应用:"
echo "   vespa config set application <tenant>.<app>.<instance>"
echo ""
echo "3. 部署应用:"
echo "   vespa deploy"
echo ""
echo "4. 索引示例数据:"
echo "   python3 batch_index.py sample_data --endpoint YOUR_ENDPOINT --extensions .txt"
echo ""
echo "5. 查询数据:"
echo "   python3 query_documents.py"
echo ""
