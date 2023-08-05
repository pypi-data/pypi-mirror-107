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
    sentence = re.sub("[^a-zA-Z0-9\s-]", "", sentence)

    # Change from one or more spaces to one hyphen
    slug = "-".join(sentence.split())

    slug = slug.lower()

    return f"The generated slug is:\n{slug}"
