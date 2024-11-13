from textnode import TextNode, TextType
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.NORMAL:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("Invalid markdown, formatted section not closed")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.NORMAL))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)",text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

    
def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.NORMAL:
            new_nodes.append(old_node)
            continue
        
        split_nodes_images = []
        remaining_text = old_node.text
        images = extract_markdown_images(remaining_text)
        
        for alt_text, url in images:
            pre_image, remaining_text = remaining_text.split(f"![{alt_text}]({url})", 1)
            if pre_image:
                split_nodes_images.append(TextNode(pre_image, TextType.NORMAL))
            split_nodes_images.append(TextNode(alt_text, TextType.IMAGE, url=url))
        
        if remaining_text:
            split_nodes_images.append(TextNode(remaining_text, TextType.NORMAL))
        
        new_nodes.extend(split_nodes_images)
        
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.NORMAL:
            new_nodes.append(old_node)
            continue
    
        split_nodes_links = []
        remaining_text = old_node.text
        links = extract_markdown_links(remaining_text)

        for link_text, url in links:
            pre_link, remaining_text = remaining_text.split(f"[{link_text}]({url})", 1)
            if pre_link:
                split_nodes_links.append(TextNode(pre_link, TextType.NORMAL))
            split_nodes_links.append(TextNode(link_text, TextType.LINK, url=url))
        
        if remaining_text:
            split_nodes_links.append(TextNode(remaining_text, TextType.NORMAL))
        
        new_nodes.extend(split_nodes_links)
        
    return new_nodes

def text_to_textnode(text):
    nodes = [TextNode(text, TextType.NORMAL)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes,"*", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes