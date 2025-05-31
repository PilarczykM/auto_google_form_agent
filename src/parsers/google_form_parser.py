from playwright.sync_api import Page

from config.project_paths import ROOT_DIRECTORY
from utils.string_utils import sanitize_filename, str_to_parsed_type

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
        img_path = ROOT_DIRECTORY / f"screenshots/{idx}_{sanitized}.png"
        el.screenshot(path=img_path)

        questions.append({"question": question_text, "img_path": img_path})

        idx += 1

    return questions


def _normalize(text):
    import re

    text = text.strip().strip('"').strip("'")
    return re.sub(r"\s+", " ", text.strip().lower())


def _find_matching_question_block(page: Page, question_text: str):
    question_blocks = page.locator(LIST_ITEMS_SELECTOR).all()
    for block in question_blocks:
        try:
            block_text = block.inner_text(timeout=1000)
            if question_text in _normalize(block_text):
                return block
        except Exception:
            continue
    return None


def _fill_radio_question(page: Page, question_data: dict):
    question_text = _normalize(question_data["question"])
    answer_text = _normalize(question_data["answer"])

    block = _find_matching_question_block(page, question_text)
    if not block:
        err_msg = f"No match for radio question '{question_text}'"
        raise ValueError(err_msg)

    for el in block.locator("*").all():
        try:
            text = el.inner_text(timeout=500)
            if _normalize(text) == answer_text:
                el.click(force=True)
                return
        except Exception:
            continue

    err_msg = f"No match for radio answer '{answer_text}' in question '{question_text}'"
    raise ValueError(err_msg)


def _fill_linear_scale_question(page: Page, question_data: dict):
    question_text = _normalize(question_data["question"])
    answer_value = _normalize(question_data["answer"])

    block = _find_matching_question_block(page, question_text)
    if not block:
        err_msg = f"No match for linear_scale question '{question_text}'"
        raise ValueError(err_msg)

    radio_els = block.locator('[role="radio"]').all()

    for radio in radio_els:
        try:
            value = radio.get_attribute("data-value") or radio.get_attribute("aria-label") or ""
            if _normalize(value) == answer_value:
                radio.click(force=True)
                return
        except Exception:
            continue

    err_msg = f"Could not find scale option '{answer_value}' in linear_scale question '{question_text}'"
    raise ValueError(err_msg)


def _fill_text_question(page: Page, question_data: dict):
    question_text = _normalize(question_data["question"])
    answer_text = _normalize(question_data["answer"])

    block = _find_matching_question_block(page, question_text)
    if not block:
        err_msg = f"No match for text question '{question_text}'"
        raise ValueError(err_msg)

    input_el = block.locator("input, textarea").first
    input_el.fill(answer_text)


def _fill_checkbox_question(page: Page, question_data: dict):
    question_text = _normalize(question_data["question"])
    answers = question_data["answer"]

    if not isinstance(answers, list):
        answers = str_to_parsed_type(answers, list)

    block = _find_matching_question_block(page, question_text)
    if not block:
        err_msg = f"No match for checkbox question '{question_text}'"
        raise ValueError(err_msg)

    for expected in answers:
        normalized_expected = _normalize(expected)
        for el in block.locator("*").all():
            try:
                text = el.inner_text(timeout=500)
                if _normalize(text) == normalized_expected:
                    el.click(force=True)
                    break
            except Exception:
                continue


def _fill_scale_matrix_question(page: Page, question_data: dict):
    question_text = _normalize(question_data["question"])
    answers = question_data["answer"]  # {"row": "value"}

    if not isinstance(answers, dict):
        answers = str_to_parsed_type(answers, dict)

    block = _find_matching_question_block(page, question_text)
    if not block:
        err_msg = f"No match for scale_matrix question '{question_text}'"
        raise ValueError(err_msg)

    radio_els = block.locator('[role="radio"]').all()

    for radio in radio_els:
        try:
            label = radio.get_attribute("aria-label") or ""
            norm_label = _normalize(label)

            for row_label, expected_value in answers.items():
                row_norm = _normalize(row_label)
                value_norm = _normalize(expected_value)

                if row_norm in norm_label and value_norm in norm_label:
                    radio.click(force=True)
                    break
        except Exception:
            continue


def _fill_multiple_choice_question(page: Page, question_data: dict):
    # Reuse the radio logic
    _fill_radio_question(page, question_data)


def fill_question(page: Page, question_data: dict):
    """Dispatche the appropriate form-filling function based on question type.

    This function receives parsed question data and determines which specific
    handler should be called to interact with the form UI using Playwright.
    Supported types include: radio, checkbox, multiple_choice, text,
    scale_matrix, and linear_scale.

    Parameters
    ----------
    page : Page
        A Playwright Page object representing the currently loaded form.

    question_data : dict
        A dictionary containing structured data about the form question.
        It must include a 'type' key (e.g., 'radio', 'text', etc.) and other
        relevant fields depending on the type.

    Raises
    ------
    NotImplementedError
        If the question type is not supported.
    ValueError
        If any of the underlying field-filling functions fail to locate
        or interact with the expected form elements.

    """
    qtype = question_data["type"]
    if qtype == "radio":
        _fill_radio_question(page, question_data)
    elif qtype == "checkbox":
        _fill_checkbox_question(page, question_data)
    elif qtype == "multiple_choice":
        _fill_multiple_choice_question(page, question_data)
    elif qtype == "text":
        _fill_text_question(page, question_data)
    elif qtype == "scale_matrix":
        _fill_scale_matrix_question(page, question_data)
    elif qtype == "linear_scale":
        _fill_linear_scale_question(page, question_data)
    else:
        raise NotImplementedError(f"Unsupported question type: {qtype}")


def submit_form(page: Page):
    """Submit a form by clicking the submit button on the given page.

    The function locates the submit button using the `aria-label="Submit"` attribute
    and triggers a click event to submit the form.

    Parameters
    ----------
    page : Page
        The page object representing the current browser page or context.

    """
    submit_button = page.locator('[aria-label="Submit"]')
    submit_button.click()
