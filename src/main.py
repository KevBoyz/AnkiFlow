import click
from rich.console import Console
from rich.panel import Panel
from rich import box
from rich.table import Table
from src.translator import DeepLTranslator
from src.config.config_editor import get_config, update_setting
from src.anki_client import AnkiClient


console = Console()


def response_output(translations, source, target):
    source_width = None
    target_width = None

    longest_source = max(len(original) for original, _ in translations)
    longest_target = max(len(translated) for _, translated in translations)

    if longest_target >= 40:
        source_width = 40
    if longest_source >= 20:
            target_width = 20

    total_source_chars = sum(len(original) for original, _ in translations)
    total_target_chars = sum(len(translated) for _, translated in translations)

    table = Table(show_header=True, header_style="green",
                  box=box.ROUNDED, border_style='grey50',
                  show_footer=True)
    table.add_column(f"Source ({source.upper()})", style="bright_black",
                     width=target_width, footer=f"{total_source_chars} chars",
                     footer_style='gray74')
    table.add_column(f"Target ({target.upper()})", style="bold cyan",
                     width=source_width, footer=f"{total_target_chars} chars",
                     footer_style='gray74',)

    for original, translated in translations:
        table.add_row(original, translated)

    console.print(table)


@click.group()
def cli():
    """AnkiFlow: Translation helper and Anki integration tool."""
    pass


@cli.group()
def config():
    """Manages settings."""
    pass


@config.command(name="show")
def show_config():
    """Displays the current settings."""
    settings = get_config()

    table = Table(title="AnkiFlow Settings",
                  show_header=True, header_style="bold blue")
    table.add_column("Key", style="cyan")
    table.add_column("Value", style="magenta")

    for key, value in settings.items():
        table.add_row(key, str(value))

    console.print(table)


@config.command(name="set")
@click.argument("key")
@click.argument("value")
def set_config(key, value):
    """Changes a specific setting. Ex: set default_deck_name 'My Terms'"""
    # Simple validation for known keys (optional)
    valid_keys = [
        "default_deck_name", 'anki_path'
        "anki_url", 'anki_basic_model']

    if key not in valid_keys:
        console.print(
            f"[yellow]Warning:[/yellow] The key '{key}' is not standard, but will be saved.")

    if update_setting(key, value):
        console.print(
            f"[bold green]Success![/bold green] '{key}' updated to '{value}'.")
    else:
        console.print(
            "[bold red]Error:[/bold red] Could not save the setting.")


@cli.command()
@click.argument('text', nargs=-1)
@click.option('--source', '-s', default='en', help='Source language (default: en)')
@click.option('--target', '-t', default='pt', help='Target language (default: pt)')
@click.option('--save/--no-save', default=True, help='Automatically save to Anki (default: enabled)')
def translate(text, source, target, save):
    """Make a translation and save a card. Use / to separate multiple terms."""

    full_text = " ".join(text)

    if not full_text:
        console.print("[yellow]Warning:[/yellow] Enter something to translate.")
        return

    terms = [term.strip() for term in full_text.split("/") if term.strip()]

    translations = []

    try:
        with console.status("[bold green]Querying DeepL..."):
            translator = DeepLTranslator(source, target)
            for term in terms:
                result = translator(term)
                translations.append((term, result))

        response_output(translations, source, target)

        if save:
            anki = AnkiClient()
            errors = []

            with console.status("[bold blue]Saving to Anki..."):
                for original, translated in translations:
                    try:
                        anki.create_card(front=original, back=translated)
                    except Exception as e:
                        # Truncate the term for display if it's too long
                        label = original if len(original) <= 15 else original[:15].rsplit(" ", 1)[0] + "..."
                        errors.append((label, str(e)))

            saved_count = len(translations) - len(errors)
            if saved_count > 0:
                console.print(f"[bold green]{saved_count} card(s) saved to Anki![/bold green]")

            for label, err in errors:
                console.print(
                    f"[yellow]Warning:[/yellow] Could not save '[bold]{label}[/bold]': {err}")
        else:
            console.print("[dim]Cards not saved (--no-save)[/dim]")

    except Exception as e:
        console.print(Panel(f"[red]Error:[/red] {str(e)}", title="Operation Failed"))


if __name__ == "__main__":
    cli()
