from enum import Enum


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

    # Heading check
    if markdown_block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    # Code check
    elif (markdown_block.startswith("```\n") and markdown_block.endswith("```")):
        return BlockType.CODE
    elif all_match_quote:
        return BlockType.QUOTE
    elif all_match_unordered:
        return BlockType.UNORDERED_LIST
    elif all_match_ordered:
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH
