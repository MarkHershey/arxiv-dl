import sys
import unittest
from pathlib import Path

from arxiv_dl.target_parser import valid_arxiv_id


class TestArxivIdentifier(unittest.TestCase):
    def test_valid_identifier(self):
        valid_id = "2103.15538"
        self.assertTrue(valid_arxiv_id(valid_id))
        valid_id = "2103.15538v1"
        self.assertTrue(valid_arxiv_id(valid_id))
        valid_id = "2103.15538v2"
        self.assertTrue(valid_arxiv_id(valid_id))
        valid_id = "2103.15538v21"
        self.assertTrue(valid_arxiv_id(valid_id))
        valid_id = "2103.99999"
        self.assertTrue(valid_arxiv_id(valid_id))
        valid_id = "2103.00001"
        self.assertTrue(valid_arxiv_id(valid_id))
        valid_id = "2912.15538"
        self.assertTrue(valid_arxiv_id(valid_id))

    def test_invalid_year_identifier(self):
        """
        Right format, but invalid year range.
        """
        invalid_id = "0701.15538"
        self.assertFalse(valid_arxiv_id(invalid_id))


    def test_valid_legacy_identifier(self):
        legacy_id = "math.GT/0211159"
        self.assertTrue(valid_arxiv_id(legacy_id))
        legacy_id = "cs/0701188"
        self.assertTrue(valid_arxiv_id(legacy_id))

    def test_invalid_identifier(self):
        valid_id = "213.15538"
        self.assertFalse(valid_arxiv_id(valid_id))
        valid_id = "2103.234"
        self.assertFalse(valid_arxiv_id(valid_id))
        valid_id = "210315538v2"
        self.assertFalse(valid_arxiv_id(valid_id))
        valid_id = "2103:15538v21"
        self.assertFalse(valid_arxiv_id(valid_id))
        valid_id = "5403.1234"
        self.assertFalse(valid_arxiv_id(valid_id))
        valid_id = "2103.00001Vd"
        self.assertFalse(valid_arxiv_id(valid_id))
        valid_id = "0000.15538vv99"
        self.assertFalse(valid_arxiv_id(valid_id))
        valid_id = "sdff.dsdf"
        self.assertFalse(valid_arxiv_id(valid_id))
        valid_id = "2113.5538"
        self.assertFalse(valid_arxiv_id(valid_id))
        valid_id = "2112.55"
        self.assertFalse(valid_arxiv_id(valid_id))
        valid_id = "2112=0055"
        self.assertFalse(valid_arxiv_id(valid_id))
        valid_id = "2112$0055"
        self.assertFalse(valid_arxiv_id(valid_id))
        valid_id = "2112:0055"
        self.assertFalse(valid_arxiv_id(valid_id))
        valid_id = 2112.0055
        self.assertFalse(valid_arxiv_id(valid_id))
        valid_id = ["2112.0055"]
        self.assertFalse(valid_arxiv_id(valid_id))


if __name__ == "__main__":
    unittest.main()
