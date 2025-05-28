import click

from agents.google_form_crew import create_bio_generator_crew, create_form_crew, create_form_question_analyzer_crew
from parsers.google_form_parser import extract_google_form
from utils.fs_utils import reset_screenshot_dir
from utils.image_utils import encode_image_to_base64
from utils.print_styles import print_header, print_success


@click.command()
@click.option("--lang", required=True)
@click.option("--form-url", required=True)
@click.option("--enforce-quality-check", is_flag=True)
def main(lang, form_url, enforce_quality_check):
    """Entry point for the AutoGF-Agent CLI.

    Parses command-line arguments to configure the form-filling agent,
    and displays the provided configuration parameters in a styled format.

    Parameters
    ----------
    lang : str
        Language code for the form responses (e.g., "en", "pl").
    form_url : str
        URL to the public Google Form that will be processed.
    enforce_quality_check : bool
        If True, enables a supervisor agent to evaluate and optionally regenerate answers.

    """
    print_header("AutoGF-Agent CLI")
    print_success("Language", lang)
    print_success("Form URL", form_url)
    print_success("Quality Check Enabled", str(enforce_quality_check))

    reset_screenshot_dir()

    questions = extract_google_form(form_url)

    crew = create_form_question_analyzer_crew(lang)
    results = []
    for question in questions:
        result = crew.kickoff(inputs={"encoded_image": encode_image_to_base64(question["img_path"])})
        results.append(str(result))

    crew = create_bio_generator_crew(lang)
    bio = crew.kickoff()

    crew = create_form_crew(lang)
    result = crew.kickoff(inputs={"question": question, "bio": str(bio)})

    print("Generated Answer:")
    print(result)


if __name__ == "__main__":
    main()
