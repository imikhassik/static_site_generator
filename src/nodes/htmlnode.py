class HTMLNode:
    def __init__(self, tag=None, value=None, props=None, children=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        result = ''

        if not self.props:
            return result

        for key, value in self.props.items():
            prop = f' {key}="{value}"'
            result += prop

        return result

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"


class LeafNode(HTMLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def to_html(self):
        if not self.value:
            raise ValueError("LeafNode must have a value")
        if not self.tag:
            return self.value

        if self.tag == "img":
            return f'<{self.tag}{self.props_to_html()}>'
        
        return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'


class ParentNode(HTMLNode):
    def __init__(self, tag=None, children=None, props=None):
        super().__init__(tag=tag, children=children, props=props)

    def to_html(self):
        if not self.tag:
            raise ValueError("Parent node must have a tag")
        if not self.children:
            raise ValueError("Parent node must have children")

        html_string = f'<{self.tag}{self.props_to_html()}>'
        for child in self.children:
            html_string += child.to_html()
        html_string += f'</{self.tag}>'

        return html_string


def main():
    html_node = HTMLNode(
        tag="a", 
        value="Link text", 
        children=['a', 'b'], 
        props={
            "href": "http://example.com",
            "target": "_blank",
        }
    )
    print(html_node)


main()
