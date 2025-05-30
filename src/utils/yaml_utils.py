import yaml

from src.config.project_paths import PROMPTS_DIRECTORY


def load_prompts(language: str) -> dict:
    """Load prompt definitions from a YAML file for a given language.

    The function looks for a YAML file named with the first two characters
    of the provided language code (e.g., "en.yaml" for "English"). It then
    loads and returns the prompts as a dictionary.

    Parameters
    ----------
    language : str
        The language identifier (e.g., "English", "en-US", "de", etc.).
        Only the first two lowercase characters are used to locate the corresponding file.

    Returns
    -------
    dict
        Dictionary containing the loaded prompt definitions.

    Raises
    ------
    ValueError
        If no YAML file is found for the given language.

    """
    lang_code = language.lower()[:2]  # 'en'
    path = PROMPTS_DIRECTORY / f"{lang_code}.yaml"

    if not path.exists():
        msg = f"No prompt file found for language: {language}"
        raise ValueError(msg)

    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)
