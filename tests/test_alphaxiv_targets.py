import unittest

from arxiv_dl.models import PaperData
from arxiv_dl.target_parser import is_alphaxiv_paper_url, parse_target


class TestAlphaXivTargets(unittest.TestCase):
    def assert_canonical_arxiv_paper(self, target: str, paper_id: str) -> None:
        result = parse_target(target)

        self.assertIsInstance(result, PaperData)
        self.assertEqual(result.paper_id, paper_id)
        self.assertEqual(result.abs_url, f"https://arxiv.org/abs/{paper_id}")
        self.assertEqual(result.pdf_url, f"https://arxiv.org/pdf/{paper_id}.pdf")
        self.assertEqual(result.src_website, "ArXiv")

    def test_supplied_alphaxiv_urls_use_the_arxiv_download_route(self):
        targets = (
            "https://www.alphaxiv.org/abs/2312.16682v2",
            "https://www.alphaxiv.org/pdf/2312.16682v2",
            "https://www.alphaxiv.org/abs/2312.16682",
        )

        for target in targets:
            with self.subTest(target=target):
                self.assert_canonical_arxiv_paper(target, "2312.16682")

    def test_alphaxiv_paper_url_variants(self):
        targets = (
            "https://alphaxiv.org/overview/2312.16682v2?ref=share#comments",
            "http://www.alphaxiv.org/html/2312.16682v2/",
            "www.alphaxiv.org/abs/2312.16682.md",
            "alphaxiv.org/pdf/2312.16682v2",
            "https://www.alphaxiv.org/zh/abs/2312.16682v2",
            "https://pdfs.assets.alphaxiv.org/2312.16682v2.pdf",
        )

        for target in targets:
            with self.subTest(target=target):
                self.assertTrue(is_alphaxiv_paper_url(target))
                self.assert_canonical_arxiv_paper(target, "2312.16682")

    def test_alphaxiv_legacy_arxiv_id(self):
        self.assert_canonical_arxiv_paper(
            "https://www.alphaxiv.org/abs/math.GT/0211159v2",
            "math.GT/0211159",
        )

    def test_rejects_lookalike_hosts_and_invalid_paper_urls(self):
        targets = (
            "https://notalphaxiv.org/abs/2312.16682",
            "https://alphaxiv.org.example.com/abs/2312.16682",
            "https://www.alphaxiv.org/about",
            "https://www.alphaxiv.org/abs/2313.16682",
            "https://www.alphaxiv.org/abs/2312.166820",
            "https://www.alphaxiv.org/abs/x2312.16682junk",
            "https://www.alphaxiv.org/abs/math.GT/02111599",
        )

        for target in targets:
            with self.subTest(target=target):
                self.assertFalse(is_alphaxiv_paper_url(target))


if __name__ == "__main__":
    unittest.main()
