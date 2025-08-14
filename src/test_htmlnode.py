import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode(
            "a",
            "Click me!",
            None,
            {"href": "https://www.google.com", "target": "_blank"},
        )
        self.assertEqual(
            node.props_to_html(),
            ' href="https://www.google.com" target="_blank"',
        )

    def test_props_to_html_empty(self):
        node = HTMLNode("p", "Just some text")
        self.assertEqual(node.props_to_html(), "")
        
    def test_props_to_html_single_prop(self):
        node = HTMLNode("img", None, None, {"src": "image.jpg"})
        self.assertEqual(node.props_to_html(), ' src="image.jpg"')

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

    def test_leaf_with_children(self):
        with self.assertRaises(ValueError):
            LeafNode("p", "Text", [LeafNode("span", "child")])
    
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")
        
    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_many_children(self):
        child1 = LeafNode("b", "bold text")
        child2 = LeafNode(None, "normal text")
        child3 = LeafNode("i", "italic text")
        child4 = LeafNode(None, "normal text")
        parent_node = ParentNode("p", [child1, child2, child3, child4])
        self.assertEqual(parent_node.to_html(), "<p><b>bold text</b>normal text<i>italic text</i>normal text</p>")

if __name__ == "__main__":
    unittest.main()
