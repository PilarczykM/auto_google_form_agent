import re

from utils import print_styles


def test_print_success_output(capsys):
    print_styles.print_success("Test Label", "Test Value")
    captured = capsys.readouterr().out
    assert "✔ Test Label:" in captured
    assert "Test Value" in captured
    assert re.search(r"\[\d{2}:\d{2}:\d{2}\]", captured)


def test_print_info_output(capsys):
    print_styles.print_info("Info Label", "Info Value")
    captured = capsys.readouterr().out
    assert "Info Label:" in captured
    assert "Info Value" in captured


def test_print_warning_output(capsys):
    print_styles.print_warning("This is a warning")
    captured = capsys.readouterr().out
    assert "⚠ This is a warning" in captured


def test_print_error_output(capsys):
    print_styles.print_error("Something went wrong")
    captured = capsys.readouterr().out
    assert "✖ Something went wrong" in captured


def test_print_header_output(capsys):
    print_styles.print_header("My CLI Header")
    captured = capsys.readouterr().out
    assert "My CLI Header" in captured
