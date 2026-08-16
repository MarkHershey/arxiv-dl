import unittest
from unittest.mock import patch

from arxiv_dl.models import PaperData
from arxiv_dl.scrapers import scrape_metadata
from arxiv_dl.target_parser import (
    is_iclr_proceedings_paper_url,
    parse_target,
    process_iclr_target,
)

_ICLR_HOST = "https://proceedings.iclr.cc"
_PAPER_IDS_BY_YEAR = {
    2024: (
        "00153f90d9177dd3a872133972bc8dea",
        "0029db782591f06e5f12926ea3987ee6",
    ),
    2025: (
        "000eba875068854d5ff003b1fa534cd6",
        "006ad9bd7b14560770c15207a95b4895",
    ),
    2026: (
        "0021c2cb1b9b6a71ac478ea52a93b25a",
        "00295cede6e1600d344b5cd6d9fd4640",
    ),
}


def _expected_urls(year: int, paper_id: str):
    base_url = f"{_ICLR_HOST}/paper_files/paper/{year}"
    return (
        f"{base_url}/hash/{paper_id}-Abstract-Conference.html",
        f"{base_url}/file/{paper_id}-Paper-Conference.pdf",
    )


class TestProcessICLRTarget(unittest.TestCase):
    def _assert_paper_data(self, paper_data, year, paper_id):
        abs_url, pdf_url = _expected_urls(year, paper_id)

        self.assertIsInstance(paper_data, PaperData)
        self.assertEqual(paper_data.paper_id, paper_id)
        self.assertEqual(paper_data.abs_url, abs_url)
        self.assertEqual(paper_data.pdf_url, pdf_url)
        self.assertEqual(paper_data.year, year)
        self.assertEqual(paper_data.src_website, "ICLR")
        self.assertEqual(paper_data.paper_venue, "ICLR")
        self.assertEqual(paper_data.download_name, f"{year}_ICLR_{paper_id}.pdf")

    def test_processes_linked_abstract_and_pdf_urls_for_each_year(self):
        for year, paper_ids in _PAPER_IDS_BY_YEAR.items():
            for paper_id in paper_ids:
                abs_url, pdf_url = _expected_urls(year, paper_id)

                for target in (abs_url, pdf_url):
                    with self.subTest(year=year, paper_id=paper_id, target=target):
                        self._assert_paper_data(
                            process_iclr_target(target), year, paper_id
                        )

    def test_canonicalizes_supported_route_aliases(self):
        paper_id = _PAPER_IDS_BY_YEAR[2026][0]
        uppercase_id = paper_id.upper()
        targets = (
            f"https://proceedings.iclr.cc/paper/2026/hash/{paper_id}-Abstract-Conference.html",
            f"https://proceedings.iclr.cc/paper/2026/file/{paper_id}-Paper-Conference.pdf",
            f"https://proceedings.iclr.cc/paper_files/paper/2026/hash/{paper_id}-Abstract.html",
            f"http://proceedings.iclr.cc/paper/2026/hash/{uppercase_id}-Abstract.html?from=share#abstract",
        )

        for target in targets:
            with self.subTest(target=target):
                self._assert_paper_data(process_iclr_target(target), 2026, paper_id)

    def test_parse_target_dispatches_iclr_abstract_and_pdf_urls(self):
        year = 2026
        paper_id = _PAPER_IDS_BY_YEAR[year][0]

        abs_url, pdf_url = _expected_urls(year, paper_id)
        targets = (
            abs_url,
            pdf_url,
            f"{abs_url}?source=arxiv.org/abs/2312.16682#proceedings.neurips.cc",
        )
        for target in targets:
            with self.subTest(target=target):
                self._assert_paper_data(parse_target(target), year, paper_id)

    def test_rejects_non_paper_and_malformed_iclr_urls(self):
        paper_id = _PAPER_IDS_BY_YEAR[2026][0]
        invalid_targets = (
            f"https://proceedings.iclr.cc.evil.test/paper_files/paper/2026/hash/{paper_id}-Abstract-Conference.html",
            f"https://proceedings.iclr.cc@evil.test/paper_files/paper/2026/hash/{paper_id}-Abstract-Conference.html",
            f"https://evil.test/proceedings.iclr.cc/paper_files/paper/2026/hash/{paper_id}-Abstract-Conference.html",
            f"https://www.proceedings.iclr.cc/paper_files/paper/2026/hash/{paper_id}-Abstract-Conference.html",
            f"{_ICLR_HOST}/paper_files/paper/2026/hash/{paper_id[:-1]}-Abstract-Conference.html",
            f"{_ICLR_HOST}/paper_files/paper/2026/hash/{'g' + paper_id[1:]}-Abstract-Conference.html",
            f"{_ICLR_HOST}/paper_files/paper/2026/hash/{paper_id}-Paper-Conference.pdf",
            f"{_ICLR_HOST}/paper_files/paper/2026/file/{paper_id}-Abstract-Conference.html",
            f"{_ICLR_HOST}/paper_files/paper/2026/hash/{paper_id}-Abstract-OpenReview.html",
            f"{_ICLR_HOST}/paper_files/paper/2026/file/{paper_id}-Paper.pdf",
            f"{_ICLR_HOST}/paper_files/paper/2026/file/{paper_id}-Supplemental-Conference.zip",
            f"{_ICLR_HOST}/paper_files/paper/6279-/bibtex",
            f"{_ICLR_HOST}/paper_files/paper/2026",
        )

        for target in invalid_targets:
            with self.subTest(target=target):
                self.assertFalse(is_iclr_proceedings_paper_url(target))
                with self.assertRaises(Exception):
                    process_iclr_target(target)

    def test_scrape_metadata_uses_shared_proceedings_template(self):
        year = 2026
        paper_id = _PAPER_IDS_BY_YEAR[year][0]
        abs_url, pdf_url = _expected_urls(year, paper_id)
        bibtex_url = f"{_ICLR_HOST}/paper_files/paper/6279-/bibtex"
        supp_url = (
            f"{_ICLR_HOST}/paper_files/paper/{year}/file/"
            f"{paper_id}-Supplemental-Conference.zip"
        )
        html = f"""
        <html>
            <head>
                <meta name="citation_title" content="MAGREF: Masked Guidance for Any-Reference Video Generation">
                <meta name="citation_author" content="Deng, Yufan">
                <meta name="citation_author" content="Yin, Yuanyang">
                <meta name="citation_pdf_url" content="{pdf_url}">
            </head>
            <body>
                <h1 class="paper-title">MAGREF: Masked Guidance for Any-Reference Video Generation</h1>
                <p class="paper-authors">Yufan Deng, Yuanyang Yin</p>
                <div class="paper-actions">
                    <a href="/paper_files/paper/6279-/bibtex">Bibtex</a>
                    <a href="{pdf_url}">Paper</a>
                    <a href="{supp_url}">Supplemental</a>
                </div>
                <section>
                    <h2>Abstract</h2>
                    <p>A short ICLR abstract.</p>
                </section>
            </body>
        </html>
        """

        class Response:
            def __init__(self, text):
                self.status_code = 200
                self.text = text

        def fake_get(url):
            if url == abs_url:
                return Response(html)
            if url == bibtex_url:
                return Response("@inproceedings{iclr2026test}")
            raise AssertionError(f"Unexpected request: {url}")

        paper_data = process_iclr_target(abs_url)
        with patch("arxiv_dl.scrapers.requests.get", side_effect=fake_get):
            scrape_metadata(paper_data)

        self.assertEqual(
            paper_data.title,
            "MAGREF: Masked Guidance for Any-Reference Video Generation",
        )
        self.assertEqual(paper_data.authors, ["Deng, Yufan", "Yin, Yuanyang"])
        self.assertEqual(paper_data.abstract, "A short ICLR abstract.")
        self.assertEqual(paper_data.pdf_url, pdf_url)
        self.assertEqual(paper_data.supp_url, supp_url)
        self.assertEqual(paper_data.bibtex, "@inproceedings{iclr2026test}")
        self.assertEqual(
            paper_data.download_name,
            "2026_ICLR_MAGREF_Masked_Guidance_for_Any-Reference_Video_Generation.pdf",
        )


if __name__ == "__main__":
    unittest.main()
