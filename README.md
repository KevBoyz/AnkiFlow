# AnkiFlow

Translation helper and automatic Anki integration. Translate words and phrases directly into Anki cards using the DeepL API.

## Features

- Fast text translation via DeepL.
- Automatic Anki integration through AnkiConnect.
- Rich command-line interface with Rich.
- Settings management (default deck, Anki URL).
- Support for multiple languages.

## Installation

### Prerequisites

- Python 3.8 or higher.
- A [DeepL](https://www.deepl.com/) account to obtain an API key.
- Anki installed with the [AnkiConnect](https://ankiweb.net/shared/info/2055492159) plugin enabled.

### Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/seu-usuario/ankiflow.git
   cd ankiflow
   ```

2. Create a virtual environment:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # On Windows
   ```

3. Install dependencies:
   ```bash
   pip install -e .
   ```

4. Configure the `.env` file with your DeepL key:
   ```
   DEEPL_API_KEY=your_key_here
   ```

## Configuration

### Anki Settings

Use the config commands to adjust the default deck and AnkiConnect URL:

- Display current settings:
  ```bash
  ankiflow config show
  ```

- Change a setting:
  ```bash
  ankiflow config set default_deck_name "My Deck"
  ankiflow config set anki_url "http://localhost:8765"
  ```

### Configuration File

Settings are saved in `src/config/config.json`. Default values:
- `default_deck_name`: "AnkiFlow"
- `anki_url`: "http://localhost:8765"

## Usage

### Translate Command

Translate a word or phrase and automatically save it to Anki:

```bash
ankiflow translate hello world
```

Options:
- `--source` or `-s`: Source language (default: en).
- `--target` or `-t`: Target language (default: pt).
- `--save` or `--no-save`: Save to Anki (default: save).

Examples:
- Translate without saving:
  ```bash
  ankiflow translate good morning --no-save
  ```

- Translate from Portuguese to English:
  ```bash
  ankiflow translate bom dia --source pt --target en
  ```

### Other Commands

- General help:
  ```bash
  ankiflow --help
  ```

- Help for a specific command:
  ```bash
  ankiflow translate --help
  ```

## Project Structure

```
AnkiFlow/
├── src/
│   ├── __init__.py
│   ├── main.py          # Main CLI
│   ├── translator.py    # DeepLTranslator class
│   ├── anki_client.py   # AnkiConnect integration
│   └── config/
│       ├── __init__.py
│       ├── config.json  # Settings
│       └── config_editor.py  # Config management
├── pyproject.toml       # Package configuration
├── requirements.txt     # Dependencies
├── .env                 # DeepL key (do not version)
└── README.md
```

## Dependencies

- `deep-translator`: For translation via DeepL.
- `requests`: For communication with AnkiConnect.
- `python-dotenv`: For loading environment variables.
- `click`: For CLI.
- `rich`: For rich terminal interface.

## Development

To contribute:
1. Fork the repository.
2. Create a branch for your feature.
3. Commit your changes.
4. Open a Pull Request.

## License

This project is under the MIT license. See the LICENSE file for more details.

## Support

If you encounter issues:
- Check that AnkiConnect is running (port 8765).
- Confirm your DeepL key.
- Open an issue on GitHub.