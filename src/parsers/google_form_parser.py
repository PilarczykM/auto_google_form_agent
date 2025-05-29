from playwright.sync_api import Page

from utils.string_utils import sanitize_filename

LIST_ITEMS_SELECTOR = 'div[role="listitem"]'
HEADING_SELECTOR = "div[role='heading']"
INPUT_TEXT_SELECTOR = "input[type='text']"
RADIO_SELECTOR = "div[role='radio']"


def extract_questions(page: Page) -> list[dict]:
    """Extract questions from a public Google Form and saves screenshots of each question.

    Parameters
    ----------
    page: Page
        The Page of the public Google Form.

    Returns
    -------
    list of dict
        A list of dictionaries with question text and path to screenshot:
        [{'question': str, 'img_path': str}, ...]

    """
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


def _normalize(text):
    import re

    return re.sub(r"\s+", " ", text.strip().lower())


def _fill_radio_question(page: Page, question_data: dict):
    question_text = _normalize(question_data["question"])
    answer_text = _normalize(question_data["answer"])

    question_blocks = page.locator(LIST_ITEMS_SELECTOR).all()

    for block in question_blocks:
        try:
            block_text = block.inner_text(timeout=1000)
        except Exception:
            continue

        if question_text in _normalize(block_text):
            matching_element = None
            for el in block.locator("*").all():
                try:
                    text = el.inner_text(timeout=500)
                    if _normalize(text) == answer_text:
                        matching_element = el
                        break
                except Exception:
                    continue

            if matching_element:
                matching_element.click(force=True)
                return

    err_msg = f"No match for radio answer '{answer_text}' in question '{question_text}'"
    raise ValueError(err_msg)


def fill_text_question(page: Page, question_data: dict):
    question_text = question_data["question"]
    answer_text = question_data["answer"]

    question_el = page.locator(f"text={question_text}").first
    question_el.wait_for(state="visible", timeout=5000)

    # Znajdź najbliższe pole tekstowe (input or textarea)
    input_el = question_el.locator("input, textarea").first
    input_el.fill(answer_text)


def fill_question(page: Page, question_data: dict):
    qtype = question_data["type"]
    if qtype == "radio":
        _fill_radio_question(page, question_data)
    elif qtype == "text":
        fill_text_question(page, question_data)
    else:
        raise NotImplementedError(f"Unsupported question type: {qtype}")
