class HTMLNode:
    def __init__ (self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        if self.props == None:
            return ""
        else:
            words = []
            for key, value in self.props.items():
                formated = f' {key}="{value}"'
                words.append(formated)
            return "".join(words)

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"


class LeafNode(HTMLNode):
    def __init__ (self, tag, value, props=None):
        super().__init__(tag, value, children=None, props=props)

    def to_html(self):
        if self.value == None:
            raise ValueError
        elif self.tag == None:
            return self.value
        else:
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"


class ParentNode(HTMLNode):
    def __init__ (self, tag, children, props=None):
        super().__init__(tag, value=None ,children=children, props=props)
    
    def to_html(self):
        if self.tag == None:
            raise ValueError('No tag in parents class')
        elif len(self.children) == 0:
            raise ValueError('No Children in ParentNode')
        else:
            New_born = []
            for child in self.children:
                returned = child.to_html()
                New_born.append(returned)
            Baby = "".join(New_born)
            return f'<{self.tag}{self.props_to_html()}>{Baby}</{self.tag}>'

transfomation_map = {
        TextType.NORMAL: lambda node: LeafNode("", node.text),
        TextType.BOLD: lambda node: LeafNode("b", node.text),
        TextType.ITALIC: lambda node: LeafNode("i", node.text),
        TextType.CODE: lambda node: LeafNode("code", node.text),
        TextType.LINK: lambda node: LeafNode("a", node.text, {"href": node.url}),
        TextType.IMAGE: lambda node: LeafNode("img", "", {"src": node.url, "alt": node.text})
        }

def text_node_to_html_node(text_node):
    if text_node.text_type in transfomation_map:
        return transfomation_map[text_node.text_type](text_node)
    else:
        raise ValueError("Unsupported TextTypes!")
               