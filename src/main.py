import click
from rich.console import Console
from rich.panel import Panel
from rich import box
from rich.table import Table
from src.translator import DeepLTranslator
from src.config.config_editor import get_config, update_setting
from src.anki_client import AnkiClient


console = Console()


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
    """Make a translation and save a card"""

    full_text = " ".join(text)

    if not full_text:
        console.print(
            "[yellow]Warning:[/yellow] Enter something to translate.")
        return

    try:
        with console.status("[bold green]Querying DeepL..."):
            translator = DeepLTranslator(source, target)
            result = translator(full_text)

        source_width = None
        target_width = None

        if len(result) >= 34:
            source_width = 34
            if len(full_text) >= 17:
                target_width = 17
        else:
            if len(full_text)>= 15:
                target_width = 15

        table = Table(show_header=True, header_style="green",
                      box=box.ROUNDED, border_style='grey50')
        table.add_column(f"Source ({source.upper()})", style="bright_black", width=target_width)
        table.add_column(f"Target ({target.upper()})", style="bold cyan", width=source_width)
        table.add_row(full_text, result)

        console.print(table)

        if save:
            try:
                with console.status("[bold blue]Saving to Anki..."):
                    anki = AnkiClient()
                    anki.create_card(front=full_text, back=result)

                console.print("[bold green]Card saved to Anki![/bold green]")

            except Exception as e:
                console.print(
                    f"[yellow]Warning:[/yellow] Translated, but could not save to Anki: {e}")
        else:
            console.print("[dim]Card not saved (--no-save)[/dim]")

    except Exception as e:
        console.print(
            Panel(f"[red]Error:[/red] {str(e)}", title="Operation Failed"))


if __name__ == "__main__":
    cli()
