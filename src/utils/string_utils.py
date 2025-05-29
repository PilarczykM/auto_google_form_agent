import ast
import re
from collections.abc import Callable
from typing import Any


def sanitize_filename(text: str, max_length: int = 50) -> str:
    """Sanitizes a string to make it safe for use as a filename.

    Normalizes whitespace, removes special characters,
    replaces spaces with underscores, and truncates the result
    to a maximum length if needed.

    Parameters
    ----------
    text : str
        The input string to sanitize.
    max_length : int, optional
        The maximum length of the resulting filename (default is 50).

    Returns
    -------
    str
        A sanitized string that is safe to use as a filename.

    """
    text = re.sub(r"\s+", " ", text).strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = text.replace(" ", "_")
    return text[:max_length]


def str_to_parsed_type(value: str, expected_type: type, item_validator: Callable[[Any], bool] | None = None) -> Any:
    """Parse a string using literal_eval and ensures it matches the expected type.

    Optionally validates items inside if the type is iterable.

    Parameters
    ----------
    value : str
        The string to parse.
    expected_type : type
        The expected top-level type (e.g., list, dict).
    item_validator : Callable, optional
        A function to validate each item (e.g., lambda x: isinstance(x, str)).

    Returns
    -------
    T
        Parsed and validated object of the expected type.

    Raises
    ------
    TypeError
        If parsing fails or types don't match.

    """
    if not isinstance(value, str):
        err_msg = "Expected a string as input."
        raise TypeError(err_msg)

    try:
        parsed = ast.literal_eval(value)
    except (ValueError, SyntaxError) as err:
        err_msg = "Input is not a valid Python literal."
        raise TypeError(err_msg) from err

    if not isinstance(parsed, expected_type):
        err_msg = f"Parsed value is not of type {expected_type.__name__}."
        raise TypeError(err_msg)

    if item_validator and isinstance(parsed, list | tuple | set | dict):
        if isinstance(parsed, dict):
            if not all(item_validator(k) and item_validator(v) for k, v in parsed.items()):
                err_msg = "One or more items in dict failed validation."
                raise TypeError(err_msg)
        elif not all(item_validator(item) for item in parsed):
            err_msg = f"One or more items in {expected_type.__name__} failed validation."
            raise TypeError(err_msg)

    return parsed
