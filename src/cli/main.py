import click

from parsers.google_form_parser import extract_google_form
from utils.fs_utils import reset_screenshot_dir
from utils.print_styles import print_header, print_success


@click.command()
@click.option("--lang", required=True)
@click.option("--personality", required=True)
@click.option("--form-url", required=True)
@click.option("--enforce-quality-check", is_flag=True)
def main(lang, personality, form_url, enforce_quality_check):
    """Entry point for the AutoGF-Agent CLI.

    Parses command-line arguments to configure the form-filling agent,
    and displays the provided configuration parameters in a styled format.

    Parameters
    ----------
    lang : str
        Language code for the form responses (e.g., "en", "pl").
    personality : str
        Comma-separated list of personality traits for the response style
        (e.g., "formal, polite, concise").
    form_url : str
        URL to the public Google Form that will be processed.
    enforce_quality_check : bool
        If True, enables a supervisor agent to evaluate and optionally regenerate answers.

    """
    print_header("AutoGF-Agent CLI")
    print_success("Language", lang)
    print_success("Personality Traits", personality)
    print_success("Form URL", form_url)
    print_success("Quality Check Enabled", str(enforce_quality_check))

    reset_screenshot_dir()

    questions = extract_google_form(form_url)
    print(questions)


if __name__ == "__main__":
    main()
