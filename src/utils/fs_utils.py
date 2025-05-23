import shutil
from pathlib import Path


def reset_screenshot_dir(path: str = "screenshots"):
    """Delete the screenshot directory if it exists and recreates it.

    Parameters
    ----------
    path : str
        Path to the directory to reset. Defaults to "screenshots".

    """
    dir_path = Path(path)

    if dir_path.exists() and dir_path.is_dir():
        shutil.rmtree(dir_path)

    dir_path.mkdir(parents=True, exist_ok=True)
