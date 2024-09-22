

class HTMLNode:
    def __init__(self, tag = None, value = None, children = None, props = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        props_as_text = ""

        if self.props:
            for prop in self.props:
                props_as_text += f" {prop}=\"{self.props[prop]}\""

        return props_as_text
    
    def __repr__(self) -> str:
        htmlnode_repr_result = "HTMLNode(" 
        
        htmlnode_repr_values = []
        if self.tag:
            htmlnode_repr_values.append(f"tag={self.tag}")
        htmlnode_repr_values.append(f"value={self.value}")
        if self.children:
            for child in self.children:
                htmlnode_repr_values.append(f"child={repr(child)}")
        if self.props:
            htmlnode_repr_values.append(f"props={self.props_to_html()}")
        
        htmlnode_repr_result += ", ".join(htmlnode_repr_values)
        htmlnode_repr_result += ")"
        return htmlnode_repr_result
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("Invalid HTML: no value")
        if self.tag is None:
            return self.value
        
        props_value = self.props_to_html()

        return f"<{self.tag}{props_value}>{self.value}</{self.tag}>"
    
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("Invalid HTML: tag is mandatory")
        if self.children is None:
            raise ValueError("Invalid HTML: children are mandatory")
        children_html = []
        for child in self.children:
            children_html.append(child.to_html())

        children_value =  "".join(children_html)
        return f"<{self.tag}{self.props_to_html()}>{children_value}</{self.tag}>"