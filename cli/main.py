import click
from utils.print_styles import print_header, print_success


@click.command()
@click.option("--lang", required=True)
@click.option("--personality", required=True)
@click.option("--form-url", required=True)
@click.option("--enforce-quality-check", is_flag=True)
def main(lang, personality, form_url, enforce_quality_check):
    print_header("AutoGF-Agent CLI")
    print_success("Language", lang)
    print_success("Personality Traits", personality)
    print_success("Form URL", form_url)
    print_success("Quality Check Enabled", str(enforce_quality_check))


if __name__ == "__main__":
    main()
