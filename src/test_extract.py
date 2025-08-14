import unittest
from extract import extract_markdown_images, extract_markdown_links


class TestExtractMarkdown(unittest.TestCase):
    def test_extract_markdown_images_single(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual(
            [("image", "https://i.imgur.com/zjjcJKZ.png")],
            matches
        )

    def test_extract_markdown_images_multiple(self):
        text = "![one](url1) and ![two](url2)"
        matches = extract_markdown_images(text)
        self.assertListEqual([("one", "url1"), ("two", "url2")], matches)

    def test_extract_markdown_links_single(self):
        matches = extract_markdown_links(
            "This is a [link](https://example.com)"
        )
        self.assertListEqual(
            [("link", "https://example.com")],
            matches
        )

    def test_extract_markdown_links_multiple(self):
        text = "[one](url1) and [two](url2)"
        matches = extract_markdown_links(text)
        self.assertListEqual([("one", "url1"), ("two", "url2")], matches)

    def test_links_do_not_match_images(self):
        text = "![image](url1) and [link](url2)"
        matches = extract_markdown_links(text)
        self.assertListEqual([("link", "url2")], matches)


if __name__ == "__main__":
    unittest.main()
