#!/usr/bin/env python3
"""
批量索引工具
从指定目录批量读取文件并索引到 Vespa
"""

import os
import time
import hashlib
from pathlib import Path
from vespa.application import Vespa


def get_file_id(file_path):
    """根据文件路径生成唯一 ID"""
    return hashlib.md5(file_path.encode()).hexdigest()


def read_files_from_directory(directory, extensions=None):
    """
    从目录中读取文件

    Args:
        directory: 目录路径
        extensions: 文件扩展名列表，例如 ['.txt', '.md']，None 表示所有文件

    Returns:
        文件列表
    """
    directory_path = Path(directory)

    if not directory_path.exists():
        raise ValueError(f"目录不存在: {directory}")

    files = []

    for file_path in directory_path.rglob('*'):
        if file_path.is_file():
            # 过滤扩展名
            if extensions and file_path.suffix not in extensions:
                continue

            files.append(file_path)

    return files


def file_to_document(file_path):
    """
    将文件转换为 Vespa 文档

    Args:
        file_path: 文件路径

    Returns:
        文档字典
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        doc_id = get_file_id(str(file_path))
        title = file_path.stem  # 文件名（不含扩展名）

        return {
            "id": doc_id,
            "title": title,
            "content": content,
            "timestamp": int(time.time())
        }

    except Exception as e:
        print(f"读取文件失败: {file_path} - {str(e)}")
        return None


def batch_index(vespa_app: Vespa, documents, batch_size=100):
    """
    批量索引文档

    Args:
        vespa_app: Vespa 应用实例
        documents: 文档列表
        batch_size: 批处理大小
    """
    total = len(documents)
    success_count = 0
    failed_count = 0

    print(f"开始批量索引 {total} 个文档...")
    print(f"批处理大小: {batch_size}\n")

    for i, doc in enumerate(documents, 1):
        try:
            response = vespa_app.feed_data_point(
                schema="document",
                data_id=doc["id"],
                fields=doc
            )

            if response.status_code == 200:
                success_count += 1
                print(f"[{i}/{total}] ✓ 成功: {doc['title']}")
            else:
                failed_count += 1
                print(f"[{i}/{total}] ✗ 失败: {doc['title']} - {response.status_code}")

        except Exception as e:
            failed_count += 1
            print(f"[{i}/{total}] ✗ 错误: {doc['title']} - {str(e)}")

        # 每个批次后暂停一下
        if i % batch_size == 0:
            print(f"\n已处理 {i}/{total} 个文档，暂停 1 秒...\n")
            time.sleep(1)

    print(f"\n{'='*50}")
    print(f"批量索引完成!")
    print(f"成功: {success_count}")
    print(f"失败: {failed_count}")
    print(f"总计: {total}")
    print(f"{'='*50}")


def main():
    """主函数"""
    import argparse

    parser = argparse.ArgumentParser(description='批量索引文件到 Vespa Cloud')
    parser.add_argument('directory', help='要索引的目录路径')
    parser.add_argument('--endpoint', required=True, help='Vespa Cloud 端点 URL')
    parser.add_argument('--extensions', nargs='+', help='文件扩展名过滤，例如: .txt .md')
    parser.add_argument('--batch-size', type=int, default=100, help='批处理大小（默认: 100）')

    args = parser.parse_args()

    # 连接到 Vespa
    print(f"连接到 Vespa Cloud: {args.endpoint}")
    vespa_app = Vespa(url=args.endpoint)

    # 读取文件
    print(f"\n读取目录: {args.directory}")
    if args.extensions:
        print(f"过滤扩展名: {args.extensions}")

    files = read_files_from_directory(args.directory, args.extensions)
    print(f"找到 {len(files)} 个文件\n")

    if not files:
        print("没有找到文件，退出。")
        return

    # 转换为文档
    documents = []
    for file_path in files:
        doc = file_to_document(file_path)
        if doc:
            documents.append(doc)

    print(f"成功读取 {len(documents)} 个文档\n")

    # 批量索引
    batch_index(vespa_app, documents, args.batch_size)


if __name__ == "__main__":
    main()
