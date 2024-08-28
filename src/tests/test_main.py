from unittest import TestCase

from src.main import extract_title


class TestExtractTitle(TestCase):
    def test_positive(self):
        markdown = "# Hello"

        self.assertEqual(extract_title(markdown), 'Hello')

    def test_negative(self):
        markdown = """
        * item 1
        * item 2"""

        self.assertRaisesRegex(
            Exception,
            "No h1 header in markdown file.",
            extract_title,
            markdown
        )
