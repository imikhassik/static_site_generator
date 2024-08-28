import src.utils as utils

from src.actions.split import markdown_to_blocks, block_to_block_type, text_to_textnodes
from src.nodes.htmlnode import ParentNode
from src.nodes.textnode import text_node_to_html_node


def get_header_hash_count(header):
    hash_count= 0
    i = 0
    while header[i] == '#':
        hash_count += 1
        i += 1
    return hash_count


def create_block_node(block, block_type):
    match block_type:
        case utils.block_type_paragraph:
            return ParentNode('p')
        case utils.block_type_heading:
            return ParentNode(f'h{get_header_hash_count(block)}')
        case utils.block_type_unordered_list:
            return ParentNode('ul')
        case utils.block_type_ordered_list:
            return ParentNode('ol')
        case utils.block_type_code:
            return ParentNode('code')
        case utils.block_type_quote:
            return ParentNode('blockquote')


def get_list_nodes(block):
    list_nodes = []
    list_items = block.split('\n')

    for item in list_items:
        list_node = ParentNode('li')
        list_node.children = get_children(item.split(' ', 1)[1], utils.block_type_paragraph)
        list_nodes.append(list_node)

    return list_nodes


def get_quote_nodes(block):
    quote_paragraphs = block.split('\n')

    for i in range(len(quote_paragraphs)):
        quote_paragraphs[i] = quote_paragraphs[i][2:]

    quote = '\n'.join(quote_paragraphs)

    return get_children(quote, utils.block_type_paragraph)


def get_html_nodes(text_nodes):
    html_nodes = []
    for node in text_nodes:
        html_nodes.append(text_node_to_html_node(node))
    return html_nodes


def get_children(block, block_type):
    match block_type:
        case utils.block_type_paragraph:
            text_nodes = text_to_textnodes(block)
            return get_html_nodes(text_nodes)
        case utils.block_type_heading:
            text_nodes = text_to_textnodes(block[get_header_hash_count(block) + 1:])
            return get_html_nodes(text_nodes)
        case utils.block_type_unordered_list:
            list_nodes = get_list_nodes(block)
            return list_nodes
        case utils.block_type_ordered_list:
            list_nodes = get_list_nodes(block)
            return list_nodes
        case utils.block_type_code:
            text_nodes = text_to_textnodes(block[3:len(block) - 3])
            return get_html_nodes(text_nodes)
        case utils.block_type_quote:
            quote_nodes = get_quote_nodes(block)
            return quote_nodes


def markdown_blocks_to_html_children(blocks):
    children = []

    for block in blocks:
        block_type = block_to_block_type(block)
        block_node = create_block_node(block, block_type)
        block_node.children = get_children(block, block_type)
        children.append(block_node)

    return children


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    parent_html_node = ParentNode('div')
    parent_html_node.children = markdown_blocks_to_html_children(blocks)      

    return parent_html_node

