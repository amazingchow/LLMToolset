# LLM Memory Calculator API

这是一个基于Flask的RESTful API服务，用于计算大语言模型(LLM)的内存使用量。

## 功能特性

- 🔍 **模型配置查询**: 查看可用的模型配置和详细信息
- 🧠 **推理内存计算**: 计算LLM推理时的内存需求
- 🎓 **训练内存计算**: 计算LLM训练时的内存需求
- 📊 **配置对比**: 比较不同配置下的内存使用情况
- ⚙️ **参数验证**: 完整的参数验证和错误处理

## 安装和运行

### 1. 安装依赖

```bash
# 使用uv安装依赖
uv sync

# 或者使用pip
pip install flask flask-cors requests
```

### 2. 启动服务

```bash
python server.py
```

服务将在 `http://localhost:5000` 启动。

### 3. 测试API

```bash
python test_api.py
```

## API 端点

### 健康检查

```http
GET /health
```

检查服务状态。

### 模型管理

#### 获取所有可用模型

```http
GET /api/models
```

返回所有可用的模型配置列表。

#### 获取模型详细信息

```http
GET /api/models/{model_name}
```

获取指定模型的详细配置信息。

### 内存计算

#### 推理内存计算

```http
POST /api/memory/inference
```

**请求体示例1 - 使用模型名称:**

```json
{
    "model_name": "Qwen3-0.6B",
    "batch_size": 2,
    "sequence_length": 4096
}
```

**请求体示例2 - 直接指定参数:**

```json
{
    "model_size": 7,
    "precision": "float16",
    "batch_size": 1,
    "sequence_length": 2048,
    "hidden_size": 4096,
    "num_hidden_layers": 32,
    "num_attention_heads": 32
}
```

#### 训练内存计算

```http
POST /api/memory/training
```

**请求体示例:**

```json
{
    "model_name": "Qwen3-7B",
    "batch_size": 4,
    "sequence_length": 2048,
    "optimizer": "AdamW",
    "trainable_parameters": 100
}
```

#### 配置对比

```http
POST /api/memory/compare
```

**请求体示例:**

```json
{
    "calculation_type": "inference",
    "configurations": [
        {
            "model_size": 0.6,
            "precision": "bfloat16",
            "batch_size": 1,
            "sequence_length": 2048,
            "hidden_size": 1024,
            "num_hidden_layers": 28,
            "num_attention_heads": 16
        },
        {
            "model_size": 0.6,
            "precision": "float16",
            "batch_size": 1,
            "sequence_length": 2048,
            "hidden_size": 1024,
            "num_hidden_layers": 28,
            "num_attention_heads": 16
        }
    ]
}
```

### 配置选项

```http
GET /api/config/options
```

获取所有可用的配置选项，包括数据类型、优化器等。

## 响应格式

### 成功响应

```json
{
    "calculation_type": "inference",
    "parameters": {
        "model_size": 7,
        "precision": "float16",
        "batch_size": 1,
        "sequence_length": 2048,
        "hidden_size": 4096,
        "num_hidden_layers": 32,
        "num_attention_heads": 32
    },
    "memory_requirements": {
        "model_weights": "14.00 GB",
        "kv_cache": "1.00 GB",
        "activation_memory": "2.50 GB",
        "inference_memory": "17.50 GB"
    }
}
```

### 错误响应

```json
{
    "error": "Model 'InvalidModel' not found"
}
```

## 支持的数据类型

- `float32`: 4字节
- `float16`: 2字节
- `bfloat16`: 2字节
- `int8`: 1字节
- `int4`: 0.5字节

## 支持的优化器

- `AdamW`: 8倍模型大小
- `Quantized AdamW`: 2倍模型大小
- `SGD`: 4倍模型大小

## 使用示例

### Python示例

```python
import requests

# 计算推理内存
response = requests.post('http://localhost:5000/api/memory/inference', json={
    "model_name": "Qwen3-0.6B",
    "batch_size": 2,
    "sequence_length": 4096
})

result = response.json()
print(f"推理内存需求: {result['memory_requirements']['inference_memory']}")
```

### curl示例

```bash
# 获取可用模型列表
curl http://localhost:5000/api/models

# 计算训练内存
curl -X POST http://localhost:5000/api/memory/training \
  -H "Content-Type: application/json" \
  -d '{
    "model_name": "Qwen3-7B",
    "batch_size": 4,
    "sequence_length": 2048,
    "optimizer": "AdamW",
    "trainable_parameters": 100
  }'
```

## 错误处理

API包含完整的错误处理机制：

- **400 Bad Request**: 参数错误或缺失
- **404 Not Found**: 模型不存在或端点不存在
- **405 Method Not Allowed**: 不支持的HTTP方法
- **500 Internal Server Error**: 服务器内部错误

所有错误响应都包含详细的错误信息。
