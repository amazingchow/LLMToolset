# Data type sizes in bytes
DATA_TYPE_SIZES = {
    "float32": 4,
    "float16": 2,
    "bfloat16": 2,
    "int8": 1,
    "int4": 0.5,
}
# Available data types
DATA_TYPES = list(DATA_TYPE_SIZES.keys())
# Optimizer memory multipliers
OPTIMIZERS_SIZE = {
    "AdamW": 8,
    "Quantized AdamW": 2,
    "SGD": 4,
}
# Available optimizers
OPTIMIZERS = list(OPTIMIZERS_SIZE.keys())
# Model parameters mapping
PARAMETERS = {
    "model_size": "model_size",
    "precision": "torch_dtype",
    "hidden_size": "hidden_size",
    "num_hidden_layers": "num_hidden_layers",
    "num_attention_heads": "num_attention_heads",
    "num_key_value_heads": "num_key_value_heads",
}
