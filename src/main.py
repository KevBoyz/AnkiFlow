import click
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from src.translator import DeepLTranslator 
from src.config.config_editor import get_config, update_setting
from src.anki_client import AnkiClient


console = Console()

@click.group()
def cli():
    """AnkiFlow: Facilitador de tradução e integração com Anki."""
    pass

@cli.group()
def config():
    """Gerencia as configurações do AnkiFlow."""
    pass

@config.command(name="show")
def show_config():
    """Exibe as configurações atuais."""
    settings = get_config()
    
    table = Table(title="Configurações do AnkiFlow", show_header=True, header_style="bold blue")
    table.add_column("Chave", style="cyan")
    table.add_column("Valor", style="magenta")

    for key, value in settings.items():
        table.add_row(key, str(value))

    console.print(table)

@config.command(name="set")
@click.argument("key")
@click.argument("value")
def set_config(key, value):
    """Altera uma configuração específica. Ex: set default_deck_name 'Meus Termos'"""
    # Validação simples para chaves conhecidas (opcional)
    valid_keys = ["default_deck_name", "anki_url"]
    
    if key not in valid_keys:
        console.print(f"[yellow]Aviso:[/yellow] A chave '{key}' não é padrão, mas será salva.")

    if update_setting(key, value):
        console.print(f"[bold green]Sucesso![/bold green] '{key}' atualizado para '{value}'.")
    else:
        console.print("[bold red]Erro:[/bold red] Não foi possível salvar a configuração.")


@cli.command()
@click.argument('text', nargs=-1)
@click.option('--source', '-s', default='en', help='Idioma de origem (padrão: en)')
@click.option('--target', '-t', default='pt', help='Idioma de destino (padrão: pt)')
@click.option('--save/--no-save', default=True, help='Salvar automaticamente no Anki (padrão: ativo)')
def translate(text, source, target, save):
    """Traduz uma palavra ou frase e exibe formatado."""
    
    full_text = " ".join(text)
    
    if not full_text:
        console.print("[yellow]Aviso:[/yellow] Digite algo para traduzir.")
        return

    try:
        with console.status("[bold green]Consultando DeepL..."):
            translator = DeepLTranslator(source, target) 
            resultado = translator(full_text)

        table = Table(title="Resultado da Tradução", show_header=True, header_style="bold magenta")
        table.add_column(f"Origem ({source.upper()})", style="dim", width=20)
        table.add_column(f"Destino ({target.upper()})", style="bold cyan")
        table.add_row(full_text, resultado)

        console.print(Panel(table, expand=False, border_style="green"))

        if save:
            try:
                with console.status("[bold blue]Salvando no Anki..."):
                    anki = AnkiClient()
                    anki.create_card(front=full_text, back=resultado)

                console.print("[bold green]✔ Cartão salvo no Anki![/bold green]")

            except Exception as e:
                console.print(f"[yellow]Aviso:[/yellow] Traduziu, mas não salvou no Anki: {e}")
        else:
            console.print("[dim]Cartão não salvo (--no-save)[/dim]")

    except Exception as e:
        console.print(Panel(f"[red]Erro:[/red] {str(e)}", title="Falha na Operação"))

if __name__ == "__main__":
    cli()