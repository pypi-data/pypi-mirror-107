from src.mkslug import generate


class TestMakeSlug:
    def test_generate_regular_sentence(self):
        """
        Test generate function works successfully when a regular sentence provided.
        """

        slug = generate("Test SLUG vaLUEs 1")

        assert slug == "The generated slug is:\ntest-slug-values-1"

    def test_generate_outer_chars_are_blank(self):
        """
        Test generate function works successfully when the outer characters are blank provided.
        """

        slug = generate("    Test SLUG vaLUEs 2  ")

        assert slug == "The generated slug is:\ntest-slug-values-2"

    def test_generate_empty_sentence(self):
        """
        Test generate function works successfully when an empty sentence provided.
        """

        slug = generate("")

        assert slug == "The sentence must be populated. Please try again."

    def test_generate_special_characters_in_sentence(self):
        """
        Test generate function works successfully when a sentence provided has some special characters.
        """

        slug = generate("%Test slug ^*value$ 3.£$/")

        assert slug == "The generated slug is:\ntest-slug-value-3"
