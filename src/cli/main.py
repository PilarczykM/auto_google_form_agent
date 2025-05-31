import click
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from playwright.sync_api import sync_playwright

from agents.google_form_crew import create_bio_generator_crew, create_form_crew
from agents.tools.vision_question_analyzer import form_question_vision_analyzer_tool
from parsers.google_form_parser import LIST_ITEMS_SELECTOR, extract_questions, fill_question, submit_form
from utils.fs_utils import reset_screenshot_dir
from utils.json_utils import str_to_json
from utils.print_styles import print_header, print_success
from utils.yaml_utils import load_prompts

load_dotenv()


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

    llm = ChatOpenAI(model="gpt-4o-mini")

    with sync_playwright() as sp:
        try:
            browser = sp.chromium.launch(headless=False)
            page = browser.new_page()
            page.goto(form_url, timeout=60000)
            page.wait_for_selector(LIST_ITEMS_SELECTOR, timeout=10000)

            questions = extract_questions(page)
            results = []
            prompts = load_prompts(lang)
            description = prompts["form_question_analysis_task"]["description"]
            expected_output = prompts["form_question_analysis_task"]["expected_output"]

            for question in questions:
                result = form_question_vision_analyzer_tool(
                    description=description, expected_output=expected_output, image_path=str(question["img_path"])
                )
                results.append(result)

            crew = create_bio_generator_crew(lang, llm)
            bio = crew.kickoff()

            crew = create_form_crew(lang, llm)
            for result in results:
                question = str_to_json(result, strip_tags=["thinking", "processing"])
                answer = crew.kickoff(inputs={"question": question, "bio": str(bio)})
                question["answer"] = str(answer)
                fill_question(page, question)

            submit_form(page)
        finally:
            browser.close()


if __name__ == "__main__":
    main()
