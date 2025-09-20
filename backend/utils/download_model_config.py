import argparse
import os
import secrets
import time

import requests


def secure_random_float() -> float:
    """
    生成一个在 [0.0, 1.0) 区间内的加密安全随机浮点数。
    """
    # secrets.randbits(53) 生成一个 53 位的随机整数。
    # 53 位是 IEEE 754 双精度浮点数尾数的最大精度。
    # 2**53 是 9007199254740992
    return secrets.randbits(53) / (2**53)


def secure_random_uniform(a: float, b: float) -> float:
    """
    生成一个在 [a, b) 区间内的加密安全随机浮点数。
    """
    return a + (b - a) * secure_random_float()


QWEN_MODELS = [
    "Qwen/Qwen3-235B-A22B-Thinking-2507-FP8",
    "Qwen/Qwen3-235B-A22B-Thinking-2507",
    "Qwen/Qwen3-235B-A22B-Instruct-2507-FP8",
    "Qwen/Qwen3-235B-A22B-Instruct-2507",
    "Qwen/Qwen3-30B-A3B-Thinking-2507-FP8",
    "Qwen/Qwen3-30B-A3B-Thinking-2507",
    "Qwen/Qwen3-30B-A3B-Instruct-2507-FP8",
    "Qwen/Qwen3-30B-A3B-Instruct-2507",
    "Qwen/Qwen3-4B-Thinking-2507-FP8",
    "Qwen/Qwen3-4B-Thinking-2507",
    "Qwen/Qwen3-4B-Instruct-2507-FP8",
    "Qwen/Qwen3-4B-Instruct-2507",
    "Qwen/Qwen3-235B-A22B",
    "Qwen/Qwen3-30B-A3B",
    "Qwen/Qwen3-32B",
    "Qwen/Qwen3-14B",
    "Qwen/Qwen3-8B",
    "Qwen/Qwen3-4B",
    "Qwen/Qwen3-1.7B",
    "Qwen/Qwen3-0.6B",
    "Qwen/Qwen3-235B-A22B-FP8",
    "Qwen/Qwen3-30B-A3B-FP8",
    "Qwen/Qwen3-32B-FP8",
    "Qwen/Qwen3-14B-FP8",
    "Qwen/Qwen3-8B-FP8",
    "Qwen/Qwen3-4B-FP8",
    "Qwen/Qwen3-1.7B-FP8",
    "Qwen/Qwen3-0.6B-FP8",
    "Qwen/Qwen3-235B-A22B-GPTQ-Int4",
    "Qwen/Qwen3-30B-A3B-GPTQ-Int4",
    "Qwen/Qwen3-32B-AWQ",
    "Qwen/Qwen3-14B-AWQ",
    "Qwen/Qwen3-8B-AWQ",
    "Qwen/Qwen3-4B-AWQ",
    "Qwen/Qwen3-1.7B-GPTQ-Int8",
    "Qwen/Qwen3-0.6B-GPTQ-Int8",
    "Qwen/Qwen3-235B-A22B-GGUF",
    "Qwen/Qwen3-30B-A3B-GGUF",
    "Qwen/Qwen3-32B-GGUF",
    "Qwen/Qwen3-14B-GGUF",
    "Qwen/Qwen3-8B-GGUF",
    "Qwen/Qwen3-4B-GGUF",
    "Qwen/Qwen3-1.7B-GGUF",
    "Qwen/Qwen3-0.6B-GGUF",
    "Qwen/Qwen3-30B-A3B-Base",
    "Qwen/Qwen3-14B-Base",
    "Qwen/Qwen3-8B-Base",
    "Qwen/Qwen3-4B-Base",
    "Qwen/Qwen3-1.7B-Base",
    "Qwen/Qwen3-0.6B-Base",
    "Qwen/Qwen3-4B-MLX-8bit",
    "Qwen/Qwen3-4B-MLX-bf16",
    "Qwen/Qwen3-4B-MLX-6bit",
    "Qwen/Qwen3-4B-MLX-4bit",
    "Qwen/Qwen3-8B-MLX-4bit",
    "Qwen/Qwen3-8B-MLX-6bit",
    "Qwen/Qwen3-8B-MLX-8bit",
    "Qwen/Qwen3-8B-MLX-bf16",
    "Qwen/Qwen3-0.6B-MLX-6bit",
    "Qwen/Qwen3-0.6B-MLX-4bit",
    "Qwen/Qwen3-0.6B-MLX-bf16",
    "Qwen/Qwen3-0.6B-MLX-8bit",
    "Qwen/Qwen3-32B-MLX-8bit",
    "Qwen/Qwen3-1.7B-MLX-6bit",
    "Qwen/Qwen3-1.7B-MLX-bf16",
    "Qwen/Qwen3-1.7B-MLX-8bit",
    "Qwen/Qwen3-1.7B-MLX-4bit",
    "Qwen/Qwen3-14B-MLX-6bit",
    "Qwen/Qwen3-14B-MLX-8bit",
    "Qwen/Qwen3-14B-MLX-4bit",
    "Qwen/Qwen3-14B-MLX-bf16",
    "Qwen/Qwen3-32B-MLX-6bit",
    "Qwen/Qwen3-32B-MLX-bf16",
    "Qwen/Qwen3-32B-MLX-4bit",
    "Qwen/Qwen3-30B-A3B-MLX-4bit",
    "Qwen/Qwen3-30B-A3B-MLX-bf16",
    "Qwen/Qwen3-30B-A3B-MLX-8bit",
    "Qwen/Qwen3-30B-A3B-MLX-6bit",
    "Qwen/Qwen3-235B-A22B-MLX-bf16",
    "Qwen/Qwen3-235B-A22B-MLX-6bit",
    "Qwen/Qwen3-235B-A22B-MLX-4bit",
    "Qwen/Qwen3-235B-A22B-MLX-8bit",
]


def download_model_configs(root_dir: str):
    """
    下载所有 QWEN 模型的配置文件到指定目录。

    Args:
        root_dir: 根目录路径，模型配置文件将保存到 {root_dir}/models/ 目录下
    """
    # 确保 models 目录存在
    models_dir = os.path.join(root_dir, "models")
    os.makedirs(models_dir, exist_ok=True)

    session = requests.Session()
    session.headers.update(
        {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36",
            "accept-encoding": "gzip, deflate, br, zstd",
        }
    )

    for model in QWEN_MODELS:
        model_name = model.split("/")[1]

        config_file = os.path.join(models_dir, f"{model_name}.json")
        if os.path.exists(config_file):
            print(f"Model Config for {model_name} already exists.")
            continue

        try:
            print(f"Downloading Model Config for {model_name}...")
            url = f"https://huggingface.co/{model}/raw/main/config.json"
            response = session.get(url)
            response.raise_for_status()

            with open(os.path.join(models_dir, f"{model_name}.json"), "w") as f:
                f.write(response.text)
            print(f"Model Config for {model_name} downloaded successfully.")
        except Exception as e:
            print(f"Error downloading Model Config for {model_name}: {e}")
        finally:
            time_to_sleep = secure_random_uniform(1, 3)
            print(f"Sleeping for {time_to_sleep} seconds...")
            time.sleep(time_to_sleep)


def main():
    parser = argparse.ArgumentParser(description="下载 QWEN 模型配置文件")
    parser.add_argument(
        "--root_dir",
        required=True,
        help="根目录路径，模型配置文件将保存到该目录下的 models 文件夹中",
    )
    args = parser.parse_args()
    print(f"Downloading Model Configs to {args.root_dir}/models...")
    # 检查根目录是否存在，如果不存在则创建
    if not os.path.exists(args.root_dir):
        os.makedirs(args.root_dir, exist_ok=True)
        print(f"创建根目录: {args.root_dir}")

    download_model_configs(args.root_dir)


if __name__ == "__main__":
    main()
