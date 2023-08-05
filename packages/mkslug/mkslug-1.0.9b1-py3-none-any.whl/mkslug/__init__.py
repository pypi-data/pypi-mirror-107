import re


def generate(sentence: str) -> str:
    """
    Generate a slug from a sentence.

    Args:
        sentence: The sentence to check.

    Returns:
        generated slug value.
    """

    if not sentence:
        return "The sentence must be populated. Please try again."

    # Weed out unsavoury characters in the sentence
    pattern = "[^a-zA-Z0-9\s-]"
    sentence = re.sub(pattern, "", sentence)

    slug = sentence.strip()
    slug = slug.lower()
    slug = slug.replace(" ", "-")

    return f"The generated slug is:\n{slug}"
