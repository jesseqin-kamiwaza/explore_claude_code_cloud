#!/usr/bin/env python3
"""
简单的 Vespa 文档索引程序
用于将文件内容索引到 Vespa Cloud
"""

import json
import time
from pathlib import Path
from vespa.application import Vespa


def read_file(file_path):
    """读取文件内容"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()


def index_documents(vespa_app: Vespa, documents):
    """
    将文档索引到 Vespa

    Args:
        vespa_app: Vespa 应用实例
        documents: 要索引的文档列表
    """
    print(f"开始索引 {len(documents)} 个文档...")

    success_count = 0
    failed_count = 0

    for doc in documents:
        try:
            response = vespa_app.feed_data_point(
                schema="document",
                data_id=doc["id"],
                fields=doc
            )

            if response.status_code == 200:
                success_count += 1
                print(f"✓ 成功索引文档: {doc['id']}")
            else:
                failed_count += 1
                print(f"✗ 索引失败: {doc['id']} - {response.status_code}")

        except Exception as e:
            failed_count += 1
            print(f"✗ 索引错误: {doc['id']} - {str(e)}")

    print(f"\n索引完成! 成功: {success_count}, 失败: {failed_count}")


def main():
    """主函数"""
    # Vespa Cloud 连接配置
    # 请替换为你的实际配置
    VESPA_CLOUD_ENDPOINT = "https://your-app.your-tenant.aws-us-east-1c.z.vespa-app.cloud/"

    print("连接到 Vespa Cloud...")
    print(f"端点: {VESPA_CLOUD_ENDPOINT}")

    # 创建 Vespa 应用连接
    # 如果使用 Vespa Cloud，需要提供 API key
    vespa_app = Vespa(url=VESPA_CLOUD_ENDPOINT)

    # 示例文档数据
    # 你可以从文件中读取或其他数据源获取
    documents = [
        {
            "id": "doc1",
            "title": "Vespa 简介",
            "content": "Vespa 是一个开源的大数据服务引擎，用于实时计算和提供大规模数据。",
            "timestamp": int(time.time())
        },
        {
            "id": "doc2",
            "title": "搜索引擎基础",
            "content": "搜索引擎是一种用于搜索和检索信息的系统，通常包括索引、查询和排序等功能。",
            "timestamp": int(time.time())
        },
        {
            "id": "doc3",
            "title": "向量搜索",
            "content": "向量搜索使用机器学习模型将文本转换为向量，然后通过向量相似度进行搜索。",
            "timestamp": int(time.time())
        }
    ]

    # 如果你想从文件中读取内容，可以使用以下代码：
    # file_path = "your_file.txt"
    # content = read_file(file_path)
    # documents.append({
    #     "id": "doc_from_file",
    #     "title": "从文件加载的文档",
    #     "content": content,
    #     "timestamp": int(time.time())
    # })

    # 索引文档
    index_documents(vespa_app, documents)


if __name__ == "__main__":
    main()
