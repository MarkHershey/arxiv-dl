import sys
import unittest
from pathlib import Path

from arxiv_dl.target_parser import process_arxiv_target
from arxiv_dl.models import PaperData


class TestProcessArxivTarget(unittest.TestCase):
    def test_process_arxiv_target_with_direct_id_modern(self):
        """Test processing modern arXiv ID directly."""
        paper_id = "2103.15538"
        result = process_arxiv_target(paper_id)
        
        self.assertIsInstance(result, PaperData)
        self.assertEqual(result.paper_id, paper_id)
        self.assertEqual(result.abs_url, f"https://arxiv.org/abs/{paper_id}")
        self.assertEqual(result.pdf_url, f"https://arxiv.org/pdf/{paper_id}.pdf")
        self.assertEqual(result.src_website, "ArXiv")

    def test_process_arxiv_target_with_direct_id_modern_with_version(self):
        """Test processing modern arXiv ID with version number."""
        paper_id = "2103.15538"
        result = process_arxiv_target(paper_id)
        
        self.assertIsInstance(result, PaperData)
        self.assertEqual(result.paper_id, "2103.15538")
        self.assertEqual(result.abs_url, f"https://arxiv.org/abs/2103.15538")
        self.assertEqual(result.pdf_url, f"https://arxiv.org/pdf/2103.15538.pdf")
        self.assertEqual(result.src_website, "ArXiv")

    def test_process_arxiv_target_with_direct_id_legacy(self):
        """Test processing legacy arXiv ID directly."""
        paper_id = "math.GT/0211159"
        result = process_arxiv_target(paper_id)
        
        self.assertIsInstance(result, PaperData)
        self.assertEqual(result.paper_id, paper_id)
        self.assertEqual(result.abs_url, f"https://arxiv.org/abs/{paper_id}")
        self.assertEqual(result.pdf_url, f"https://arxiv.org/pdf/{paper_id}.pdf")
        self.assertEqual(result.src_website, "ArXiv")

    def test_process_arxiv_target_with_url_modern(self):
        """Test processing modern arXiv URL."""
        url = "https://arxiv.org/abs/2103.15538"
        result = process_arxiv_target(url)
        
        self.assertIsInstance(result, PaperData)
        self.assertEqual(result.paper_id, "2103.15538")
        self.assertEqual(result.abs_url, "https://arxiv.org/abs/2103.15538")
        self.assertEqual(result.pdf_url, "https://arxiv.org/pdf/2103.15538.pdf")
        self.assertEqual(result.src_website, "ArXiv")

    def test_process_arxiv_target_with_url_modern_with_version(self):
        """Test processing modern arXiv URL with version number."""
        url = "https://arxiv.org/abs/2103.15538v2"
        result = process_arxiv_target(url)
        
        self.assertIsInstance(result, PaperData)
        self.assertEqual(result.paper_id, "2103.15538")
        self.assertEqual(result.abs_url, "https://arxiv.org/abs/2103.15538")
        self.assertEqual(result.pdf_url, "https://arxiv.org/pdf/2103.15538.pdf")
        self.assertEqual(result.src_website, "ArXiv")

    def test_process_arxiv_target_with_url_legacy(self):
        """Test processing legacy arXiv URL."""
        url = "https://arxiv.org/abs/math.GT/0211159"
        result = process_arxiv_target(url)
        
        self.assertIsInstance(result, PaperData)
        self.assertEqual(result.paper_id, "math.GT/0211159")
        self.assertEqual(result.abs_url, "https://arxiv.org/abs/math.GT/0211159")
        self.assertEqual(result.pdf_url, "https://arxiv.org/pdf/math.GT/0211159.pdf")
        self.assertEqual(result.src_website, "ArXiv")

    def test_process_arxiv_target_with_url_legacy_2nd(self):
        """Test processing legacy arXiv URL."""
        url = "https://arxiv.org/abs/cs/0701188"
        result = process_arxiv_target(url)
        
        self.assertIsInstance(result, PaperData)
        self.assertEqual(result.paper_id, "cs/0701188")
        self.assertEqual(result.abs_url, "https://arxiv.org/abs/cs/0701188")
        self.assertEqual(result.pdf_url, "https://arxiv.org/pdf/cs/0701188.pdf")
        self.assertEqual(result.src_website, "ArXiv")

    def test_process_arxiv_target_with_pdf_url_modern(self):
        """Test processing modern arXiv PDF URL."""
        url = "https://arxiv.org/pdf/2103.15538.pdf"
        result = process_arxiv_target(url)
        
        self.assertIsInstance(result, PaperData)
        self.assertEqual(result.paper_id, "2103.15538")
        self.assertEqual(result.abs_url, "https://arxiv.org/abs/2103.15538")
        self.assertEqual(result.pdf_url, "https://arxiv.org/pdf/2103.15538.pdf")
        self.assertEqual(result.src_website, "ArXiv")

    def test_process_arxiv_target_with_pdf_url_modern_with_version(self):
        """Test processing modern arXiv PDF URL with version number."""
        url = "https://arxiv.org/pdf/2103.15538v2.pdf"
        result = process_arxiv_target(url)
        
        self.assertIsInstance(result, PaperData)
        self.assertEqual(result.paper_id, "2103.15538")
        self.assertEqual(result.abs_url, "https://arxiv.org/abs/2103.15538")
        self.assertEqual(result.pdf_url, "https://arxiv.org/pdf/2103.15538.pdf")
        self.assertEqual(result.src_website, "ArXiv")

    def test_process_arxiv_target_with_pdf_url_legacy(self):
        """Test processing legacy arXiv PDF URL."""
        url = "https://arxiv.org/pdf/math.GT/0211159"
        result = process_arxiv_target(url)
        
        self.assertIsInstance(result, PaperData)
        self.assertEqual(result.paper_id, "math.GT/0211159")
        self.assertEqual(result.abs_url, "https://arxiv.org/abs/math.GT/0211159")
        self.assertEqual(result.pdf_url, "https://arxiv.org/pdf/math.GT/0211159.pdf")
        self.assertEqual(result.src_website, "ArXiv")




if __name__ == "__main__":
    unittest.main()
