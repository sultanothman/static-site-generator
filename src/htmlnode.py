

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

        for prop in self.props:
            props_as_text += f" {prop}={self.props[prop]}"

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