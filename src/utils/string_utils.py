import re


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
