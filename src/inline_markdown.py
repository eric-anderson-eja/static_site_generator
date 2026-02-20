import re
from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        # If it's not a text node, we don't touch it
        if old_node.text_type != TextType.TEXT_PLAIN:
            new_nodes.append(old_node)
            continue
            
        split_nodes = []
        sections = old_node.text.split(delimiter)
        
        # If the length is even, it means a delimiter wasn't closed
        # e.g., "text *bold" splits into ["text ", "bold"] (length 2)
        if len(sections) % 2 == 0:
            raise ValueError(f"Invalid Markdown syntax: no closing delimiter '{delimiter}' found.")
            
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT_PLAIN))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
        
    return new_nodes




def extract_markdown_images(text):
    # Pattern: ![alt text](url)
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(pattern, text)

def extract_markdown_links(text):
    # Pattern: [anchor text](url) 
    # The (?<!!) is a "negative lookbehind" - it ensures there is NO '!' before the '['
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(pattern, text)


def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT_PLAIN:
            new_nodes.append(old_node)
            continue
        
        original_text = old_node.text
        images = extract_markdown_images(original_text)
        
        if len(images) == 0:
            new_nodes.append(old_node)
            continue
        
        for image_alt, image_link in images:
            sections = original_text.split(f"![{image_alt}]({image_link})", 1)
            if len(sections) != 2:
                raise ValueError("Invalid markdown, image section not closed")
            
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT_PLAIN))
            
            new_nodes.append(TextNode(image_alt, TextType.IMAGE_TEXT, image_link))
            original_text = sections[1]
            
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT_PLAIN))
            
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT_PLAIN:
            new_nodes.append(old_node)
            continue
            
        original_text = old_node.text
        links = extract_markdown_links(original_text)
        
        if len(links) == 0:
            new_nodes.append(old_node)
            continue
            
        for link_text, link_url in links:
            sections = original_text.split(f"[{link_text}]({link_url})", 1)
            if len(sections) != 2:
                raise ValueError("Invalid markdown, link section not closed")
            
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT_PLAIN))
            
            new_nodes.append(TextNode(link_text, TextType.LINK_TEXT, link_url))
            original_text = sections[1]
            
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT_PLAIN))
            
    return new_nodes