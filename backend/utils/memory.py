import warnings
from typing import Dict, List, Tuple

from config.memory import (
    DATA_TYPE_SIZES,
    OPTIMIZERS_SIZE,
)

# Memory calculation utilities for LLM training and inference
#
# Unit conventions:
#   - model_size: in billions of parameters (B)
#   - All memory calculations return values in GB (using 1024^3 bytes = 1 GB)
#   - model_size (B) * bytes_per_param directly gives GB since 1B params ≈ 1GB at 1 byte/param


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
    """Calculate the memory required for model weights in GB.

    For standard models: memory = params * bytes_per_param
    For mixed quantization: memory = (quantized_params * quantized_bytes) +
                                     (non_quantized_params * normal_bytes)

    Args:
        model_size: Model size in billions of parameters
        precision: Model weights precision (e.g., 'float32', 'float16', 'int8')
        is_mixed_quantized: Whether the model uses mixed quantization
        mixed_quantized_ratio: Fraction of parameters that are quantized (0.0-1.0)
        mixed_quantized_precision: Precision of quantized parameters

    Returns:
        Model weights memory in GB
    """
    try:
        if not is_mixed_quantized:
            # Simple case: all parameters use same precision
            # model_size (billions) * bytes_per_param = GB (since 1B ≈ 1GB at 1 byte/param)
            return model_size * DATA_TYPE_SIZES[precision]

        # Mixed quantization: some params at lower precision
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
    """Calculate the memory required for key-value cache in GB.

    Formula: 2 (K+V) * layers * kv_heads * head_dim * seq * batch * bytes

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

    Returns:
        KV cache memory in GB
    """
    try:
        # KV cache: 2 (for K and V) * layers * kv_heads * head_dim * seq * batch * bytes
        kv_size_bytes = (
            2
            * num_hidden_layers
            * num_key_value_heads
            * head_dim
            * sequence_length
            * batch_size
            * DATA_TYPE_SIZES[precision]
        )

        # Page Attention reduces memory by ~86% through efficient memory paging
        if use_page_attention:
            kv_size_bytes = kv_size_bytes * 0.14

        # Convert bytes to GB (using 1024^3)
        return kv_size_bytes / (1024**3)
    except Exception as e:
        warnings.warn(f"Error calculating KV cache memory: {str(e)}")
        return 0


def _get_activation_memory(
    precision: str,
    batch_size: int,
    sequence_length: int,
    hidden_size: int,
    num_hidden_layers: int,
    use_flash_attention: bool = False,
) -> float:
    """Calculate the memory required for activations in GB.

    Activations include: attention outputs, FFN outputs, residual connections,
    and layer normalizations across all transformer layers.

    Standard formula: batch * seq * hidden * layers * factor * bytes
    - factor ≈ 12 for standard attention (stores attention matrices)
    - factor ≈ 1 for Flash Attention (doesn't materialize attention matrices)

    Args:
        precision: Activation precision
        batch_size: Batch size
        sequence_length: Input sequence length
        hidden_size: Hidden layer size (d_model)
        num_hidden_layers: Number of transformer layers
        use_flash_attention: Whether Flash Attention is used

    Returns:
        Activation memory in GB
    """
    try:
        if use_flash_attention:
            # Flash Attention: no attention matrix materialization
            # Only store essential activations (FFN, residuals, norms)
            factor = 1
        else:
            # Standard Attention: stores full attention matrices + activations
            # Attention matrix: batch * heads * seq * seq (dominates memory)
            # Plus FFN activations, residuals, layer norms
            factor = 12

        activation_size_bytes = (
            batch_size * sequence_length * hidden_size * num_hidden_layers * factor * DATA_TYPE_SIZES[precision]
        )

        # Convert bytes to GB (using 1024^3)
        return activation_size_bytes / (1024**3)
    except Exception as e:
        warnings.warn(f"Error calculating activation memory: {str(e)}")
        return 0


def _get_optimizer_memory(
    model_size: int,
    optimizer: str,
) -> float:
    """Calculate the memory required for optimizer states in GB.

    Optimizer memory stores momentum, variance, and other state information
    for each parameter being trained.

    Memory multipliers:
    - Adam/AdamW: 8 bytes per param (2 states × 4 bytes for fp32)
    - SGD with momentum: 4 bytes per param (1 state × 4 bytes)
    - Quantized AdamW: 2 bytes per param (quantized states)

    Args:
        model_size: Model size in billions of parameters
        optimizer: Optimizer type ('Adam', 'AdamW', 'SGD', 'Quantized AdamW')

    Returns:
        Optimizer memory in GB
    """
    try:
        # model_size (billions) * multiplier (bytes/param) = GB
        return model_size * OPTIMIZERS_SIZE[optimizer]
    except Exception as e:
        warnings.warn(f"Error calculating optimizer memory: {str(e)}")
        return 0


def _get_gradient_memory(
    model_size: int,
    precision: str = "float32",
) -> float:
    """Calculate the memory required for gradients in GB.

    Note: Gradients are typically stored in float32 for numerical stability,
    even when the model uses lower precision (fp16/bf16). This is the default
    behavior in mixed-precision training frameworks like AMP.

    Args:
        model_size: Model size in billions of parameters
        precision: Gradients precision (default: float32 for stability)

    Returns:
        Gradient memory in GB
    """
    try:
        # model_size is in billions, DATA_TYPE_SIZES gives bytes per param
        # Since 1B params * 1 byte ≈ 1 GB, we get GB directly
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
        hidden_size,
        num_hidden_layers,
        use_flash_attention,
    )
    # 额外开销 (framework overhead, CUDA context, etc.)
    # Typically 10-20% of total memory, here we use 15%
    base_memory = model_weights + kv_cache + activation_memory
    overhead_memory = base_memory * 0.15
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
        hidden_size,
        num_hidden_layers,
        use_flash_attention,
    )
    # 优化器状态占用的 VRAM
    optimizer_memory = _get_optimizer_memory(model_size, optimizer) * trainable_parameters / 100
    # 梯度占用的 VRAM
    # Note: Using float32 for gradients even if model is fp16/bf16 (common in mixed-precision training)
    gradient_precision = "float32"  # Standard practice for numerical stability
    gradients_memory = _get_gradient_memory(model_size, gradient_precision) * trainable_parameters / 100
    # 额外开销 (framework overhead, CUDA context, communication buffers, etc.)
    # Typically 10-20% of total memory, here we use 15%
    base_memory = model_weights + activation_memory + optimizer_memory + gradients_memory
    overhead_memory = base_memory * 0.15
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
