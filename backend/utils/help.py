import json
import os


def load_predefined_models(models_dir: str) -> dict:
    models = {}
    for model_file in os.listdir(models_dir):
        if model_file.endswith(".json"):
            with open(os.path.join(models_dir, model_file)) as fr:
                models[model_file[:-5]] = json.load(fr)
    return models
