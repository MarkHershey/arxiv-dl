import sys
import unittest
from pathlib import Path

src_dir = Path(__file__).resolve().parent.parent / "arxiv_dl"

sys.path.insert(0, str(src_dir))

from arxiv_dl import validate_arxiv_paper_id


class TestArxivIdentifier(unittest.TestCase):
    def test_valid_identifier(self):
        valid_id = "2103.15538"
        validate_arxiv_paper_id(valid_id)
        valid_id = "2103.15538v1"
        validate_arxiv_paper_id(valid_id)
        valid_id = "2103.15538v2"
        validate_arxiv_paper_id(valid_id)
        valid_id = "2103.15538v21"
        validate_arxiv_paper_id(valid_id)
        valid_id = "2103.99999"
        validate_arxiv_paper_id(valid_id)
        valid_id = "2103.00001"
        validate_arxiv_paper_id(valid_id)
        valid_id = "0701.15538"
        validate_arxiv_paper_id(valid_id)
        valid_id = "2912.15538"
        validate_arxiv_paper_id(valid_id)

    def test_invalid_identifier(self):
        with self.assertRaises(ValueError):
            valid_id = "213.15538"
            validate_arxiv_paper_id(valid_id)
        with self.assertRaises(ValueError):
            valid_id = "2103.234"
            validate_arxiv_paper_id(valid_id)
        with self.assertRaises(ValueError):
            valid_id = "210315538v2"
            validate_arxiv_paper_id(valid_id)
        with self.assertRaises(ValueError):
            valid_id = "2103:15538v21"
            validate_arxiv_paper_id(valid_id)
        with self.assertRaises(ValueError):
            valid_id = "5403.1234"
            validate_arxiv_paper_id(valid_id)
        with self.assertRaises(ValueError):
            valid_id = "2103.00001Vd"
            validate_arxiv_paper_id(valid_id)
        with self.assertRaises(ValueError):
            valid_id = "0000.15538vv99"
            validate_arxiv_paper_id(valid_id)
        with self.assertRaises(ValueError):
            valid_id = "sdff.dsdf"
            validate_arxiv_paper_id(valid_id)
        with self.assertRaises(ValueError):
            valid_id = "2113.5538"
            validate_arxiv_paper_id(valid_id)
        with self.assertRaises(ValueError):
            valid_id = "2112.55"
            validate_arxiv_paper_id(valid_id)
        with self.assertRaises(ValueError):
            valid_id = "2112=0055"
            validate_arxiv_paper_id(valid_id)
        with self.assertRaises(ValueError):
            valid_id = "2112$0055"
            validate_arxiv_paper_id(valid_id)
        with self.assertRaises(ValueError):
            valid_id = "2112:0055"
            validate_arxiv_paper_id(valid_id)
        with self.assertRaises(TypeError):
            valid_id = 2112.0055
            validate_arxiv_paper_id(valid_id)
        with self.assertRaises(TypeError):
            valid_id = ["2112.0055"]
            validate_arxiv_paper_id(valid_id)


if __name__ == "__main__":
    unittest.main()
