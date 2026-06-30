import json
import time
import os

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt

console = Console()


def mostrar_menu():
    menu = """
[bold yellow]1 - Cadastrar contato[/bold yellow]
[bold yellow]2 - Listar contatos[/bold yellow]
[bold yellow]3 - Buscar contato[/bold yellow]
[bold yellow]4 - Editar telefone[/bold yellow]
[bold yellow]5 - Remover contato[/bold yellow]
[bold red]6 - Sair[/bold red]
"""

    console.print(
        Panel(
            menu,
            title="[bold cyan]MENU PRINCIPAL[/bold cyan]",
            border_style="cyan"
        )
    )


def pausar():
    console.input("\n[bold]Pressione ENTER para continuar...[/bold]")


def limpar_tela():
    os.system("cls" if os.name == "nt" else "clear")


def carregar_agenda():
    try:
        with open("agenda.json", "r", encoding="utf-8") as arquivo:
            return json.load(arquivo)

    except FileNotFoundError:
        console.print("[yellow]Arquivo não encontrado. Criando lista vazia.[/yellow]")
        return []

    except json.JSONDecodeError:
        console.print("[yellow]Arquivo vazio ou inválido. Criando lista vazia.[/yellow]")
        return []


def salvar_agenda():
    with open("agenda.json", "w", encoding="utf-8") as arquivo:
        json.dump(agenda, arquivo, indent=4, ensure_ascii=False)


agenda = carregar_agenda()


def criar_tabela_contato(titulo, contato):
    tabela = Table(title=titulo)

    tabela.add_column("Nome", style="cyan")
    tabela.add_column("Telefone", style="green")
    tabela.add_column("Email", style="yellow")
    tabela.add_column("Compromisso", style="magenta")

    tabela.add_row(
        str(contato["nome"]),
        str(contato["telefone"]),
        str(contato["email"]),
        str(contato.get("compromisso", "Sem compromisso"))
    )

    console.print(tabela)


def cadastrar_contato():
    nome = Prompt.ask("[cyan]Digite o nome[/cyan]")
    telefone = Prompt.ask("[cyan]Digite o telefone[/cyan]")
    email = Prompt.ask("[cyan]Digite o email[/cyan]")
    compromisso = Prompt.ask("[cyan]Digite o tipo de compromisso[/cyan]")

    contato = {
        "nome": nome,
        "telefone": telefone,
        "email": email,
        "compromisso": compromisso
    }

    agenda.append(contato)

    console.print("[blue]Salvando contato...[/blue]")
    time.sleep(1)

    salvar_agenda()
    console.print("[green]Contato salvo com sucesso![/green]")


def listar_contatos():
    console.print("[blue]Listando contatos...[/blue]")
    time.sleep(1)

    if len(agenda) == 0:
        console.print("[red]A agenda está vazia[/red]")
        return

    tabela = Table(title="Agenda de Contatos")

    tabela.add_column("Nome", style="cyan", no_wrap=True)
    tabela.add_column("Telefone", style="green")
    tabela.add_column("Email", style="yellow")
    tabela.add_column("Compromisso", style="magenta")

    for contato in agenda:
        tabela.add_row(
            str(contato["nome"]),
            str(contato["telefone"]),
            str(contato["email"]),
            str(contato.get("compromisso", "Sem compromisso"))
        )

    console.print(tabela)


def buscar_contato():
    nome_buscado = Prompt.ask("[cyan]Digite o nome que deseja buscar[/cyan]").lower()

    console.print(f"[blue]Buscando contato {nome_buscado}...[/blue]")
    time.sleep(1)

    for contato in agenda:
        if contato["nome"].lower() == nome_buscado:
            console.print("[green]Contato encontrado![/green]")
            criar_tabela_contato("Contato Encontrado", contato)
            return contato

    console.print(f"[red]Nenhum contato com {nome_buscado} foi encontrado. Tente novamente.[/red]")
    return None


def editar_telefone():
    nome_buscado = Prompt.ask("[cyan]Digite o nome que deseja buscar[/cyan]").lower()

    console.print(f"[blue]Buscando o contato {nome_buscado}...[/blue]")
    time.sleep(1)

    for contato in agenda:
        if contato["nome"].lower() == nome_buscado:
            console.print("[green]Contato encontrado![/green]")
            criar_tabela_contato("Contato Encontrado", contato)

            novo_telefone = Prompt.ask("[cyan]Digite o novo telefone para atualizar[/cyan]")

            console.print("[blue]Atualizando telefone...[/blue]")
            time.sleep(2)

            contato["telefone"] = novo_telefone
            salvar_agenda()

            console.print("[green]Telefone registrado com sucesso![/green]")
            return

    console.print("[red]Contato não encontrado[/red]")


def remover_contato():
    nome_buscado = Prompt.ask("[cyan]Digite o nome que deseja remover[/cyan]").lower()

    console.print("[blue]Buscando contato...[/blue]")
    time.sleep(1)

    for contato in agenda:
        if contato["nome"].lower() == nome_buscado:
            console.print("[green]Contato encontrado![/green]")
            criar_tabela_contato("Contato que será removido", contato)

            confirmar = Prompt.ask(
                "[yellow]Tem certeza que deseja remover esse contato?[/yellow]",
                choices=["s", "n"]
            ).lower()

            if confirmar == "s":
                agenda.remove(contato)
                salvar_agenda()
                console.print(f"[green]Contato {contato['nome']} foi excluído com sucesso![/green]")
            else:
                console.print("[yellow]Remoção cancelada.[/yellow]")

            return

    console.print("[red]Contato não encontrado. Tente novamente.[/red]")


while True:
    limpar_tela()
    mostrar_menu()

    escolha = Prompt.ask(
        "[bold cyan]Qual opção você deseja[/bold cyan]",
        choices=["1", "2", "3", "4", "5", "6"]
    )

    print()

    if escolha == "1":
        cadastrar_contato()
        pausar()

    elif escolha == "2":
        listar_contatos()
        pausar()

    elif escolha == "3":
        buscar_contato()
        pausar()

    elif escolha == "4":
        editar_telefone()
        pausar()

    elif escolha == "5":
        remover_contato()
        pausar()

    elif escolha == "6":
        console.print("[red]Encerrando programa...[/red]")
        time.sleep(2)
        break