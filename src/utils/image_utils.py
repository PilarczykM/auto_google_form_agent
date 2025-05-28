import base64


def encode_image_to_base64(image_path: str) -> str:
    """Encode an image file to a base64 string.

    Parameters
    ----------
    image_path : str
        Path to the image file (e.g., PNG or JPG).

    Returns
    -------
    str
        Base64-encoded string of the image content (suitable for embedding).

    """
    with open(image_path, "rb") as image_file:
        encoded_bytes = base64.b64encode(image_file.read())
        return encoded_bytes.decode("utf-8")
