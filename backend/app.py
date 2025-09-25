"""
Flask RESTful API for LLM Memory Usage Calculations

This service provides endpoints to calculate memory requirements for LLM inference and training
based on model configurations and parameters.
"""

import os
import re
from typing import Any, Dict, List

from flask import Flask, jsonify, request
from flask_cors import CORS

from config.memory import DATA_TYPES, OPTIMIZERS, SFT_OR_PEFT
from utils.help import load_predefined_models
from utils.memory import calculate_inference_memory, calculate_training_memory

app = Flask(__name__)
CORS(app)  # Enable CORS for all domains on all routes

# Configuration
MODELS_DIR = os.path.join(os.path.dirname(__file__), "models")
MODELS = load_predefined_models(MODELS_DIR)


def get_available_models() -> List[str]:
    """Get list of available models."""
    models = list(MODELS.keys())
    return sorted(models)


def extract_model_params(model_name: str, config: Dict[str, Any]) -> Dict[str, Any]:
    # 正则表达式：匹配一个数字（可能带小数点），后面跟着 'B' 或 'M'，不区分大小写
    # \d+(\.\d+)?  -> 匹配整数或小数
    # (B|M)        -> 匹配 'B' 或 'M'
    pattern = re.compile(r"\d+(\.\d+)?(B|M)", re.IGNORECASE)
    match = pattern.search(model_name)
    if match:
        model_size = float(match.group(0)[:-1])
    else:
        model_size = None
    return {
        "model_size": model_size,
        "precision": config.get("torch_dtype", "float32"),
        "num_hidden_layers": config.get("num_hidden_layers", 36),
        "hidden_size": config.get("hidden_size", 4096),
        "num_attention_heads": config.get("num_attention_heads", 32),
        "head_dim": config.get("head_dim", 128),
        "num_key_value_heads": config.get(
            "num_key_value_heads", config.get("num_attention_heads", 32)
        ),  # MHA 的 KV 头数等于查询头数
        "use_flash_attention": False,
        "use_page_attention": False,
    }


@app.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint."""
    return jsonify({"status": "healthy", "service": "LLM Memory Calculator API", "version": "1.0.0"})


@app.route("/api/models", methods=["GET"])
def list_models():
    """Get list of available models."""
    try:
        models = get_available_models()
        return jsonify({"models": models, "count": len(models)})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/models/<model_name>", methods=["GET"])
def get_model_info(model_name: str):
    """Get detailed information about a specific model."""
    try:
        config = MODELS[model_name]
        params = extract_model_params(model_name, config)

        return jsonify({"model_name": model_name, "config": config, "extracted_params": params})
    except FileNotFoundError:
        return jsonify({"error": f'Model "{model_name}" not found'}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/memory/inference", methods=["POST"])
def calculate_inference():
    """
    Calculate memory requirements for LLM inference.

    Request body should contain:
    - model_name: Name of model configuration to use
    - precision: Data type precision for model weights
    - batch_size: Batch size for inference
    - sequence_length: Input sequence length
    - kv_cache_precision: Data type precision for KV cache
    - use_flash_attention: Whether to use Flash Attention
    - use_page_attention: Whether to use Page Attention
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Request body is required"}), 400
        if "model_name" not in data:
            return jsonify({"error": "model_name is required"}), 400
        if "batch_size" not in data:
            return jsonify({"error": "batch_size is required"}), 400
        if "sequence_length" not in data:
            return jsonify({"error": "sequence_length is required"}), 400
        if "kv_cache_precision" not in data:
            return jsonify({"error": "kv_cache_precision is required"}), 400

        model_name = data["model_name"]
        config = MODELS[model_name]
        params = extract_model_params(model_name, config)
        for key in [
            "precision",
            "batch_size",
            "sequence_length",
            "kv_cache_precision",
            "use_flash_attention",
            "use_page_attention",
        ]:
            if key in data:
                params[key] = data[key]
        if params.get("precision") not in DATA_TYPES:
            return jsonify({"error": f"Invalid precision. Must be one of: {DATA_TYPES}"}), 400
        result = calculate_inference_memory(
            model_size=params["model_size"],
            precision=params["precision"],
            batch_size=params["batch_size"],
            sequence_length=params["sequence_length"],
            kv_cache_precision=params["kv_cache_precision"],
            num_hidden_layers=params["num_hidden_layers"],
            hidden_size=params["hidden_size"],
            num_attention_heads=params["num_attention_heads"],
            head_dim=params["head_dim"],
            num_key_value_heads=params["num_key_value_heads"],
            use_flash_attention=params["use_flash_attention"],
            use_page_attention=params["use_page_attention"],
        )
        return jsonify({"calculation_type": "inference", "parameters": params, "memory_requirements": result})
    except FileNotFoundError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/memory/training", methods=["POST"])
def calculate_training():
    """
    Calculate memory requirements for LLM training.

    Request body should contain:
    - model_name: Name of model configuration to use
    - precision: Data type precision for model weights
    - batch_size: Batch size for training
    - sequence_length: Input sequence length
    - optimizer: Optimizer type
    - trainable_parameters: Percentage of trainable parameters
    - use_flash_attention: Whether to use Flash Attention
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Request body is required"}), 400
        if "model_name" not in data:
            return jsonify({"error": "model_name is required"}), 400
        if "batch_size" not in data:
            return jsonify({"error": "batch_size is required"}), 400
        if "sequence_length" not in data:
            return jsonify({"error": "sequence_length is required"}), 400
        if "optimizer" not in data:
            return jsonify({"error": "optimizer is required"}), 400
        if "trainable_parameters" not in data:
            return jsonify({"error": "trainable_parameters is required"}), 400

        model_name = data["model_name"]
        config = MODELS[model_name]
        params = extract_model_params(model_name, config)
        for key in [
            "precision",
            "batch_size",
            "sequence_length",
            "optimizer",
            "trainable_parameters",
            "use_flash_attention",
        ]:
            if key in data:
                params[key] = data[key]
        if params.get("precision") not in DATA_TYPES:
            return jsonify({"error": f"Invalid precision. Must be one of: {DATA_TYPES}"}), 400
        if params.get("optimizer") not in OPTIMIZERS:
            return jsonify({"error": f"Invalid optimizer. Must be one of: {OPTIMIZERS}"}), 400

        result = calculate_training_memory(
            model_size=params["model_size"],
            precision=params["precision"],
            batch_size=params["batch_size"],
            sequence_length=params["sequence_length"],
            num_hidden_layers=params["num_hidden_layers"],
            hidden_size=params["hidden_size"],
            num_attention_heads=params["num_attention_heads"],
            head_dim=params["head_dim"],
            num_key_value_heads=params["num_key_value_heads"],
            optimizer=params["optimizer"],
            trainable_parameters=params["trainable_parameters"],
            use_flash_attention=params["use_flash_attention"],
        )
        return jsonify({"calculation_type": "training", "parameters": params, "memory_requirements": result})
    except FileNotFoundError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/config/options", methods=["GET"])
def get_config_options():
    """Get available configuration options (data types, optimizers, etc.)."""
    return jsonify(
        {
            "data_types": DATA_TYPES,
            "optimizers": OPTIMIZERS,
            "sft_or_peft": SFT_OR_PEFT,
            "available_models": get_available_models(),
        }
    )


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({"error": "Endpoint not found"}), 404


@app.errorhandler(405)
def method_not_allowed(error):
    """Handle 405 errors."""
    return jsonify({"error": "Method not allowed"}), 405


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    return jsonify({"error": "Internal server error"}), 500
