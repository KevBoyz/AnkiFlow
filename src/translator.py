import os
from pathlib import Path
from dotenv import load_dotenv
import requests

env_path = Path(__file__).resolve().parent.parent / '.env'
load_dotenv(dotenv_path=env_path)


class DeepLTranslator:
    def __init__(self, source='EN', target='PT'):
        self.api_key = os.getenv("DEEPL_API_KEY")

        if not self.api_key:
            raise ValueError(
                "Erro: DEEPL_API_KEY não encontrada no arquivo .env"
            )

        self.source = source.upper()
        self.target = target.upper()

        if self.api_key.endswith(":fx"):
            self.url = "https://api-free.deepl.com/v2/translate"
        else:
            self.url = "https://api.deepl.com/v2/translate"

    def __call__(self, text: str) -> str:
        try:
            response = requests.post(
                self.url,
                headers={
                    "Authorization": f"DeepL-Auth-Key {self.api_key}"
                },
                data={
                    "text": text,
                    "source_lang": self.source,
                    "target_lang": self.target,
                },
                timeout=10
            )

            response.raise_for_status()
            data = response.json()

            return data["translations"][0]["text"]

        except requests.exceptions.RequestException as e:
            return f"Erro na requisição: {e}"

        except (KeyError, IndexError):
            return f"Resposta inesperada da API: {response.text}"