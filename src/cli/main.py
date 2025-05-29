import click
from playwright.sync_api import sync_playwright

from agents.google_form_crew import create_bio_generator_crew, create_form_crew, create_form_question_analyzer_crew
from parsers.google_form_parser import LIST_ITEMS_SELECTOR, extract_questions, fill_question
from utils.fs_utils import reset_screenshot_dir
from utils.image_utils import encode_image_to_base64
from utils.json_utils import str_to_json
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

    with sync_playwright() as sp:
        try:
            browser = sp.chromium.launch(headless=False)
            page = browser.new_page()
            page.goto(form_url, timeout=60000)
            page.wait_for_selector(LIST_ITEMS_SELECTOR, timeout=10000)

            questions = extract_questions(page)

            crew = create_form_question_analyzer_crew(lang)
            results = []
            for question in questions:
                result = crew.kickoff(inputs={"encoded_image": encode_image_to_base64(question["img_path"])})
                results.append(str(result))

            crew = create_bio_generator_crew(lang)
            bio = crew.kickoff()

            # Loop through questions and add answer as result.
            # question = """
            # {
            #     "type": "radio",
            #     "question": "Płeć",
            #     "options": ["Kobieta", "Mężczyzna", "Nie chcę podawać"],
            #     "required": true,
            #     "context": "",
            #     "answer" : "Kobieta",
            #     "confidence": 0.99
            # }
            # """
            # question = """
            # {
            #     "type": "text",
            #     "question": "Jakie jedno usprawnienie najbardziej poprawiłoby Twój komfort udziału w rekrutacjach?",
            #     "required": true,
            #     "context": "",
            #     "answer" : "Brak",
            #     "confidence": 0.99
            # }
            # """

            #             question = """
            # {
            #   "type": "checkbox",
            #   "question": "Z jakich portali/źródeł najczęściej korzystasz przy poszukiwaniu pracy?",
            #   "options": [
            #     "LinkedIn",
            #     "JustJoin.IT",
            #     "NoFluff.Jobs",
            #     "Pracuj.pl",
            #     "Bezpośredni kontakt do rekrutera",
            #     "Discord/ Facebook"
            #   ],
            #   "required": true,
            #   "context": "",
            #   "confidence": 0.98,
            #   "allow_custom_option": true,
            #   "answer": ["LinkedIn", "Bezpośredni kontakt do rekrutera"]
            # }
            # """
            #             question = """
            # {
            #   "type": "scale_matrix",
            #   "question": "Oceń przydatność poniższych metod rekrutacji z Twojej perspektywy (skala 1-5).",
            #   "rows": [
            #     "Aplikowanie przez portal ogłoszeniowy",
            #     "Sourcing na LinkedIn",
            #     "Polecenia znajomych",
            #     "Hackhatony i meetupy",
            #     "Rekrutacje wewnętrzne",
            #     "Bezpośredni kontakt z rekruterem"
            #   ],
            #   "scale": ["1", "2", "3", "4", "5"],
            #   "required": true,
            #   "context": "1 - brak znajomości, 5 - ekspert",
            #   "confidence": 0.97,
            #   "answer": {
            #     "Aplikowanie przez portal ogłoszeniowy": "5",
            #     "Sourcing na LinkedIn": "4",
            #     "Polecenia znajomych": "4",
            #     "Hackhatony i meetupy": "1",
            #     "Rekrutacje wewnętrzne": "2",
            #     "Bezpośredni kontakt z rekruterem": "4"
            #   }
            # }
            # """

            question = """
            {
            "type": "linear_scale",
            "question": "Jak oceniasz jakość komunikacji z rekruterami w ostatnich procesach, 
            w których brałeś/aś udział?",
            "scale": ["1", "2", "3", "4", "5"],
            "required": true,
            "context": "1 - nieskuteczne, 5 - bardzo skuteczne",
            "confidence": 0.97,
            "answer": "4"
            }
            """

            question = str_to_json(question, strip_tags=["thinking", "processing"])
            crew = create_form_crew(lang)
            result = crew.kickoff(inputs={"question": question, "bio": str(bio)})
            question["answer"] = str(result)

            fill_question(page, question)
        finally:
            browser.close()


if __name__ == "__main__":
    main()
