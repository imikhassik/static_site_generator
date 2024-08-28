import unittest
import src.utils as utils

from src.nodes.textnode import TextNode
from src.actions.split import split_nodes_delimiter, split_nodes_link, \
split_nodes_image, text_to_textnodes, markdown_to_blocks, block_to_block_type


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_single_node_code(self):
        node = TextNode("This is text with a `code block` word", utils.text_type_text)
        new_nodes = split_nodes_delimiter([node], "`", utils.text_type_code)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", utils.text_type_text),
                TextNode("code block", utils.text_type_code),
                TextNode(" word", utils.text_type_text),
            ]
        )

    def test_single_node_bold(self):
        node = TextNode("This is text with a **bolded phrase** in the middle", utils.text_type_text)
        new_nodes = split_nodes_delimiter([node], "**", utils.text_type_bold)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", utils.text_type_text),
                TextNode("bolded phrase", utils.text_type_bold),
                TextNode(" in the middle", utils.text_type_text),
            ]
        )

    def test_single_node_italic(self):
        node = TextNode("This is text with an *italic phrase* in the middle", utils.text_type_text)
        new_nodes = split_nodes_delimiter([node], "*", utils.text_type_italic)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with an ", utils.text_type_text),
                TextNode("italic phrase", utils.text_type_italic),
                TextNode(" in the middle", utils.text_type_text),
            ]
        )

    def test_single_node_multiple_code(self):
        node = TextNode(
            "This is text with a `first code block` word and a `second code block` word", 
            utils.text_type_text
        )
        new_nodes = split_nodes_delimiter([node], "`", utils.text_type_code)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", utils.text_type_text),
                TextNode("first code block", utils.text_type_code),
                TextNode(" word and a ", utils.text_type_text),
                TextNode("second code block", utils.text_type_code),
                TextNode(" word", utils.text_type_text),
            ]
        )

    def test_single_node_multiple_code_no_last_text(self):
        node = TextNode(
            "This is text with a `first code block` word and a `second code block`", 
            utils.text_type_text
        )
        new_nodes = split_nodes_delimiter([node], "`", utils.text_type_code)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", utils.text_type_text),
                TextNode("first code block", utils.text_type_code),
                TextNode(" word and a ", utils.text_type_text),
                TextNode("second code block", utils.text_type_code)
            ]
        )

    def test_single_node_multiple_code_no_first_text(self):
        node = TextNode(
            "`First code block` word and `second code block` word", 
            utils.text_type_text
        )
        new_nodes = split_nodes_delimiter([node], "`", utils.text_type_code)
        self.assertEqual(
            new_nodes,
            [
                TextNode("First code block", utils.text_type_code),
                TextNode(" word and ", utils.text_type_text),
                TextNode("second code block", utils.text_type_code),
                TextNode(" word", utils.text_type_text),
            ]
        )

    
    def test_single_node_multiple_code_no_first_no_last_text(self):
        node = TextNode(
            "`First code block` word and `second code block`", 
            utils.text_type_text
        )
        new_nodes = split_nodes_delimiter([node], "`", utils.text_type_code)
        self.assertEqual(
            new_nodes,
            [
                TextNode("First code block", utils.text_type_code),
                TextNode(" word and ", utils.text_type_text),
                TextNode("second code block", utils.text_type_code)
            ]
        )

    def test_multiple_nodes_code(self):
        node1 = TextNode("This is text with a `code block` word", utils.text_type_text)
        node2 = TextNode("This is another text with a `code block` word", utils.text_type_text)
        new_nodes = split_nodes_delimiter([node1, node2], "`", utils.text_type_code)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", utils.text_type_text),
                TextNode("code block", utils.text_type_code),
                TextNode(" word", utils.text_type_text),
                TextNode("This is another text with a ", utils.text_type_text),
                TextNode("code block", utils.text_type_code),
                TextNode(" word", utils.text_type_text),
            ]
        )

    def test_not_text_type(self):
        node = TextNode("**Bold text**", utils.text_type_bold)
        new_nodes = split_nodes_delimiter([node], "**", utils.text_type_bold)
        self.assertEqual(
            new_nodes,
            [
                TextNode("**Bold text**", utils.text_type_bold)
            ]
        )

    def test_multiple_delimiters(self):
        node = TextNode("This is *text* with a `code block` word", utils.text_type_text)
        new_nodes = split_nodes_delimiter([node], '*', utils.text_type_italic)
        new_nodes = split_nodes_delimiter(new_nodes, '`', utils.text_type_code)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is ", utils.text_type_text),
                TextNode("text", utils.text_type_italic),
                TextNode(" with a ", utils.text_type_text),
                TextNode("code block", utils.text_type_code),
                TextNode(" word", utils.text_type_text),
            ]
        )

    
    def test_multiple_delimiters_no_text_between(self):
        node = TextNode("This is *text with a *`code block` word", utils.text_type_text)
        new_nodes = split_nodes_delimiter([node], '*', utils.text_type_italic)
        new_nodes = split_nodes_delimiter(new_nodes, '`', utils.text_type_code)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is ", utils.text_type_text),
                TextNode("text with a ", utils.text_type_italic),
                TextNode("code block", utils.text_type_code),
                TextNode(" word", utils.text_type_text),
            ]
        )

    def test_invalid_markdown_syntax(self):
        node = TextNode("This is text with a `code block` word", utils.text_type_text)
        self.assertRaisesRegex(
            Exception,
            "Invalid Markdown syntax",
            split_nodes_delimiter,
            node,
            "'",
            utils.text_type_code
        )


class TestSplitNodesLink(unittest.TestCase):
    def test_single_node_single_link(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev)",
            utils.text_type_text
        )
        new_nodes = split_nodes_link([node])
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a link ", utils.text_type_text),
                TextNode("to boot dev", utils.text_type_link, "https://www.boot.dev")
            ]
        )

    def test_single_node_multiple_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev) with end text",
            utils.text_type_text
        )
        new_nodes = split_nodes_link([node])
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a link ", utils.text_type_text),
                TextNode("to boot dev", utils.text_type_link, "https://www.boot.dev"),
                TextNode(" and ", utils.text_type_text),
                TextNode("to youtube", utils.text_type_link, "https://www.youtube.com/@bootdotdev"),
                TextNode(" with end text", utils.text_type_text)
            ]
        )

    def test_single_node_no_start_text(self):
        node = TextNode(
            "[to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            utils.text_type_text
        )
        new_nodes = split_nodes_link([node])
        self.assertEqual(
            new_nodes,
            [
                TextNode("to boot dev", utils.text_type_link, "https://www.boot.dev"),
                TextNode(" and ", utils.text_type_text),
                TextNode("to youtube", utils.text_type_link, "https://www.youtube.com/@bootdotdev")
            ]
        )

    def test_single_node_no_end_text(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            utils.text_type_text
        )
        new_nodes = split_nodes_link([node])
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a link ", utils.text_type_text),
                TextNode("to boot dev", utils.text_type_link, "https://www.boot.dev"),
                TextNode(" and ", utils.text_type_text),
                TextNode("to youtube", utils.text_type_link, "https://www.youtube.com/@bootdotdev")
            ]
        )

    def test_single_node_no_mid_text(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev)[to youtube](https://www.youtube.com/@bootdotdev)",
            utils.text_type_text
        )
        new_nodes = split_nodes_link([node])
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a link ", utils.text_type_text),
                TextNode("to boot dev", utils.text_type_link, "https://www.boot.dev"),
                TextNode("to youtube", utils.text_type_link, "https://www.youtube.com/@bootdotdev")
            ]
        )

    def test_multiple_nodes_multiple_links(self):
        node1 = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            utils.text_type_text
        )
        node2 = TextNode(
            "Another link [to boot dev](https://www.boot.dev) and [to yandex](https://www.yandex.ru)",
            utils.text_type_text
        )
        new_nodes = split_nodes_link([node1, node2])
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a link ", utils.text_type_text),
                TextNode("to boot dev", utils.text_type_link, "https://www.boot.dev"),
                TextNode(" and ", utils.text_type_text),
                TextNode("to youtube", utils.text_type_link, "https://www.youtube.com/@bootdotdev"),
                TextNode("Another link ", utils.text_type_text),
                TextNode("to boot dev", utils.text_type_link, "https://www.boot.dev"),
                TextNode(" and ", utils.text_type_text),
                TextNode("to yandex", utils.text_type_link, "https://www.yandex.ru"),
            ]
        )

    
class TestSplitNodesImage(unittest.TestCase):
    def test_single_node_single_image(self):
        node = TextNode(
            "This is text with an image of a ![cat](https://www.boot.dev/cat.png)",
            utils.text_type_text
        )
        new_nodes = split_nodes_image([node])
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with an image of a ", utils.text_type_text),
                TextNode("cat", utils.text_type_image, "https://www.boot.dev/cat.png")
            ]
        )
    
    def test_single_node_multiple_images(self):
        node = TextNode(
            "This is text with an image of a ![cat](https://www.boot.dev/cat.png) and a ![mouse](https://www.boot.dev/mouse.png) with end text",
            utils.text_type_text
        )
        new_nodes = split_nodes_image([node])
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with an image of a ", utils.text_type_text),
                TextNode("cat", utils.text_type_image, "https://www.boot.dev/cat.png"),
                TextNode(" and a ", utils.text_type_text),
                TextNode("mouse", utils.text_type_image, "https://www.boot.dev/mouse.png"),
                TextNode(" with end text", utils.text_type_text)
            ]
        )

    def test_single_node_no_start_text(self):
        node = TextNode(
            "![cat](https://www.boot.dev/cat.png) and ![mouse](https://www.boot.dev/mouse.png)",
            utils.text_type_text
        )
        new_nodes = split_nodes_image([node])
        self.assertEqual(
            new_nodes,
            [
                TextNode("cat", utils.text_type_image, "https://www.boot.dev/cat.png"),
                TextNode(" and ", utils.text_type_text),
                TextNode("mouse", utils.text_type_image, "https://www.boot.dev/mouse.png")
            ]
        )

    def test_single_node_no_end_text(self):
        node = TextNode(
            "This is text with an image of a ![cat](https://www.boot.dev/cat.png) and a ![mouse](https://www.boot.dev/mouse.png)",
            utils.text_type_text
        )
        new_nodes = split_nodes_image([node])
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with an image of a ", utils.text_type_text),
                TextNode("cat", utils.text_type_image, "https://www.boot.dev/cat.png"),
                TextNode(" and a ", utils.text_type_text),
                TextNode("mouse", utils.text_type_image, "https://www.boot.dev/mouse.png")
            ]
        )

    def test_single_node_no_mid_text(self):
        node = TextNode(
            "This is text with an image of a ![cat](https://www.boot.dev/cat.png)![mouse](https://www.boot.dev/mouse.png)",
            utils.text_type_text
        )
        new_nodes = split_nodes_image([node])
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with an image of a ", utils.text_type_text),
                TextNode("cat", utils.text_type_image, "https://www.boot.dev/cat.png"),
                TextNode("mouse", utils.text_type_image, "https://www.boot.dev/mouse.png")
            ]
        )

    def test_multiple_nodes_sigle_multiple_images(self):
        node1 = TextNode(
            "This is text with an image of a ![cat](https://www.boot.dev/cat.png) and a ![mouse](https://www.boot.dev/mouse.png)",
            utils.text_type_text
        )
        node2 = TextNode(
            "Another image of a ![cat](https://www.boot.dev/cat.png) and a ![dog](https://www.boot.dev/dog.png)",
            utils.text_type_text
        )
        new_nodes = split_nodes_image([node1, node2])
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with an image of a ", utils.text_type_text),
                TextNode("cat", utils.text_type_image, "https://www.boot.dev/cat.png"),
                TextNode(" and a ", utils.text_type_text),
                TextNode("mouse", utils.text_type_image, "https://www.boot.dev/mouse.png"),
                TextNode("Another image of a ", utils.text_type_text),
                TextNode("cat", utils.text_type_image, "https://www.boot.dev/cat.png"),
                TextNode(" and a ", utils.text_type_text),
                TextNode("dog", utils.text_type_image, "https://www.boot.dev/dog.png")
            ]
        )


class TestTextToTextnodes(unittest.TestCase):
    def test_all_splits_in_order(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        self.assertEqual(
            nodes,
            [
                TextNode("This is ", utils.text_type_text),
                TextNode("text", utils.text_type_bold),
                TextNode(" with an ", utils.text_type_text),
                TextNode("italic", utils.text_type_italic),
                TextNode(" word and a ", utils.text_type_text),
                TextNode("code block", utils.text_type_code),
                TextNode(" and an ", utils.text_type_text),
                TextNode("obi wan image", utils.text_type_image, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", utils.text_type_text),
                TextNode("link", utils.text_type_link, "https://boot.dev"),
            ]
        )
    
    def test_all_splits_out_of_order(self):
        text = "[Here's a link](https://boot.dev) *italics text*`code` some ![image](https://boot.dev/image.png) and **bold text** to finish."
        nodes = text_to_textnodes(text)
        self.assertEqual(
            nodes,
            [
                TextNode("Here's a link", utils.text_type_link, "https://boot.dev"),
                TextNode(" ", utils.text_type_text),
                TextNode("italics text", utils.text_type_italic),
                TextNode("code", utils.text_type_code),
                TextNode(" some ", utils.text_type_text),
                TextNode("image", utils.text_type_image, "https://boot.dev/image.png"),
                TextNode(" and ", utils.text_type_text),
                TextNode("bold text", utils.text_type_bold),
                TextNode(" to finish.", utils.text_type_text)
            ]
        )

    def test_multiple_images_and_links(self):
        text = "One ![image1](https://example.com/image1.png), two [link](https://boot.dev/link1), **three** ![image2](https://example.com/image2.png), `four` [link2](https://boot.dev/link2)"
        nodes = text_to_textnodes(text)
        self.assertEqual(
            nodes,
            [
                TextNode("One ", utils.text_type_text),
                TextNode("image1", utils.text_type_image, "https://example.com/image1.png"),
                TextNode(", two ", utils.text_type_text),
                TextNode("link", utils.text_type_link, "https://boot.dev/link1"),
                TextNode(", ", utils.text_type_text),
                TextNode("three", utils.text_type_bold),
                TextNode(" ", utils.text_type_text),
                TextNode("image2", utils.text_type_image, "https://example.com/image2.png"),
                TextNode(", ", utils.text_type_text),
                TextNode("four", utils.text_type_code),
                TextNode(" ", utils.text_type_text),
                TextNode("link2", utils.text_type_link, "https://boot.dev/link2")
            ]
        )


class TestMarkdownToBlocks(unittest.TestCase):
    def test_general_case(self):
        markdown = """# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item"""
        expected_result = [
            '# This is a heading', 
            'This is a paragraph of text. It has some **bold** and *italic* words inside of it.',
            '* This is the first list item in a list block\n* This is a list item\n* This is another list item'
            ]
    
        self.assertEqual(markdown_to_blocks(markdown), expected_result)

    def test_excessive_newlines(self):
        markdown = """# This is a heading



This is a paragraph of text. It has some **bold** and *italic* words inside of it.


* This is the first list item in a list block
* This is a list item
* This is another list item"""
        expected_result = [
            '# This is a heading', 
            'This is a paragraph of text. It has some **bold** and *italic* words inside of it.',
            '* This is the first list item in a list block\n* This is a list item\n* This is another list item'
            ]
    
        self.assertEqual(markdown_to_blocks(markdown), expected_result)
    
    def test_leading_and_trailing_whitespace(self):
        markdown = """# This is a heading   

    This is a paragraph of text. It has some **bold** and *italic* words inside of it.


 * This is the first list item in a list block
* This is a list item
* This is another list item """
        expected_result = [
            '# This is a heading', 
            'This is a paragraph of text. It has some **bold** and *italic* words inside of it.',
            '* This is the first list item in a list block\n* This is a list item\n* This is another list item'
            ]
    
        self.assertEqual(markdown_to_blocks(markdown), expected_result)
        

class TestBlockToBlockType(unittest.TestCase):
    def test_headings(self):
        block1 = "# heading"
        self.assertEqual(block_to_block_type(block1), utils.block_type_heading)
        
        block2 = "## heading"
        self.assertEqual(block_to_block_type(block2), utils.block_type_heading)

        block3 = "### heading"
        self.assertEqual(block_to_block_type(block3), utils.block_type_heading)

        block4 = "#### heading"
        self.assertEqual(block_to_block_type(block4), utils.block_type_heading)

        block5 = "##### heading"
        self.assertEqual(block_to_block_type(block5), utils.block_type_heading)

        block6 = "###### heading"
        self.assertEqual(block_to_block_type(block6), utils.block_type_heading)

        block7 = "####### heading"
        self.assertEqual(block_to_block_type(block7), utils.block_type_paragraph)

        block8 = "#####heading"
        self.assertEqual(block_to_block_type(block8), utils.block_type_paragraph)

    def test_code(self):
        block1 = "```code```"
        self.assertEqual(block_to_block_type(block1), utils.block_type_code)

        block2 = "``'code ```"
        self.assertEqual(block_to_block_type(block2), utils.block_type_paragraph)

        block3 = "``` code ```"
        self.assertEqual(block_to_block_type(block3), utils.block_type_code)
        
    def test_quote(self):
        block1 = """> quote1
>quote2
>quote3"""
        self.assertEqual(block_to_block_type(block1), utils.block_type_quote)

        block2 = """> quote1
>quote2
quote3"""
        self.assertEqual(block_to_block_type(block2), utils.block_type_paragraph)

    def test_unordered_list(self):
        block1 = """* item1
* item2
* item3"""
        self.assertEqual(block_to_block_type(block1), utils.block_type_unordered_list)

        block2 = """- item1
- item2
- item3"""
        self.assertEqual(block_to_block_type(block2), utils.block_type_unordered_list)

        block3 = """* item1
- item2
* item3"""
        self.assertEqual(block_to_block_type(block3), utils.block_type_unordered_list)

        block4 = """* item1
* item2
*item3"""
        self.assertEqual(block_to_block_type(block4), utils.block_type_paragraph)

        block5 = """* item1
% item2
* item3"""
        self.assertEqual(block_to_block_type(block5), utils.block_type_paragraph)

    def test_ordered_list(self):
        block1 = """1. item1
2. item2
3. item3"""
        self.assertEqual(block_to_block_type(block1), utils.block_type_ordered_list)

        block2 = """1. item1
2. item2
3. item3
4. item4
5. item5
6. item6
7. item7
8. item8
9. item9
10. item10
11. item11
12. item12"""
        self.assertEqual(block_to_block_type(block2), utils.block_type_ordered_list)

        block3 = """1. item1
2. item2
3. item3
4. item4
5. item5
6. item6
7. item7
8. item8
9. item9
10. item10
11.item11
12. item12"""
        self.assertEqual(block_to_block_type(block3), utils.block_type_paragraph)

        block4 = """1. item1
2. item2
3. item3
4. item4
5. item5
6. item6
7. item7
8. item8
9. item9
10. item10
11. item11
12. """
        self.assertEqual(block_to_block_type(block4), utils.block_type_ordered_list)

        block5 = """1. item1
2. item2
3. item3
4. item4
5. item5
6. item6
7. item7
8. item8
9. item9
10. item10
11. item11
12."""
        self.assertEqual(block_to_block_type(block5), utils.block_type_paragraph)

        block6 = """10. item1
11. item2
12. item3"""
        self.assertEqual(block_to_block_type(block6), utils.block_type_paragraph)

        block7 = """1. item1
1. item2
2. item3"""
        self.assertEqual(block_to_block_type(block7), utils.block_type_paragraph)

    def test_other(self):
        block = """~ item1
~ item2"""
        self.assertEqual(block_to_block_type(block), utils.block_type_paragraph)

