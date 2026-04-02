import json
import os
from pathlib import Path

CONFIG_PATH = Path(__file__).resolve().parent / "config.json"

def get_config():
    """Lê as configurações do arquivo JSON."""
    default_config = {
        "default_deck_name": "AnkiFlow",
        "anki_url": "http://localhost:8765"
    }

    if not CONFIG_PATH.exists():
        save_config(default_config)
        return default_config

    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return default_config

def save_config(config_dict):
    """Salva um dicionário no arquivo config.json."""
    try:
        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump(config_dict, f, indent=4, ensure_ascii=False)
        return True
    except IOError:
        return False

def update_setting(key, value):
    """Atualiza uma chave específica sem apagar as outras."""
    config = get_config()
    config[key] = value
    return save_config(config)