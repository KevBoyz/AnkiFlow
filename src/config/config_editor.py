import json
import os
from pathlib import Path

CONFIG_PATH = Path(__file__).resolve().parent / "config.json"

def get_config():
    """Lê as configurações do arquivo JSON, preenchendo campos ausentes com valores padrão."""
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

    # Se uma config está vazia, o default é escrito
    merged = default_config | {k: v for k, v in config.items() if v not in (None, "")}
    if merged != config:
        save_config(merged)
    return merged

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