from rich import print
from rich.panel import Panel
from datetime import datetime


def print_header(title: str):
    print(Panel.fit(f"[bold cyan]{title}[/bold cyan]"))


def print_success(label: str, value: str):
    now = datetime.now().strftime("%H:%M:%S")
    print(f"[bold green][{now}] ✔ {label}:[/bold green] {value}")


def print_info(label: str, value: str):
    now = datetime.now().strftime("%H:%M:%S")
    print(f"[bold blue][{now}] {label}:[/bold blue] {value}")


def print_warning(message: str):
    now = datetime.now().strftime("%H:%M:%S")
    print(f"[bold yellow][{now}] ⚠ {message}[/bold yellow]")


def print_error(message: str):
    now = datetime.now().strftime("%H:%M:%S")
    print(f"[bold red][{now}] ✖ {message}[/bold red]")
