"""
配置文件示例
复制此文件为 config.py 并填入你的实际配置
"""

# Vespa Cloud 端点 URL
# 格式: https://<app-name>.<tenant-name>.<region>.z.vespa-app.cloud/
VESPA_CLOUD_ENDPOINT = "https://your-app.your-tenant.aws-us-east-1c.z.vespa-app.cloud/"

# Vespa Cloud API Key（如果需要）
# 可以在 Vespa Cloud 控制台生成
VESPA_API_KEY = None

# 应用配置
APPLICATION_TENANT = "your-tenant"
APPLICATION_NAME = "your-app"
APPLICATION_INSTANCE = "default"

# 索引配置
BATCH_SIZE = 100  # 批量索引时的批次大小
INDEX_TIMEOUT = 30  # 索引超时时间（秒）

# 查询配置
DEFAULT_HITS = 10  # 默认返回结果数量
QUERY_TIMEOUT = 5  # 查询超时时间（秒）
