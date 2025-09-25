import warnings
from typing import Dict, List, Tuple

from config.memory import (
    DATA_TYPE_SIZES,
    OPTIMIZERS_SIZE,
)

# 优化计算，在计算内存的时候，去除10亿这个参数量因子，因为10亿约等于1024*1024*1024，约等于1GB，所以可以去除


def _get_memory(values: List[float], warnings_list: List[str] | None = None) -> Tuple[str, bool]:
    """Convert total memory from bytes to human-readable format.

    Args:
        values: List of memory values in bytes
        warnings_list: Optional list to store warning messages

    Returns:
        Tuple of (formatted memory string, warning flag)
    """
    total = 0
    warning = False
    for v in values:
        if v > 0:
            total += v
        else:
            warning = True
            if warnings_list is not None:
                warnings_list.append("Some memory calculations returned 0 bytes")
    result = f"{total:.2f} GB"
    result += " * " if warning else ""
    return result, warning


def _get_model_weights(
    model_size: int,
    precision: str,
    is_mixed_quantized: bool = False,
    mixed_quantized_ratio: float = 0.0,
    mixed_quantized_precision: str = "int8",
) -> float:
    """Calculate the memory required for model weights.

    Args:
        model_size: Model size in billions of parameters
        precision: Model weights precision
        is_mixed_quantized: Whether the model is mixed quantized
        mixed_quantized_ratio: Ratio of parameters that are mixed quantized
        mixed_quantized_precision: Precision of mixed quantized parameters
    """
    try:
        if not is_mixed_quantized:
            return model_size * DATA_TYPE_SIZES[precision]
        quantized_size = model_size * mixed_quantized_ratio * DATA_TYPE_SIZES[mixed_quantized_precision]
        non_quantized_size = model_size * (1 - mixed_quantized_ratio) * DATA_TYPE_SIZES[precision]
        return quantized_size + non_quantized_size
    except Exception as e:
        warnings.warn(f"Error calculating model weights memory: {str(e)}")
        return 0


def _get_kv_cache(
    precision: str,
    batch_size: int,
    sequence_length: int,
    num_hidden_layers: int,
    hidden_size: int,
    num_attention_heads: int,
    head_dim: int,
    num_key_value_heads: int,
    use_page_attention: bool = False,
) -> float:
    """Calculate the memory required for key-value cache.

    Args:
        precision: KV cache precision
        batch_size: Batch size
        sequence_length: Input sequence length
        num_hidden_layers: Number of hidden layers
        hidden_size: Hidden layer size
        num_attention_heads: Number of attention heads
        head_dim: Head dimension
        num_key_value_heads: Number of key-value heads
        use_page_attention: Whether Page Attention is used
    """
    try:
        # Basic KV cache calculation
        kv_size = (
            2
            * num_hidden_layers
            * num_key_value_heads
            * head_dim
            * sequence_length
            * batch_size
            * DATA_TYPE_SIZES[precision]
        )
        if use_page_attention:
            kv_size = kv_size * 0.14  # Page Attention typically reduces memory by ~86%
        return kv_size / (10**9)
    except Exception as e:
        warnings.warn(f"Error calculating KV cache memory: {str(e)}")
        return 0


def _get_activation_memory(
    precision: str,
    batch_size: int,
    sequence_length: int,
    head_dim: int,
    use_flash_attention: bool = False,
) -> float:
    """Calculate the memory required for activations.

    Args:
        precision: Activation precision
        batch_size: Batch size
        sequence_length: Input sequence length
        head_dim: Head dimension
        use_flash_attention: Whether Flash Attention is used
    """
    try:
        activation_size = sequence_length * sequence_length * batch_size * head_dim * DATA_TYPE_SIZES[precision]
        if use_flash_attention:
            activation_size = sequence_length * batch_size * head_dim * DATA_TYPE_SIZES[precision] * 20
        return activation_size / (1024**3)
    except Exception as e:
        warnings.warn(f"Error calculating activation memory: {str(e)}")
        return 0


def _get_optimizer_memory(
    model_size: int,
    optimizer: str,
) -> float:
    """Calculate the memory required for optimizer.

    Args:
        model_size: Model size in billions of parameters
        optimizer: Optimizer type
    """
    try:
        return model_size * OPTIMIZERS_SIZE[optimizer]
    except Exception as e:
        warnings.warn(f"Error calculating optimizer memory: {str(e)}")
        return 0


def _get_gradient_memory(
    model_size: int,
    precision: str = "float32",
) -> float:
    """Calculate the memory required for gradients.

    Args:
        model_size: Model size in billions of parameters
        precision: Gradients precision
    """
    try:
        return model_size * DATA_TYPE_SIZES[precision]
    except Exception as e:
        warnings.warn(f"Error calculating gradient memory: {str(e)}")
        return 0


def calculate_inference_memory(
    model_size: int,
    precision: str,
    batch_size: int,
    sequence_length: int,
    kv_cache_precision: str,
    num_hidden_layers: int,
    hidden_size: int,
    num_attention_heads: int,
    head_dim: int,
    num_key_value_heads: int,
    use_flash_attention: bool = False,
    use_page_attention: bool = False,
    is_mixed_quantized: bool = False,
    mixed_quantized_ratio: float = 0.0,
    mixed_quantized_precision: str = "int8",
    architecture: str = "decoder_only",
) -> Dict[str, str]:
    """Calculate the total memory required for inference.

    Args:
        model_size: Model size in billions of parameters
        precision: Model weights precision
        batch_size: Batch size for inference
        sequence_length: Input sequence length
        kv_cache_precision: KV cache precision
        num_hidden_layers: Number of hidden layers
        hidden_size: Hidden layer size
        num_attention_heads: Number of attention heads
        head_dim: Head dimension
        num_key_value_heads: Number of key-value heads
        use_flash_attention: Whether to use Flash Attention
        use_page_attention: Whether to use Page Attention
        is_mixed_quantized: Whether the model is mixed quantized
        mixed_quantized_ratio: Ratio of parameters that are mixed quantized
        mixed_quantized_precision: Precision of mixed quantized parameters
        architecture: Model architecture type
    """
    warnings_list = []
    # 模型参数占用的 VRAM
    model_weights = _get_model_weights(
        model_size,
        precision,
        is_mixed_quantized,
        mixed_quantized_ratio,
        mixed_quantized_precision,
    )
    # KV 缓存占用的 VRAM
    kv_cache = _get_kv_cache(
        kv_cache_precision,
        batch_size,
        sequence_length,
        num_hidden_layers,
        hidden_size,
        num_attention_heads,
        head_dim,
        num_key_value_heads,
        use_page_attention,
    )
    # 激活值占用的 VRAM
    activation_memory = _get_activation_memory(
        precision,
        batch_size,
        sequence_length,
        head_dim,
        use_flash_attention,
    )
    # 额外开销
    overhead_memory = 1.04
    # 总 VRAM
    result = {
        "model_weights_memory": _get_memory([model_weights], warnings_list)[0],
        "kv_cache_memory": _get_memory([kv_cache], warnings_list)[0],
        "activation_memory": _get_memory([activation_memory], warnings_list)[0],
        "overhead_memory": _get_memory([overhead_memory], warnings_list)[0],
        "inference_memory": _get_memory([model_weights, kv_cache, activation_memory, overhead_memory], warnings_list)[
            0
        ],
    }
    if warnings_list:
        result["warnings"] = warnings_list
    return result


def calculate_training_memory(
    model_size: int,
    precision: str,
    batch_size: int,
    sequence_length: int,
    num_hidden_layers: int,
    hidden_size: int,
    num_attention_heads: int,
    head_dim: int,
    num_key_value_heads: int,
    optimizer: str,
    trainable_parameters: int,
    use_flash_attention: bool = False,
    is_mixed_quantized: bool = False,
    mixed_quantized_ratio: float = 0.0,
    mixed_quantized_precision: str = "int8",
    architecture: str = "decoder_only",
) -> Dict[str, str]:
    """Calculate the total memory required for training.

    Args:
        model_size: Model size in billions of parameters
        precision: Model weights precision
        batch_size: Batch size for training
        sequence_length: Input sequence length
        num_hidden_layers: Number of hidden layers
        hidden_size: Hidden layer size
        num_attention_heads: Number of attention heads
        head_dim: Head dimension
        num_key_value_heads: Number of key-value heads
        optimizer: Optimizer type
        trainable_parameters: Percentage of trainable parameters
        use_flash_attention: Whether to use Flash Attention
        is_mixed_quantized: Whether the model is mixed quantized
        mixed_quantized_ratio: Ratio of parameters that are mixed quantized
        mixed_quantized_precision: Precision of mixed quantized parameters
        architecture: Model architecture type
    """
    warnings_list = []
    # 模型参数占用的 VRAM
    model_weights = _get_model_weights(
        model_size,
        precision,
        is_mixed_quantized,
        mixed_quantized_ratio,
        mixed_quantized_precision,
    )
    # 激活值占用的 VRAM
    activation_memory = _get_activation_memory(
        precision,
        batch_size,
        sequence_length,
        head_dim,
        use_flash_attention,
    )
    # 优化器状态占用的 VRAM
    optimizer_memory = _get_optimizer_memory(model_size, optimizer) * trainable_parameters / 100
    # 梯度占用的 VRAM
    gradients_memory = _get_gradient_memory(model_size, precision) * trainable_parameters / 100
    # 额外开销
    overhead_memory = 1.54
    # 总 VRAM
    result = {
        "model_weights_memory": _get_memory([model_weights], warnings_list)[0],
        "activation_memory": _get_memory([activation_memory], warnings_list)[0],
        "optimizer_memory": _get_memory([optimizer_memory], warnings_list)[0],
        "gradients_memory": _get_memory([gradients_memory], warnings_list)[0],
        "overhead_memory": _get_memory([overhead_memory], warnings_list)[0],
        "training_memory": _get_memory(
            [model_weights, activation_memory, optimizer_memory, gradients_memory, overhead_memory], warnings_list
        )[0],
    }
    if warnings_list:
        result["warnings"] = warnings_list
    return result
