from enum import Enum
from htmlnode import HTMLNode, ParentNode
from inline_markdown import text_to_textnodes
from textnode import TextNode, text_node_to_html_node, TextType


def markdown_to_blocks(markdown):
    # Split the document by double newlines
    raw_blocks = markdown.split("\n\n")
    filtered_blocks = []
    
    for block in raw_blocks:
        # Strip leading/trailing whitespace
        cleaned_block = block.strip()
        
        # Only add to list if the block isn't empty
        if cleaned_block != "":
            filtered_blocks.append(cleaned_block)
            
    return filtered_blocks

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING   = "heading"
    CODE      = "code"
    QUOTE     = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_block_type(markdown_block):
    #Quote list check
    lines = markdown_block.split("\n")
    all_match_quote = True
    for line in lines:
        if not line.startswith(">"):
            all_match_quote= False
            break

    #Unordered List Check
    all_match_unordered = True
    for line in lines:
        if not line.startswith("- "):
            all_match_unordered = False
            break
    
    #Ordered list check
    all_match_ordered = True
    i = 1
    for line in lines:
        if not line.startswith(f"{i}. "):
            all_match_ordered = False
            break
        i += 1

    if markdown_block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    elif markdown_block.startswith("```\n") and markdown_block.endswith("```"):
        return BlockType.CODE  
    elif all_match_quote:
        return BlockType.QUOTE
    elif all_match_unordered:
        return BlockType.UNORDERED_LIST
    elif all_match_ordered:
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH

#converts markdown doc into htmlnode
def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    block_nodes = []

    for block in blocks:
        block_type = block_to_block_type(block)

        if block_type == BlockType.HEADING:
            node = create_heading_node(block)
        elif block_type == BlockType.CODE:
            node = create_code_node(block)
        elif block_type == BlockType.QUOTE:
            node = create_quote_node(block)
        elif block_type == BlockType.UNORDERED_LIST:
            node = create_ul_node(block)
        elif block_type == BlockType.ORDERED_LIST:
            node = create_ol_node(block)
        else: # paragraph
            node = create_paragraph_node(block)

        block_nodes.append(node)

    #wrap all blocks in a single parent div
    return ParentNode("div", block_nodes)


#helper functions
def create_heading_node(block):
    level = 0
    for char in block:
        if char == '#':
            level += 1
        else:
            break
    text = block[level + 1:].strip()
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)

def create_code_node(block):
    text = block.strip("`").strip()
    content_node = text_node_to_html_node(TextNode(text, TextType.TEXT_PLAIN))
    code_node = ParentNode("code", [content_node])
    return ParentNode("pre", [code_node])

def create_quote_node(block):
    lines = block.split("\n")
    cleaned_lines = [line.lstrip(">").strip() for line in lines]
    content = " ".join(cleaned_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)

def create_ul_node(block):
    items = block.split("\n")
    li_nodes = []
    for item in items:
        text = item[2:].strip()
        li_nodes.append(ParentNode("li", text_to_children(text)))
    return ParentNode("ul", li_nodes)

def create_ol_node(block):
    items = block.split("\n")
    li_nodes = []
    for item in items:
        text = item[item.find(" ") + 1:].strip()
        li_nodes.append(ParentNode("li", text_to_children(text)))
    return ParentNode("ol", li_nodes)

def create_paragraph_node(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)

def text_to_children(text):
    # 1. Convert the raw string into a list of TextNodes 
    # (Handling bold, italic, code, etc.)
    text_nodes = text_to_textnodes(text)
    
    # 2. Convert each TextNode into an HTMLNode (LeafNode)
    html_nodes = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        html_nodes.append(html_node)
        
    return html_nodes