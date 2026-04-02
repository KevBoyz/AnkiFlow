import time
import requests
from config.config_editor import get_config
from rich.console import Console

console = Console()


class AnkiClient:
    def __init__(self):
        config = get_config()

        self.url = config.get("anki_url")
        self.deck_name = config.get("default_deck_name")
        self.anki_path = config.get('anki_path')
        self.basic_model = config.get('anki_basic_model')

    def _start_anki(self):
        """Tenta abrir o Anki se não estiver aberto"""
        import ctypes
        ctypes.windll.shell32.ShellExecuteW(None, "open", self.anki_path, None, None, 1)

    def _wait_for_anki(self, timeout=30):
            """Aguarda o Anki inicializar e aceitar conexões"""
            with console.status("[yellow]Aguardando o Anki inicializar...[/yellow]"):
                for _ in range(timeout):
                    try:
                        r = requests.post(self.url, json={"action": "version", "version": 6}, timeout=3)
                        if r.status_code == 200:
                            return True
                    except Exception:
                        pass
                    time.sleep(0.3)
            return False

    def _try_open_anki(self):
        """Tenta abrir o Anki e aguarda estar pronto. Retorna True se conseguiu."""
        console.print("[yellow]Anki não está aberto. Tentando iniciar...[/yellow]")
        try:
            self._start_anki()
        except FileNotFoundError:
            console.print(f"[red]Executável do Anki não encontrado em '{self.anki_path}'.[/red]")
            return False
        except Exception as e:
            console.print(f"[red]Erro ao tentar abrir o Anki: {e}[/red]")
            return False

        if self._wait_for_anki():
            console.print("[green]✓ Anki iniciado com sucesso![/green]")
            return True

        console.print("[red]✗ Anki não respondeu a tempo. Verifique se está instalado corretamente.[/red]")
        return False

    def _request(self, payload):
        """Executa a requisição HTTP e trata a resposta — sem retry."""
        response = requests.post(self.url, json=payload, timeout=5)
        response.raise_for_status()
        res_json = response.json()
        if res_json.get("error"):
            raise Exception(res_json["error"])
        return res_json["result"]

    def _invoke(self, action, **params):
        payload = {"action": action, "version": 6, "params": params}
        try:
            return self._request(payload)
        except requests.exceptions.ConnectionError:
            if not self._try_open_anki():
                raise ConnectionError(
                    f"Não foi possível conectar ao Anki em {self.url}. "
                    "Verifique se o Anki está instalado e o AnkiConnect está ativo."
                )
            return self._request(payload)

    def _get_available_models(self):
        return self._invoke("modelNames")

    def _ensure_model(self):
        models = self._get_available_models()

        if self.basic_model not in models:
            raise Exception(
                f"""Modelo '{self.basic_model}' não encontrado. Disponíveis:\n{models}\n
                Altere o parâmetro anki_basic_model para um modelo válido."""
            )

    def create_card(self, front, back):
        front = str(front).strip()
        back = str(back).strip()

        if not front or not back:
            raise ValueError("Front ou Back estão vazios")

        self._ensure_model()

        note = {
            "deckName": self.deck_name,
            "modelName": self.basic_model,
            "fields": {
                "Frente": front,
                "Verso": back
            },
            "options": {"allowDuplicate": False},
            "tags": ["ankiflow_automation"]
        }

        self._invoke("createDeck", deck=self.deck_name)
        return self._invoke("addNote", note=note)
    

if __name__ == '__main__':
    client = AnkiClient()
    client._invoke('modelNames')