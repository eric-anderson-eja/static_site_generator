from textnode import TextNode, TextType
import re

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