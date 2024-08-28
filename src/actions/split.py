import src.utils as utils

from src.nodes.textnode import TextNode
from src.actions.extract_links import extract_markdown_links, extract_markdown_images


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    if delimiter != utils.delimiters.get(text_type):
        raise Exception("Invalid Markdown syntax")

    new_nodes = []
    
    for node in old_nodes:
        if node.text_type == utils.text_type_text:
            node_text = node.text.split(delimiter)

            for i in range(len(node_text)):
                if i % 2 and node_text[i]:
                    new_nodes.append(TextNode(node_text[i], text_type))
                elif node_text[i]:
                    new_nodes.append(TextNode(node_text[i], utils.text_type_text))
        else:
            new_nodes.append(node)
    
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []

    for node in old_nodes:
        links = extract_markdown_links(node.text)
        if links:
            sections = [node.text]
            text_portions = []
            for anchor_text, url in links:
                sections = sections[-1].split(f'[{anchor_text}]({url})', 1)
                text_portions.append(sections[0])
                text_node = TextNode(text_portions[-1], utils.text_type_text)
                link_node = TextNode(anchor_text, utils.text_type_link, url)
                if text_node.text:
                    new_nodes.append(text_node)
                new_nodes.append(link_node)
            end_node = TextNode(sections[-1], utils.text_type_text)
            if end_node.text:
                new_nodes.append(end_node)
        else:
            new_nodes.append(node)

    return new_nodes


def split_nodes_image(old_nodes):
    new_nodes = []

    for node in old_nodes:
        images = extract_markdown_images(node.text)
        if images:
            sections = [node.text]
            text_portions = []
            for alt_text, url in images:
                sections = sections[-1].split(f'![{alt_text}]({url})', 1)
                text_portions.append(sections[0])
                text_node = TextNode(text_portions[-1], utils.text_type_text)
                image_node = TextNode(alt_text, utils.text_type_image, url)
                if text_node.text:
                    new_nodes.append(text_node)
                new_nodes.append(image_node)
            end_node = TextNode(sections[-1], utils.text_type_text)
            if end_node.text:
                new_nodes.append(end_node)
        else:
            new_nodes.append(node)

    return new_nodes


def text_to_textnodes(text):
    node = TextNode(text, utils.text_type_text)
    bold_nodes = split_nodes_delimiter([node], '**', utils.text_type_bold)
    italic_nodes = split_nodes_delimiter(bold_nodes, '*', utils.text_type_italic)
    code_nodes = split_nodes_delimiter(italic_nodes, '`', utils.text_type_code)
    image_nodes = split_nodes_image(code_nodes)
    link_nodes = split_nodes_link(image_nodes)
    return link_nodes


def markdown_to_blocks(markdown):
    split_markdown = markdown.split('\n\n')
    result = []
    for block in split_markdown:
        if block.strip():
            result.append(block.strip())
    return result


def block_to_block_type(block):
    if block[0] == '#':
        i = 1
        while block[i] != ' ' and i < 6:
            i += 1
        
        if block[i] == ' ' and block[i - 1] == '#':
            return utils.block_type_heading
        return utils.block_type_paragraph
    elif block[:3] == "```" and block[len(block) - 3: len(block)] == "```":
        return utils.block_type_code
    elif block[0] == '>':
        split_block = block.split('\n')
        for i in range(len(split_block)):
            if split_block[i][0] != '>':
                return utils.block_type_paragraph
        return utils.block_type_quote
    elif block[:2] == '* ' or block[:2] == '- ':
        split_block = block.split('\n')
        for i in range(len(split_block)):
            if split_block[i][:2] != '* ' and split_block[i][:2] != '- ':
                return utils.block_type_paragraph
        return utils.block_type_unordered_list
    elif block[0].isnumeric():
        if block[:3] != "1. ":
            return utils.block_type_paragraph

        split_block = block.split('\n')
        for i in range(len(split_block)):
            line_number = 0
            j = 0
            while split_block[i][j].isnumeric():
                j += 1
            if j < len(split_block[i]) - 1 and split_block[i][j: j + 2] == '. ':
                line_number = int(split_block[i][:j])
            if line_number != i + 1:
                return utils.block_type_paragraph
        return utils.block_type_ordered_list
    else:
        return utils.block_type_paragraph
        
