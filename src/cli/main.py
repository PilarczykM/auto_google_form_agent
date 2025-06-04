import os

import click
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from phoenix.otel import register
from playwright.sync_api import sync_playwright

from agents.google_form_crew import create_bio_generator_crew, create_form_crew
from agents.tools.vision_question_analyzer import form_question_vision_analyzer_tool
from parsers.google_form_parser import LIST_ITEMS_SELECTOR, extract_questions, fill_question, submit_form
from utils.fs_utils import reset_screenshot_dir
from utils.json_utils import str_to_json
from utils.print_styles import print_header, print_success
from utils.yaml_utils import load_prompts

load_dotenv()

PHOENIX_API_KEY = os.getenv("PHOENIX_API_KEY")
PHOENIX_ENDPOINT = os.getenv("PHOENIX_ENDPOINT")
os.environ["PHOENIX_CLIENT_HEADERS"] = f"api_key={PHOENIX_API_KEY}"


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
    reset_screenshot_dir()

    register(project_name="google-form-agent", auto_instrument=True, endpoint=PHOENIX_ENDPOINT)

    llm = ChatOpenAI(model="gpt-4o-mini")
    previous_bios = []

    for i in range(20):
        print(f"Iteration {i}")
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

                try:
                    crew = create_bio_generator_crew(lang, llm)
                    bio = crew.kickoff(inputs={"previous_bios": "\n\n".join(previous_bios)})
                    previous_bios.append(str(bio))
                except RuntimeError as e:
                    print(f"Error: {e}")
                except Exception as e:
                    print(f"Unexpected error: {e}")

                try:
                    crew = create_form_crew(lang, llm)
                    for result in results:
                        question = str_to_json(result, strip_tags=["thinking", "processing"])
                        answer = crew.kickoff(inputs={"question": question, "bio": str(bio)})
                        question["answer"] = str(answer)
                        fill_question(page, question)
                except RuntimeError as e:
                    print(f"Error: {e}")
                except Exception as e:
                    print(f"Unexpected error: {e}")

                submit_form(page)
            except Exception as e:
                print(e)
            finally:
                browser.close()
                continue  # noqa: B012


if __name__ == "__main__":
    main()
