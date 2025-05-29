import json
import re


def str_to_json(text: str, strip_tags: list[str] | None = None) -> dict | list | None:
    """Clean specified XML-style tags from the input string and attempt to parse the remaining JSON content.

    Parameters
    ----------
    text : str
        Raw string that may contain JSON and unwanted tag blocks.

    strip_tags : list of str, optional
        A list of tag names to strip from the input. Tags should be without angle brackets,
        e.g., ['thinking', 'processing'].

    Returns
    -------
    dict or list or None
        Parsed JSON object or array if found and valid, otherwise None.

    """
    cleaned_text = text

    # Remove all specified tags and their content
    if strip_tags:
        for tag in strip_tags:
            cleaned_text = re.sub(rf"<{tag}.*?>.*?</{tag}>", "", cleaned_text, flags=re.DOTALL | re.IGNORECASE)

    # Extract first JSON-looking structure (object or array)
    match = re.search(r"(\{.*\}|\[.*\])", cleaned_text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(1))
        except json.JSONDecodeError:
            return None
    return None
