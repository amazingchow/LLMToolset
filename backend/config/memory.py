"""Memory configuration for the memory calculator."""

# Data type sizes in bytes
DATA_TYPE_SIZES = {
    "float32": 4,
    "float16": 2,
    "bfloat16": 2,  # 一种半精度浮点格式，与传统的 float32 相比，它能将模型大小和内存占用减半，同时保持与 float32 相似的数值范围，非常适合用于训练和推理大型神经网络。
    "int8": 1,
    "int4": 0.5,
}
# Available data types
DATA_TYPES = list(DATA_TYPE_SIZES.keys())
# Attention mechanisms
ATTENTION_MECHANISMS = [
    # 算法架构层面的注意力机制
    "Multi-Head Attention",
    "Multi-Query Attention",
    "Grouped-Query Attention",
    # 系统实现层面的注意力机制，不改变模型架构本身
    "Flash Attention",
    "Page Attention",
]
# Optimizer memory multipliers
OPTIMIZERS_SIZE = {
    "Adam": 8,  # 2 * 4 = 8，为每个参数存储两个状态（动量和方差）
    "AdamW": 8,  # 2 * 4 = 8，为每个参数存储两个状态（动量和方差）
    "Quantized AdamW": 2,  # 2 * 1 = 2，量化后的 AdamW
    "SGD": 4,  # 1 * 4 = 4，为每个参数存储一个状态（动量）
}
# Available optimizers
OPTIMIZERS = list(OPTIMIZERS_SIZE.keys())
# SFT or PEFT
SFT_OR_PEFT = [
    "SFT",
    "LoRA",
    "QLoRA",
]
# Model parameters mapping
PARAMETERS = {
    "model_size": "model_size",
    "precision": "torch_dtype",
    "num_hidden_layers": "num_hidden_layers",
    "hidden_size": "hidden_size",
    "num_attention_heads": "num_attention_heads",
    "head_dim": "head_dim",
    "num_key_value_heads": "num_key_value_heads",
}
