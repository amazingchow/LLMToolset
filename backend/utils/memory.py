from typing import Dict, List

from config.memory import (
    DATA_TYPE_SIZES,
    OPTIMIZERS_SIZE,
)


def _get_memory(values: List[int]) -> str:
    """Convert total memory from bytes to human-readable format."""
    total = 0
    warning = False
    for v in values:
        if v > 0:
            total += v
        else:
            warning = True
    # Convert bytes to human-readable format
    if total == 0:
        result = ""
    elif total < 1024:
        result = f"{total} Bytes"
    elif total < 1024**2:
        result = f"{total / 1024:.2f} KB"
    elif total < 1024**3:
        result = f"{total / (1024**2):.2f} MB"
    elif total < 1024**4:
        result = f"{total / (1024**3):.2f} GB"
    else:
        result = f"{total / (1024**4):.2f} TB"
    result += " * " if warning else ""
    return result


def _get_model_weights(
    model_size: int,
    precision: str,
) -> int:
    """Calculate the memory required for model weights."""
    try:
        return model_size * DATA_TYPE_SIZES[precision] * (10**9)
    except Exception:
        return 0


def _get_kv_cache(
    precision: str,
    batch_size: int,
    sequence_length: int,
    hidden_size: int,
    num_hidden_layers: int,
) -> int:
    """Calculate the memory required for key-value cache."""
    try:
        return 2 * batch_size * sequence_length * num_hidden_layers * hidden_size * DATA_TYPE_SIZES[precision]
    except Exception:
        return 0


def _get_activation_memory(
    batch_size: int,
    sequence_length: int,
    hidden_size: int,
    num_attention_heads: int,
) -> int:
    """Calculate the memory required for activations."""
    precision = "float32"
    try:
        return (
            batch_size
            * sequence_length
            * hidden_size
            * (34 + (5 * sequence_length * num_attention_heads) / hidden_size)
            * DATA_TYPE_SIZES[precision]
        )
    except Exception:
        return 0


def _get_optimizer_memory(
    model_size: int,
    optimizer: str,
) -> int:
    """Calculate the memory required for optimizer."""
    try:
        return OPTIMIZERS_SIZE[optimizer] * model_size * (10**9)
    except Exception:
        return 0


def _get_gradient_memory(
    model_size: int,
    precision: str,
) -> int:
    """Calculate the memory required for gradients."""
    precision = "float32"
    try:
        return DATA_TYPE_SIZES[precision] * model_size * (10**9)
    except Exception:
        return 0


def calculate_inference_memory(
    model_size: int,
    precision: str,
    batch_size: int,
    sequence_length: int,
    hidden_size: int,
    num_hidden_layers: int,
    num_attention_heads: int,
) -> Dict[str, str]:
    """Calculate the total memory required for inference."""
    model_weights = _get_model_weights(model_size, precision)
    kv_cache = _get_kv_cache(precision, batch_size, sequence_length, hidden_size, num_hidden_layers)
    activation_memory = _get_activation_memory(batch_size, sequence_length, hidden_size, num_attention_heads)
    return {
        "model_weights": _get_memory([model_weights]),
        "kv_cache": _get_memory([kv_cache]),
        "activation_memory": _get_memory([activation_memory]),
        "inference_memory": _get_memory([model_weights, kv_cache, activation_memory]),
    }


def calculate_training_memory(
    model_size: int,
    precision: str,
    batch_size: int,
    sequence_length: int,
    hidden_size: int,
    num_hidden_layers: int,
    num_attention_heads: int,
    optimizer: str,
    trainable_parameters: int,
) -> Dict[str, str]:
    """Calculate the total memory required for training."""
    model_weights = _get_model_weights(model_size, precision)
    kv_cache = _get_kv_cache(precision, batch_size, sequence_length, hidden_size, num_hidden_layers)
    activation_memory = _get_activation_memory(batch_size, sequence_length, hidden_size, num_attention_heads)
    optimizer_memory = _get_optimizer_memory(model_size, optimizer) * trainable_parameters / 100
    gradients_memory = _get_gradient_memory(model_size, precision) * trainable_parameters / 100

    return {
        "model_weights": _get_memory([model_weights]),
        "kv_cache": _get_memory([kv_cache]),
        "activation_memory": _get_memory([activation_memory]),
        "optimizer_memory": _get_memory([optimizer_memory]),
        "gradients_memory": _get_memory([gradients_memory]),
        "training_memory": _get_memory(
            [model_weights, kv_cache, activation_memory, optimizer_memory, gradients_memory]
        ),
    }
