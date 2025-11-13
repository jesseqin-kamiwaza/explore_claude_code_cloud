#!/usr/bin/env python3
"""
简单的 Vespa 查询程序
用于从 Vespa Cloud 中查询文档
"""

from vespa.application import Vespa


def query_documents(vespa_app: Vespa, query_text, hits=10):
    """
    查询 Vespa 中的文档

    Args:
        vespa_app: Vespa 应用实例
        query_text: 查询文本
        hits: 返回结果数量

    Returns:
        查询结果
    """
    print(f"\n查询: '{query_text}'")
    print("-" * 50)

    # 使用 YQL (Vespa Query Language) 进行查询
    response = vespa_app.query(
        yql=f"select * from document where userQuery()",
        query=query_text,
        hits=hits
    )

    return response


def display_results(response):
    """显示查询结果"""
    if response.is_successful():
        hits = response.hits

        if not hits:
            print("没有找到匹配的文档")
            return

        print(f"找到 {len(hits)} 个结果:\n")

        for i, hit in enumerate(hits, 1):
            fields = hit['fields']
            relevance = hit.get('relevance', 0)

            print(f"{i}. {fields.get('title', 'N/A')} (相关度: {relevance:.4f})")
            print(f"   ID: {fields.get('id', 'N/A')}")
            print(f"   内容: {fields.get('content', 'N/A')[:100]}...")
            print()

    else:
        print(f"查询失败: {response.status_code}")
        print(f"错误信息: {response.get_json()}")


def advanced_query(vespa_app: Vespa, title_query=None, content_query=None):
    """
    高级查询示例 - 可以指定字段查询

    Args:
        vespa_app: Vespa 应用实例
        title_query: 标题查询文本
        content_query: 内容查询文本
    """
    conditions = []

    if title_query:
        conditions.append(f'title contains "{title_query}"')

    if content_query:
        conditions.append(f'content contains "{content_query}"')

    where_clause = " or ".join(conditions) if conditions else "true"

    print(f"\n高级查询:")
    print(f"  标题包含: {title_query if title_query else 'N/A'}")
    print(f"  内容包含: {content_query if content_query else 'N/A'}")
    print("-" * 50)

    response = vespa_app.query(
        yql=f"select * from document where {where_clause}",
        hits=10
    )

    return response


def main():
    """主函数"""
    # Vespa Cloud 连接配置
    # 请替换为你的实际配置
    VESPA_CLOUD_ENDPOINT = "https://your-app.your-tenant.aws-us-east-1c.z.vespa-app.cloud/"

    print("连接到 Vespa Cloud...")
    print(f"端点: {VESPA_CLOUD_ENDPOINT}")

    # 创建 Vespa 应用连接
    vespa_app = Vespa(url=VESPA_CLOUD_ENDPOINT)

    # 示例 1: 简单查询
    print("\n" + "=" * 50)
    print("示例 1: 简单全文搜索")
    print("=" * 50)

    response = query_documents(vespa_app, "搜索引擎")
    display_results(response)

    # 示例 2: 另一个查询
    print("\n" + "=" * 50)
    print("示例 2: 搜索向量相关内容")
    print("=" * 50)

    response = query_documents(vespa_app, "向量")
    display_results(response)

    # 示例 3: 高级查询
    print("\n" + "=" * 50)
    print("示例 3: 高级字段查询")
    print("=" * 50)

    response = advanced_query(
        vespa_app,
        title_query="Vespa",
        content_query=None
    )
    display_results(response)

    # 交互式查询
    print("\n" + "=" * 50)
    print("交互式查询模式")
    print("=" * 50)
    print("输入 'quit' 或 'exit' 退出")

    while True:
        try:
            query_text = input("\n请输入查询: ").strip()

            if query_text.lower() in ['quit', 'exit', 'q']:
                print("退出查询程序")
                break

            if not query_text:
                print("请输入查询文本")
                continue

            response = query_documents(vespa_app, query_text)
            display_results(response)

        except KeyboardInterrupt:
            print("\n\n退出查询程序")
            break
        except Exception as e:
            print(f"错误: {str(e)}")


if __name__ == "__main__":
    main()
