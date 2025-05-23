from playwright.sync_api import Page, sync_playwright

from utils.string_utils import sanitize_filename

LIST_ITEMS_SELECTOR = 'div[role="listitem"]'
HEADING_SELECTOR = "div[role='heading']"
INPUT_TEXT_SELECTOR = "input[type='text']"
RADIO_SELECTOR = "div[role='radio']"


def _extract_questions(page: Page) -> list[dict]:
    question_elements = page.query_selector_all(LIST_ITEMS_SELECTOR)
    questions = []
    idx = 1
    for el in question_elements:
        heading = el.query_selector(HEADING_SELECTOR)
        if not heading:
            continue

        question_text = heading.inner_text().strip()
        sanitized = sanitize_filename(question_text)
        img_path = f"screenshots/{idx}_{sanitized}.png"
        el.screenshot(path=img_path)

        questions.append({"question": question_text, "img_path": img_path})

        idx += 1

    return questions


def extract_google_form(form_url: str) -> list[dict]:
    """Extract questions from a public Google Form and saves screenshots of each question.

    Parameters
    ----------
    form_url : str
        The URL of the public Google Form.

    Returns
    -------
    list of dict
        A list of dictionaries with question text and path to screenshot:
        [{'question': str, 'img_path': str}, ...]

    """
    with sync_playwright() as sp:
        try:
            browser = sp.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(form_url, timeout=60000)
            page.wait_for_selector(LIST_ITEMS_SELECTOR, timeout=10000)

            questions = _extract_questions(page)
        finally:
            browser.close()
        return questions
