import shutil
import unittest
from pathlib import Path
from unittest.mock import patch

from arxiv_dl.__main__ import download_paper
from arxiv_dl.models import PaperData
from arxiv_dl.target_parser import (
    expand_target,
    get_huggingface_paper_urls_from_listing,
    is_huggingface_collection_url,
    is_huggingface_paper_url,
    is_huggingface_papers_listing_url,
    parse_target,
    process_huggingface_target,
)


class _Response:
    def __init__(self, text="", status_code=200):
        self.text = text
        self.status_code = status_code


class TestHuggingFaceTargets(unittest.TestCase):
    def test_process_huggingface_single_paper_urls(self):
        for paper_id in ("2605.12357", "2603.06408"):
            with self.subTest(paper_id=paper_id):
                url = f"https://huggingface.co/papers/{paper_id}"
                paper_data = process_huggingface_target(url)

                self.assertIsInstance(paper_data, PaperData)
                self.assertEqual(paper_data.paper_id, paper_id)
                self.assertEqual(
                    paper_data.abs_url, f"https://arxiv.org/abs/{paper_id}"
                )
                self.assertEqual(
                    paper_data.pdf_url, f"https://arxiv.org/pdf/{paper_id}.pdf"
                )
                self.assertEqual(paper_data.src_website, "ArXiv")

    def test_huggingface_single_paper_url_with_trailing_slash_and_query(self):
        paper_data = process_huggingface_target(
            "https://huggingface.co/papers/2605.12357/?utm_source=test#discussion"
        )

        self.assertEqual(paper_data.paper_id, "2605.12357")
        self.assertEqual(paper_data.abs_url, "https://arxiv.org/abs/2605.12357")
        self.assertEqual(paper_data.pdf_url, "https://arxiv.org/pdf/2605.12357.pdf")

    def test_parse_target_dispatches_huggingface_single_paper_url(self):
        paper_data = parse_target("https://huggingface.co/papers/2603.06408")

        self.assertIsInstance(paper_data, PaperData)
        self.assertEqual(paper_data.paper_id, "2603.06408")
        self.assertEqual(paper_data.src_website, "ArXiv")

    def test_huggingface_url_classification(self):
        self.assertTrue(
            is_huggingface_paper_url("https://huggingface.co/papers/2605.12357")
        )
        self.assertTrue(
            is_huggingface_papers_listing_url("https://huggingface.co/papers")
        )
        self.assertTrue(
            is_huggingface_papers_listing_url(
                "https://huggingface.co/papers/month/2026-05"
            )
        )
        self.assertTrue(
            is_huggingface_papers_listing_url(
                "https://huggingface.co/papers/date/2026-05-22"
            )
        )
        self.assertTrue(
            is_huggingface_papers_listing_url(
                "https://huggingface.co/papers/week/2026-W21"
            )
        )
        self.assertTrue(
            is_huggingface_papers_listing_url("https://huggingface.co/papers/trending")
        )
        self.assertTrue(
            is_huggingface_papers_listing_url("https://huggingface.co/akhaliq/papers")
        )
        self.assertTrue(
            is_huggingface_collection_url(
                "https://huggingface.co/collections/Testerpce/memory"
            )
        )
        self.assertFalse(
            is_huggingface_papers_listing_url(
                "https://huggingface.co/papers/month/2026-13"
            )
        )
        self.assertFalse(
            is_huggingface_papers_listing_url(
                "https://huggingface.co/papers/week/2026-w21"
            )
        )
        self.assertFalse(
            is_huggingface_papers_listing_url(
                "https://huggingface.co/papers/week/2026-21"
            )
        )
        self.assertFalse(
            is_huggingface_papers_listing_url("https://huggingface.co/models/papers")
        )
        self.assertFalse(
            is_huggingface_collection_url(
                "https://huggingface.co/collections?paper=2605.12357"
            )
        )
        self.assertFalse(is_huggingface_paper_url("https://huggingface.co/papers"))

    @patch("arxiv_dl.target_parser.requests.get")
    def test_extracts_unique_paper_urls_from_huggingface_listing_page(self, mock_get):
        mock_get.return_value = _Response("""
            <html>
              <body>
                <a href="/papers">Papers home</a>
                <a href="/papers/date/2026-05-22">Date page</a>
                <a href="/papers/2605.12357">First paper</a>
                <a href="https://huggingface.co/papers/2603.06408">Second paper</a>
                <a href="/papers/2605.12357">Duplicate first paper</a>
                <a href="/papers/2605.99999?from=listing#comments">Third paper</a>
                <a href="/papers?q=memory">Search link</a>
              </body>
            </html>
            """)

        paper_urls = get_huggingface_paper_urls_from_listing(
            "https://huggingface.co/papers/date/2026-05-22"
        )

        self.assertEqual(
            paper_urls,
            [
                "https://huggingface.co/papers/2605.12357",
                "https://huggingface.co/papers/2603.06408",
                "https://huggingface.co/papers/2605.99999",
            ],
        )
        mock_get.assert_called_once_with(
            "https://huggingface.co/papers/date/2026-05-22", timeout=10
        )

    @patch("arxiv_dl.target_parser.requests.get")
    def test_expand_target_expands_huggingface_month_page(self, mock_get):
        mock_get.return_value = _Response("""
            <a href="/papers/2605.12357">First paper</a>
            <a href="/papers/2603.06408">Second paper</a>
            """)

        self.assertEqual(
            expand_target("https://huggingface.co/papers/month/2026-05"),
            [
                "https://huggingface.co/papers/2605.12357",
                "https://huggingface.co/papers/2603.06408",
            ],
        )

    @patch("arxiv_dl.target_parser.requests.get")
    def test_expand_target_expands_all_supported_huggingface_list_pages(self, mock_get):
        mock_get.return_value = _Response("""
            <a href="/papers/2605.12357">First paper</a>
            <a href="/papers/2603.06408">Second paper</a>
            """)

        targets = [
            "https://huggingface.co/papers",
            "https://huggingface.co/papers/week/2026-W21",
            "https://huggingface.co/papers/trending",
            "https://huggingface.co/huggingface/papers",
            "https://huggingface.co/collections/Testerpce/memory",
        ]

        for target in targets:
            with self.subTest(target=target):
                self.assertEqual(
                    expand_target(target),
                    [
                        "https://huggingface.co/papers/2605.12357",
                        "https://huggingface.co/papers/2603.06408",
                    ],
                )

    def test_expand_target_leaves_single_paper_targets_unchanged(self):
        target = "https://huggingface.co/papers/2605.12357"

        self.assertEqual(expand_target(target), [target])


class TestHuggingFaceDownloadExpansion(unittest.TestCase):
    def setUp(self):
        self.root_dir = Path(__file__).resolve().parent.parent
        self.test_dir = self.root_dir / "tests" / "test_tmp_huggingface"
        self.test_dir.mkdir(exist_ok=True)

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)

    @patch("arxiv_dl.__main__._download_single_paper")
    @patch("arxiv_dl.__main__.expand_target")
    def test_download_paper_downloads_each_expanded_target(
        self, mock_expand_target, mock_download_single_paper
    ):
        expanded_targets = [
            "https://huggingface.co/papers/2605.12357",
            "https://huggingface.co/papers/2603.06408",
        ]
        mock_expand_target.return_value = expanded_targets
        mock_download_single_paper.side_effect = [True, True]

        success = download_paper(
            "https://huggingface.co/papers/month/2026-05",
            download_dir=self.test_dir,
            set_verbose_level="silent",
        )

        self.assertTrue(success)
        self.assertEqual(
            [
                kwargs["target"]
                for _, kwargs in mock_download_single_paper.call_args_list
            ],
            expanded_targets,
        )

    @patch("arxiv_dl.__main__._download_single_paper")
    @patch("arxiv_dl.__main__.expand_target")
    def test_download_paper_reports_failure_if_any_expanded_target_fails(
        self, mock_expand_target, mock_download_single_paper
    ):
        mock_expand_target.return_value = [
            "https://huggingface.co/papers/2605.12357",
            "https://huggingface.co/papers/2603.06408",
        ]
        mock_download_single_paper.side_effect = [True, False]

        success = download_paper(
            "https://huggingface.co/papers/date/2026-05-22",
            download_dir=self.test_dir,
            set_verbose_level="silent",
        )

        self.assertFalse(success)


if __name__ == "__main__":
    unittest.main()
