# src/parking_system/config.py
import yaml
from pathlib import Path
from copy import deepcopy

CONFIG_DIR = Path(__file__).resolve().parent.parent.parent / "configs"

def deep_merge(default: dict, override: dict) -> dict:
    """Recursively merge two dicts: override keys take precedence"""
    result = deepcopy(default)
    for k, v in override.items():
        if k in result and isinstance(result[k], dict) and isinstance(v, dict):
            result[k] = deep_merge(result[k], v)
        else:
            result[k] = v
    return result

def load_config(env="dev"):
    with open(CONFIG_DIR / "defaults.yaml", "r") as f:
        defaults = yaml.safe_load(f)

    env_file = CONFIG_DIR / f"{env}.yaml"
    if env_file.exists():
        with open(env_file, "r") as f:
            env_config = yaml.safe_load(f)
        config = deep_merge(defaults, env_config)
    else:
        config = defaults

    # Optional: sanity check
    if "app" not in config or "name" not in config["app"]:
        raise ValueError("Missing 'app.name' in configuration!")
    return config
