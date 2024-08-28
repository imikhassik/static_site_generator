from unittest import TestCase

from src.actions.convert import markdown_to_html_node


class TestConvert(TestCase):
    def test_convert_heading_and_paragraph(self):
        markdown = """# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it."""

        html = """<div><h1>This is a heading</h1>\
<p>This is a paragraph of text. It has some <b>bold</b> and <i>italic</i> words inside of it.</p></div>"""

        result = markdown_to_html_node(markdown).to_html()

        self.assertEqual(result, html)

    def test_convert_paragraph_and_unordered_list(self):
        markdown = """This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the **first** list item in a list block
* This is a list `item`
* This is *another* list item"""

        html = """<div><p>This is a paragraph of text. It has some <b>bold</b> and <i>italic</i> words inside of it.</p>\
<ul><li>This is the <b>first</b> list item in a list block</li>\
<li>This is a list <code>item</code></li>\
<li>This is <i>another</i> list item</li></ul></div>"""

        result = markdown_to_html_node(markdown).to_html()

        self.assertEqual(result, html)

    def test_convert_heading_and_ordered_list(self):
        markdown = """## Another heading

1. This is the first ordered item in a list block
2. This is another ordered list item
3. This is one more ordered list item"""

        html = """<div><h2>Another heading</h2>\
<ol><li>This is the first ordered item in a list block</li>\
<li>This is another ordered list item</li>\
<li>This is one more ordered list item</li></ol></div>"""

        result = markdown_to_html_node(markdown).to_html()

        self.assertEqual(result, html)

    def test_convert_ordered_list_and_code(self):
        markdown = """1. This is the first ordered item in a list block
2. This is another ordered list item
3. This is one more ordered list item

```this is code block```"""

        html = """<div><ol><li>This is the first ordered item in a list block</li>\
<li>This is another ordered list item</li>\
<li>This is one more ordered list item</li></ol>\
<code>this is code block</code></div>"""

        result = markdown_to_html_node(markdown).to_html()

        self.assertEqual(result, html)

    def test_convert_heading_and_quote(self):
        markdown = """###### Heading of size 6

> quote line 1
> quote line 2"""

        html = """<div><h6>Heading of size 6</h6>\
<blockquote>quote line 1
quote line 2</blockquote></div>"""

        result = markdown_to_html_node(markdown).to_html()

        self.assertEqual(result, html)

    def test_paragraphs_with_links(self):
        markdown = """This is a paragraph with a [link](https://www.google.com) in it.

Another paragraph"""

        html = """<div><p>This is a paragraph with a <a href="https://www.google.com">link</a> in it.</p>\
<p>Another paragraph</p></div>"""

        result = markdown_to_html_node(markdown).to_html()

        self.assertEqual(result, html)

    def test_paragraphs_with_images(self):
        markdown = """This is a paragraph with a ![Description of image](url/of/image.jpg) in it.

Another paragraph"""

        html = """<div><p>This is a paragraph with a <img src="url/of/image.jpg" alt="Description of image"> in it.</p>\
<p>Another paragraph</p></div>"""

        result = markdown_to_html_node(markdown).to_html()

        self.assertEqual(result, html)

    def test_combined_markdown_to_html(self):
        markdown = """# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the **first** list item in a list block
* This is a list `item`
* This is *another* list item

## Another heading

1. This is the first ordered item in a list block
2. This is another ordered list item
3. This is one more ordered list item

```this is code block```

###### Heading of size 6

> quote line 1
> quote line 2

This is a paragraph with a [link](https://www.google.com) in it.

Another paragraph

This is a paragraph with a ![Description of image](url/of/image.jpg) in it.

Another paragraph"""

        html = """<div><h1>This is a heading</h1>\
<p>This is a paragraph of text. It has some <b>bold</b> and <i>italic</i> words inside of it.</p>\
<ul><li>This is the <b>first</b> list item in a list block</li>\
<li>This is a list <code>item</code></li>\
<li>This is <i>another</i> list item</li></ul>\
<h2>Another heading</h2>\
<ol><li>This is the first ordered item in a list block</li>\
<li>This is another ordered list item</li>\
<li>This is one more ordered list item</li></ol>\
<code>this is code block</code>\
<h6>Heading of size 6</h6>\
<blockquote>quote line 1
quote line 2</blockquote>\
<p>This is a paragraph with a <a href="https://www.google.com">link</a> in it.</p>\
<p>Another paragraph</p>\
<p>This is a paragraph with a <img src="url/of/image.jpg" alt="Description of image"> in it.</p>\
<p>Another paragraph</p></div>"""

        result = markdown_to_html_node(markdown).to_html()

        self.assertEqual(result, html)
        