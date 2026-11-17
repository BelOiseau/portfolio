class HTMLNode():
    def __init__(
        self,
        tag: str | None = None,
        value: str | None = None,
        children: list["HTMLNode"] | None = None,
        props: dict[str, str] | None = None
    ) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self) -> str:
        node_attributes = ""
        for attribute, value in self.props.items():
            node_attributes += f' {attribute}="{value}"'
        return node_attributes

    def __repr__(self) -> str:
        output = f"tag: '{self.tag}', value: '{self.value}', children: {self.children}, props: {self.props}"
        return output

class ParentNode(HTMLNode):
    def __init__(
        self, tag: str, children: list[HTMLNode], props: dict[str, str] | None = None
    ) -> None:
        super().__init__(tag=tag, children=children, props=props)

    def to_html(self) -> str:
        if self.tag is None:
            raise ValueError("Tag is required")
        if self.children is None:
            raise ValueError("Children must not be None")

        html = []
        html.append(f"<{self.tag}")
        if self.props is not None:
            attribute = super().props_to_html()
            html.append(attribute)

        inner_html = []
        for node in self.children:
            inner_html.append(node.to_html())

        html.append(f">{"".join(inner_html)}</{self.tag}>")
        return "".join(html)

class LeafNode(HTMLNode):
    def __init__(
        self,
        tag: str | None,
        value: str,
        props: dict[str, str] | None = None
    ) -> None:
        super().__init__(tag=tag, value=value, props=props)
    
    def to_html(self) -> str:
        if self.value is None:
            raise ValueError("Value must not be None")
        if self.tag is None:
            return self.value
        html = []
        html.append(f"<{self.tag}")
        if self.props is not None:
            attribute = super().props_to_html()
            html.append(attribute)
        html.append(f">{self.value}</{self.tag}>")
        return "".join(html)

    def __repr__(self) -> str:
        return f"tag: '{self.tag}', value: '{self.value}', props: {self.props}"
