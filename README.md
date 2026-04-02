# AnkiFlow

Facilitador de tradução e integração automática com o Anki. Traduza palavras e frases diretamente para cartões no Anki usando a API do DeepL.

## Funcionalidades

- Tradução rápida de texto via DeepL.
- Integração automática com Anki através do AnkiConnect.
- Interface de linha de comando rica com Rich.
- Gerenciamento de configurações (deck padrão, URL do Anki).
- Suporte a múltiplos idiomas.

## Instalação

### Pré-requisitos

- Python 3.8 ou superior.
- Conta no [DeepL](https://www.deepl.com/) para obter uma chave de API.
- Anki instalado com o plugin [AnkiConnect](https://ankiweb.net/shared/info/2055492159) ativado.

### Passos

1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/ankiflow.git
   cd ankiflow
   ```

2. Crie um ambiente virtual:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # No Windows
   ```

3. Instale as dependências:
   ```bash
   pip install -e .
   ```

4. Configure o arquivo `.env` com sua chave do DeepL:
   ```
   DEEPL_API_KEY=sua_chave_aqui
   ```

## Configuração

### Configurações do Anki

Use os comandos de configuração para ajustar o deck padrão e a URL do AnkiConnect:

- Exibir configurações atuais:
  ```bash
  ankiflow config show
  ```

- Alterar uma configuração:
  ```bash
  ankiflow config set default_deck_name "Meu Deck"
  ankiflow config set anki_url "http://localhost:8765"
  ```

### Arquivo de Configuração

As configurações são salvas em `src/config/config.json`. Valores padrão:
- `default_deck_name`: "AnkiFlow"
- `anki_url`: "http://localhost:8765"

## Uso

### Comando de Tradução

Traduza uma palavra ou frase e salve automaticamente no Anki:

```bash
ankiflow translate hello world
```

Opções:
- `--source` ou `-s`: Idioma de origem (padrão: en).
- `--target` ou `-t`: Idioma de destino (padrão: pt).
- `--save` ou `--no-save`: Salvar no Anki (padrão: salvar).

Exemplos:
- Traduzir sem salvar:
  ```bash
  ankiflow translate good morning --no-save
  ```

- Traduzir de português para inglês:
  ```bash
  ankiflow translate bom dia --source pt --target en
  ```

### Outros Comandos

- Ajuda geral:
  ```bash
  ankiflow --help
  ```

- Ajuda de um comando específico:
  ```bash
  ankiflow translate --help
  ```

## Estrutura do Projeto

```
AnkiFlow/
├── src/
│   ├── __init__.py
│   ├── main.py          # CLI principal
│   ├── translator.py    # Classe DeepLTranslator
│   ├── anki_client.py   # Integração com AnkiConnect
│   └── config/
│       ├── __init__.py
│       ├── config.json  # Configurações
│       └── config_editor.py  # Gerenciamento de config
├── pyproject.toml       # Configuração do pacote
├── requirements.txt     # Dependências
├── .env                 # Chave do DeepL (não versionar)
└── README.md
```

## Dependências

- `deep-translator`: Para tradução via DeepL.
- `requests`: Para comunicação com AnkiConnect.
- `python-dotenv`: Para carregar variáveis de ambiente.
- `click`: Para CLI.
- `rich`: Para interface rica no terminal.

## Desenvolvimento

Para contribuir:
1. Fork o repositório.
2. Crie uma branch para sua feature.
3. Faça commit das mudanças.
4. Abra um Pull Request.

## Licença

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.

## Suporte

Se encontrar problemas:
- Verifique se o AnkiConnect está rodando (porta 8765).
- Confirme sua chave do DeepL.
- Abra uma issue no GitHub.