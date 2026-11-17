import unittest
from block_conversion import *

class TestMdToBlocks(unittest.TestCase):
    def test_multilines_text(self):
        text = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        current = md_to_blocks(text)
        expected = [
            "This is **bolded** paragraph",
            "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
            "- This is a list\n- with items",
        ]
        self.assertEqual(current, expected)

        text2 = """
Here is **bolded** paragraph

    This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        current = md_to_blocks(text2)
        expected = [
            "Here is **bolded** paragraph",
            "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
            "- This is a list\n- with items",
        ]
        self.assertEqual(current, expected)

class TestBlockToBlockType(unittest.TestCase):
    def test_block_to_block_type(self):
        block = "# That should be a BIG TITLE" 
        current = block_to_block_type(block)
        expected = BlockType.HEADING
        self.assertEqual(current, expected)

        block = "###### That should be a small title" 
        current = block_to_block_type(block)
        expected = BlockType.HEADING
        self.assertEqual(current, expected)

        block = "> That should be a quote\nEven if there is a linebreak" 
        current = block_to_block_type(block)
        expected = BlockType.QUOTE
        self.assertEqual(current, expected)

        block = ">That should also be a quote\nEven if there is a linebreak" 
        current = block_to_block_type(block)
        expected = BlockType.QUOTE
        self.assertEqual(current, expected)

        block = """```
def func(test): return test + "!"
```
"""
        current = block_to_block_type(block)
        expected = BlockType.CODE
        self.assertEqual(current, expected)

        block = """```
Even this code text
should be @#$
code_text(input)
```
"""
        current = block_to_block_type(block)
        expected = BlockType.CODE
        self.assertEqual(current, expected)

        block = "This > should be normal text"
        current = block_to_block_type(block)
        expected = BlockType.PARAGRAPH
        self.assertEqual(current, expected)

        block = "Also this ### should be normal text ```"
        current = block_to_block_type(block)
        expected = BlockType.PARAGRAPH
        self.assertEqual(current, expected)

        block = """- It must be
- an
- unsorted list"""
        current = block_to_block_type(block)
        expected = BlockType.UL
        self.assertEqual(current, expected)

        block = """- but this
should- not
- be an ul"""
        current = block_to_block_type(block)
        expected = BlockType.PARAGRAPH
        self.assertEqual(current, expected)

        block = """- and also this
-not
- be an ul"""
        current = block_to_block_type(block)
        expected = BlockType.PARAGRAPH
        self.assertEqual(current, expected)

        block = """1. OL here
2. as u can
3. see"""
        current = block_to_block_type(block)
        expected = BlockType.OL
        self.assertEqual(current, expected)

        block = """1. no OL here
2, as u can
3. see"""
        current = block_to_block_type(block)
        expected = BlockType.PARAGRAPH
        self.assertEqual(current, expected)

        block = """1. no OL here
 2. as u can
3. see"""
        current = block_to_block_type(block)
        expected = BlockType.PARAGRAPH
        self.assertEqual(current, expected)