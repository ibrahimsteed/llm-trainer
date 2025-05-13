# 该文件定义了 Ollama 模型配置，用于配置与 Ollama 服务的连接。
# 配置项包括模型名称、API 类型和客户端主机地址。
# 请确保在 Ollama 中已拉取指定的模型。

# Ollama 模型配置
config_list = [
    {
        "model": "qwen3:4b",  # 确保在 Ollama 中已拉取此模型
        "api_type": "ollama",
        "client_host": "http://127.0.0.1:11434",  # Ollama 主机
    }
]
