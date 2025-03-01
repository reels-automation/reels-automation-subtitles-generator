import unicodedata
import re

def sanitize_attribute(attribute: str):
    """Sanitiza un input para que no contenga caracteres que no puedan ser parseados

    Args:
        attribute (str):

    Returns:
        (str):
    """
    if attribute is not None:
        result = (
            unicodedata.normalize("NFKD", attribute)
            .encode("ASCII", "ignore")
            .decode("ASCII")
        )
        # Modify the regex to exclude dots
        result = re.sub(r"[^a-zA-Z0-9._-]", " ", result)
        result = result.strip()
        return result
    return None
