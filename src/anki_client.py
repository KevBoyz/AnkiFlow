import requests
from .config.config_editor import get_config


class AnkiClient:
    def __init__(self):
        config = get_config()

        self.url = config.get("anki_url", "http://localhost:8765")
        self.deck_name = config.get("default_deck_name", "AnkiFlow")
        self.model_name = "Básico"

    def _invoke(self, action, **params):
        payload = {"action": action, "version": 6, "params": params}
        try:
            response = requests.post(self.url, json=payload, timeout=5)
            response.raise_for_status()
            res_json = response.json()

            if res_json.get('error'):
                raise Exception(res_json['error'])
            return res_json['result']

        except requests.exceptions.ConnectionError:
            raise ConnectionError(
                f"Não foi possível conectar ao Anki em {self.url}. O Anki está aberto?"
            )

    def _get_available_models(self):
        return self._invoke("modelNames")

    def _ensure_model(self):
        models = self._get_available_models()

        if self.model_name not in models:
            if "Basic (and reverse card)" in models:
                self.model_name = "Basic (and reverse card)"
            else:
                raise Exception(
                    f"Modelo '{self.model_name}' não encontrado. Disponíveis: {models}"
                )

    def create_card(self, front, back):
        front = str(front).strip()
        back = str(back).strip()

        if not front or not back:
            raise ValueError("Front ou Back estão vazios")

        self._ensure_model()

        note = {
            "deckName": self.deck_name,
            "modelName": self.model_name,
            "fields": {
                "Frente": front,
                "Verso": back
            },
            "options": {"allowDuplicate": False},
            "tags": ["ankiflow_automation"]
        }

        self._invoke("createDeck", deck=self.deck_name)
        return self._invoke("addNote", note=note)