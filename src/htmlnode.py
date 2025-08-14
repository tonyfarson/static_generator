class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("to_html method not implemented")

    def props_to_html(self):
        if not self.props:
            return ""
        # Build attributes in insertion order (default in modern Python)
        return "".join(f' {k}="{v}"' for k, v in self.props.items())

    def __repr__(self):
        return (
            f"HTMLNode(tag={self.tag}, value={self.value}, "
            f"children={self.children}, props={self.props})"
        )


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        # Leaf nodes must have a value
        if value is None:
            raise ValueError("LeafNode must have a value")
        # If someone tries to pass children in the 3rd arg (a list), fail fast
        if isinstance(props, list):
            raise ValueError("LeafNode cannot have children")
        super().__init__(tag=tag, value=value, children=None, props=props)

    def to_html(self):
        if self.value is None:
            raise ValueError("LeafNode must have a value to render HTML")
        # If no tag, just return the text value
        if self.tag is None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        # Parent nodes must have a tag and children
        if tag is None:
            raise ValueError("ParentNode must have a tag")
        if children is None:
            raise ValueError("ParentNode must have children")
        super().__init__(tag=tag, value=None, children=children, props=props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("ParentNode must have a tag")
        if self.children is None:
            raise ValueError("ParentNode must have children")

        # Recursively render all children
        inner = "".join(child.to_html() for child in self.children)
        return f"<{self.tag}{self.props_to_html()}>{inner}</{self.tag}>"
