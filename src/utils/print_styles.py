from datetime import datetime

from rich import print
from rich.panel import Panel


def print_header(title: str):
    """Print a styled header inside a cyan panel box.

    Parameters
    ----------
    title : str
        The title text to display in the panel.

    """
    print(Panel.fit(f"[bold cyan]{title}[/bold cyan]"))


def print_success(label: str, value: str):
    """Print a green-styled success message with a timestamp.

    Parameters
    ----------
    label : str
        The name or key to display (e.g., 'Language').
    value : str
        The corresponding value to display (e.g., 'pl').

    """
    now = datetime.now().strftime("%H:%M:%S")
    print(f"[bold green][{now}] ✔ {label}:[/bold green] {value}")


def print_info(label: str, value: str):
    """Print a blue-styled informational message with a timestamp.

    Parameters
    ----------
    label : str
        The name or key to display.
    value : str
        The corresponding informational value.

    """
    now = datetime.now().strftime("%H:%M:%S")
    print(f"[bold blue][{now}] {label}:[/bold blue] {value}")


def print_warning(message: str):
    """Print a yellow-styled warning message with a timestamp.

    Parameters
    ----------
    message : str
        The warning message to display.

    """
    now = datetime.now().strftime("%H:%M:%S")
    print(f"[bold yellow][{now}] ⚠ {message}[/bold yellow]")


def print_error(message: str):
    """Print a red-styled error message with a timestamp.

    Parameters
    ----------
    message : str
        The error message to display.

    """
    now = datetime.now().strftime("%H:%M:%S")
    print(f"[bold red][{now}] ✖ {message}[/bold red]")
