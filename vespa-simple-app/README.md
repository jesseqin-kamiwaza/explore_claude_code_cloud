# Vespa Cloud 简单示例应用

这是一个最简单的 Vespa Cloud 应用示例，演示如何将文档索引到 Vespa 并进行查询。

## 项目结构

```
vespa-simple-app/
├── schemas/
│   └── document.sd          # 文档 schema 定义
├── sample_data/             # 示例数据文件
│   ├── article1.txt
│   ├── article2.txt
│   └── article3.txt
├── services.xml             # Vespa 服务配置
├── deployment.xml           # Vespa Cloud 部署配置
├── requirements.txt         # Python 依赖
├── index_documents.py       # 文档索引程序
├── batch_index.py           # 批量索引工具
├── query_documents.py       # 文档查询程序
├── config.example.py        # 配置示例
├── quickstart.sh            # 快速开始脚本
└── README.md               # 本文档
```

## Vespa 简介

**Vespa** 是一个开源的大数据服务引擎，特别适合用于：
- 全文搜索
- 向量搜索
- 推荐系统
- 实时数据分析

**Vespa Cloud** 是托管版本的 Vespa，无需自己管理基础设施。

## 快速开始

如果你想快速体验，可以运行快速开始脚本：

```bash
chmod +x quickstart.sh
./quickstart.sh
```

该脚本会检查环境并提示你完成设置步骤。

## 前置要求

1. **Python 3.7+**
2. **Vespa Cloud 账户**（在 https://cloud.vespa.ai 注册）
3. **Vespa CLI**（可选，用于部署应用）

## 安装步骤

### 1. 安装 Python 依赖

```bash
pip install -r requirements.txt
```

### 2. 安装 Vespa CLI

```bash
# macOS
brew install vespa-cli

# Linux
curl -fsSL https://github.com/vespa-engine/vespa/releases/latest/download/vespa-cli_linux_amd64.tar.gz | tar -xz -C /usr/local/bin

# 或下载预编译版本
# https://github.com/vespa-engine/vespa/releases
```

### 3. 登录 Vespa Cloud

```bash
vespa auth login
```

### 4. 创建 Vespa Cloud 应用

在 Vespa Cloud 控制台创建一个新应用，或使用 CLI：

```bash
vespa config set application <tenant>.<application>.<instance>
# 例如: vespa config set application mytenant.myapp.default
```

### 5. 部署应用到 Vespa Cloud

```bash
# 在项目根目录执行
vespa deploy
```

等待部署完成（通常需要几分钟）。

### 6. 获取应用端点

部署完成后，你可以获取应用的端点 URL：

```bash
vespa status
```

或在 Vespa Cloud 控制台查看。

## 使用方法

### 配置端点

在使用索引和查询程序之前，需要修改程序中的端点 URL：

编辑 `index_documents.py` 和 `query_documents.py`，将以下行替换为你的实际端点：

```python
VESPA_CLOUD_ENDPOINT = "https://your-app.your-tenant.aws-us-east-1c.z.vespa-app.cloud/"
```

### 索引文档

#### 方法 1: 使用基础索引程序

运行索引程序将文档添加到 Vespa：

```bash
python index_documents.py
```

程序会索引预定义的示例文档。你可以修改 `index_documents.py` 中的 `documents` 列表来索引自己的数据。

**从文件索引**：

取消注释 `index_documents.py` 中的文件读取部分：

```python
file_path = "your_file.txt"
content = read_file(file_path)
documents.append({
    "id": "doc_from_file",
    "title": "从文件加载的文档",
    "content": content,
    "timestamp": int(time.time())
})
```

#### 方法 2: 使用批量索引工具（推荐）

批量索引工具可以自动读取目录中的所有文件并索引到 Vespa：

```bash
# 索引示例数据
python batch_index.py sample_data --endpoint YOUR_VESPA_ENDPOINT

# 只索引特定类型的文件
python batch_index.py /path/to/docs --endpoint YOUR_ENDPOINT --extensions .txt .md

# 指定批处理大小
python batch_index.py /path/to/docs --endpoint YOUR_ENDPOINT --batch-size 50
```

参数说明：
- `directory`: 要索引的目录路径（必需）
- `--endpoint`: Vespa Cloud 端点 URL（必需）
- `--extensions`: 文件扩展名过滤（可选，例如：`.txt .md .json`）
- `--batch-size`: 批处理大小，默认 100（可选）

### 查询文档

运行查询程序搜索文档：

```bash
python query_documents.py
```

程序提供三种查询方式：

1. **简单全文搜索** - 在所有字段中搜索
2. **高级字段查询** - 指定在特定字段中搜索
3. **交互式查询** - 持续输入查询进行搜索

## Schema 说明

文档 schema 定义在 `schemas/document.sd`：

```
schema document {
    document document {
        field id type string           # 文档 ID
        field title type string        # 标题（可搜索）
        field content type string      # 内容（可搜索）
        field timestamp type long      # 时间戳
    }
}
```

**字段属性说明**：
- `indexing: summary | index` - 字段可被索引和返回
- `index: enable-bm25` - 启用 BM25 排序算法
- `attribute: fast-search` - 启用快速搜索

## API 使用示例

### 使用 HTTP API 索引文档

```bash
curl -X POST \
  -H "Content-Type: application/json" \
  --data '{
    "fields": {
      "id": "doc1",
      "title": "示例标题",
      "content": "示例内容",
      "timestamp": 1234567890
    }
  }' \
  https://your-endpoint/document/v1/content/document/docid/doc1
```

### 使用 HTTP API 查询

```bash
curl "https://your-endpoint/search/?yql=select%20*%20from%20document%20where%20userQuery()&query=搜索词"
```

## 常见问题

### 1. 认证错误

如果遇到认证错误，确保已登录：
```bash
vespa auth login
```

### 2. 部署失败

检查配置文件语法，确保 `services.xml` 和 `deployment.xml` 格式正确。

### 3. 查询没有结果

确保文档已成功索引，可以使用 Vespa 控制台查看文档数量。

### 4. 连接超时

检查端点 URL 是否正确，应用是否已成功部署。

## 进阶功能

### 添加向量搜索

修改 schema 添加向量字段：

```
field embedding type tensor<float>(x[384]) {
    indexing: attribute | index
    index {
        hnsw {
            max-links-per-node: 16
            neighbors-to-explore-at-insert: 200
        }
    }
}
```

### 自定义排序

在 schema 中添加自定义 rank-profile：

```
rank-profile custom {
    first-phase {
        expression: bm25(title) * 2 + bm25(content)
    }
}
```

### 聚合查询

使用 YQL 进行聚合：

```python
response = vespa_app.query(
    yql="select * from document where true | all(group(timestamp) each(output(count())))"
)
```

## 相关资源

- [Vespa 官方文档](https://docs.vespa.ai/)
- [Vespa Cloud 文档](https://cloud.vespa.ai/en/)
- [pyvespa 文档](https://pyvespa.readthedocs.io/)
- [Vespa 示例应用](https://github.com/vespa-engine/sample-apps)

## 许可证

MIT

## 贡献

欢迎提交 Issue 和 Pull Request！
