import json
import os
from pathlib import Path

CONFIG_PATH = Path(__file__).resolve().parent / "config.json"

def get_config():
    """Reads settings from the JSON file, filling missing fields with default values."""
    default_config = {
        "default_deck_name": "AnkiFlow",
        "anki_url": "http://localhost:8765",
        "anki_path": rf"C:\Users\{os.getlogin()}\AppData\Local\Programs\Anki\anki.exe",
        "anki_basic_model": "Básico",
    }
    if not CONFIG_PATH.exists():
        save_config(default_config)
        return default_config

    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            config = json.load(f)
    except (json.JSONDecodeError, IOError):
        save_config(default_config)
        return default_config

    # If a config value is empty, the default is written
    merged = default_config | {k: v for k, v in config.items() if v not in (None, "")}
    if merged != config:
        save_config(merged)
    return merged

def save_config(config_dict):
    """Saves a dictionary to the config.json file."""
    try:
        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump(config_dict, f, indent=4, ensure_ascii=False)
        return True
    except IOError:
        return False

def update_setting(key, value):
    """Updates a specific key without overwriting the others."""
    config = get_config()
    config[key] = value
    return save_config(config)