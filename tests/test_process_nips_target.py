import unittest

from arxiv_dl.models import PaperData
from arxiv_dl.target_parser import parse_target, process_nips_target


# First two paper links from each annual proceedings page at
# https://proceedings.neurips.cc/.
_PAPER_IDS_BY_YEAR = {
    2025: (
        "0010031a1b4910aa67edbda26a705518",
        "0010665e949927b74faf6e3ada6d7f72",
    ),
    2024: (
        "000f947dcaff8fbffcc3f53a1314f358",
        "00295cede6e1600d344b5cd6d9fd4640",
    ),
    2023: (
        "0001ca33ba34ce0351e4612b744b3936",
        "001608167bb652337af5df0129aeaabd",
    ),
    2022: (
        "002262941c9edfd472a79298b2ac5e17",
        "00295cede6e1600d344b5cd6d9fd4640",
    ),
    2021: (
        "000c076c390a4c357313fca29e390ece",
        "003dd617c12d444ff9c80f717c3fa982",
    ),
    2020: (
        "0004d0b59e19461ff126e3a08a814c33",
        "00482b9bed15a272730fcb590ffebddd",
    ),
    2019: (
        "00989c20ff1386dc386d8124ebcba1a5",
        "00ac8ed3b4327bdd4ebbebcb2ba10a00",
    ),
    2018: (
        "00ac8ed3b4327bdd4ebbebcb2ba10a00",
        "01161aaa0b6d1345dd8fe4e481144d84",
    ),
    2017: (
        "0060ef47b12160b9198302ebdb144dcf",
        "0070d23b06b1486a538c0eaa45dd167a",
    ),
    2016: (
        "018b59ce1fd616d874afad0f44ba338d",
        "01931a6925d3de09e5f87419d9d55055",
    ),
    2015: (
        "01f78be6f7cad02658508fe4616098a9",
        "020c8bfac8de160d4c5543b96d1fdede",
    ),
    2014: (
        "002302d5a1c66195b6981e33e38df11d",
        "014b0027decf8737e4c1242be3054307",
    ),
    2013: (
        "01386bd6d8e091c2ab4c7c7de644d37b",
        "021bbc7ee20b71134d53e20206bd6feb",
    ),
    2012: (
        "00411460f7c92d2124a67ea0f4cb5f85",
        "01386bd6d8e091c2ab4c7c7de644d37b",
    ),
    2011: (
        "01386bd6d8e091c2ab4c7c7de644d37b",
        "013d407166ec4fa56eb1e1f8cbe183b9",
    ),
    2010: (
        "00411460f7c92d2124a67ea0f4cb5f85",
        "00e26af6ac3b1c1c49d7c3d79c60d000",
    ),
    2009: (
        "00411460f7c92d2124a67ea0f4cb5f85",
        "013d407166ec4fa56eb1e1f8cbe183b9",
    ),
    2008: (
        "00411460f7c92d2124a67ea0f4cb5f85",
        "0060ef47b12160b9198302ebdb144dcf",
    ),
    2007: (
        "0084ae4bc24c0795d1e6a4f58444d39b",
        "013a006f03dbc5392effeb8f18fda755",
    ),
    2006: (
        "019f8b946a256d9357eadc5ace2c8678",
        "03bfc1d4783966c69cc6aef8247e0103",
    ),
    2005: (
        "0172d289da48c48de8c5ebf3de9f7ee1",
        "02180771a9b609a26dcea07f272e141f",
    ),
    2004: (
        "026a39ae63343c68b5223a95f3e17616",
        "028ee724157b05d04e7bdcf237d12e60",
    ),
    2003: (
        "01a0683665f38d8e5e567b3b15ca98bf",
        "020bf2c45e7bb322f89a226bd2c5d41b",
    ),
    2002: (
        "00a03ec6533ca7f5c644d198d815329c",
        "01894d6f048493d2cacde3c579c315a3",
    ),
    2001: (
        "0004d0b59e19461ff126e3a08a814c33",
        "0070d23b06b1486a538c0eaa45dd167a",
    ),
    2000: (
        "04df4d434d481c5bb723be1b6df1ee65",
        "052335232b11864986bb2fa20fa38748",
    ),
    1999: (
        "01e00f2f4bfcbb7505cb641066f2859b",
        "02f039058bd48307e6f653a2005c9dd2",
    ),
    1998: (
        "020c8bfac8de160d4c5543b96d1fdede",
        "06a81a4fb98d149f2d31c68828fa6eb2",
    ),
    1997: (
        "01d8bae291b1e4724443375634ccfa0e",
        "0245952ecff55018e2a459517fdb40e3",
    ),
    1996: (
        "0188e8b8b014829e2fa0f430f0a95961",
        "018b59ce1fd616d874afad0f44ba338d",
    ),
    1995: (
        "00e26af6ac3b1c1c49d7c3d79c60d000",
        "021bbc7ee20b71134d53e20206bd6feb",
    ),
    1994: (
        "01882513d5fa7c329e940dda99b12147",
        "024d7f84fff11dd7e8d9c510137a2381",
    ),
    1993: (
        "013a006f03dbc5392effeb8f18fda755",
        "02a32ad2669e6fe298e607fe7cc0e1a0",
    ),
    1992: (
        "00ac8ed3b4327bdd4ebbebcb2ba10a00",
        "04ecb1fa28506ccb6f72b12c0245ddbc",
    ),
    1991: (
        "01f78be6f7cad02658508fe4616098a9",
        "0353ab4cbed5beae847a7ff6e220b5cf",
    ),
    1990: (
        "00411460f7c92d2124a67ea0f4cb5f85",
        "00ec53c4682d36f5c4359f4ae7bd7ba1",
    ),
    1989: (
        "01161aaa0b6d1345dd8fe4e481144d84",
        "0266e33d3f546cb5436a10798e657d97",
    ),
    1988: (
        "006f52e9102a8d3be2fe5614f42ba989",
        "013d407166ec4fa56eb1e1f8cbe183b9",
    ),
    1987: (
        "03004620ea802b9118dd44d69f07af56",
        "0316d8d63a0c252a3ec57921d7d2429b",
    ),
}


def _expected_urls(year, paper_id):
    base_url = f"https://proceedings.neurips.cc/paper_files/paper/{year}"

    if year >= 2022:
        abs_suffix = "Abstract-Conference.html"
        pdf_suffix = "Paper-Conference.pdf"
    else:
        abs_suffix = "Abstract.html"
        pdf_suffix = "Paper.pdf"

    return (
        f"{base_url}/hash/{paper_id}-{abs_suffix}",
        f"{base_url}/file/{paper_id}-{pdf_suffix}",
    )


def _expected_venue(year):
    return "NeurIPS" if year >= 2018 else "NIPS"


class TestProcessNIPSTarget(unittest.TestCase):
    def _assert_paper_data(self, paper_data, year, paper_id):
        abs_url, pdf_url = _expected_urls(year, paper_id)

        self.assertIsInstance(paper_data, PaperData)
        self.assertEqual(paper_data.paper_id, paper_id)
        self.assertEqual(paper_data.abs_url, abs_url)
        self.assertEqual(paper_data.pdf_url, pdf_url)
        self.assertEqual(paper_data.year, year)
        self.assertEqual(paper_data.src_website, "NeurIPS")
        self.assertEqual(paper_data.paper_venue, _expected_venue(year))

    def test_process_nips_abstract_urls_two_papers_per_year(self):
        for year, paper_ids in _PAPER_IDS_BY_YEAR.items():
            for paper_id in paper_ids:
                abs_url, _ = _expected_urls(year, paper_id)

                with self.subTest(year=year, paper_id=paper_id, target="abstract"):
                    paper_data = process_nips_target(abs_url)
                    self._assert_paper_data(paper_data, year, paper_id)

    def test_process_nips_pdf_urls_two_papers_per_year(self):
        for year, paper_ids in _PAPER_IDS_BY_YEAR.items():
            for paper_id in paper_ids:
                _, pdf_url = _expected_urls(year, paper_id)

                with self.subTest(year=year, paper_id=paper_id, target="pdf"):
                    paper_data = process_nips_target(pdf_url)
                    self._assert_paper_data(paper_data, year, paper_id)

    def test_parse_target_dispatches_neurips_abstract_url(self):
        year = 2025
        paper_id = _PAPER_IDS_BY_YEAR[year][0]
        abs_url, _ = _expected_urls(year, paper_id)

        paper_data = parse_target(abs_url)

        self._assert_paper_data(paper_data, year, paper_id)

    def test_parse_target_dispatches_neurips_pdf_url(self):
        year = 1987
        paper_id = _PAPER_IDS_BY_YEAR[year][0]
        _, pdf_url = _expected_urls(year, paper_id)

        paper_data = parse_target(pdf_url)

        self._assert_paper_data(paper_data, year, paper_id)


if __name__ == "__main__":
    unittest.main()
