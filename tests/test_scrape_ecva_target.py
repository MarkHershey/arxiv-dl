import sys
import unittest
from pathlib import Path

from arxiv_dl.target_parser import process_ecva_target
from arxiv_dl.models import PaperData
from arxiv_dl.scrapers import scrape_metadata_ecva

root_dir = Path(__file__).resolve().parent.parent

sys.path.insert(0, str(root_dir))


class TestScrapeECVA(unittest.TestCase):
    def test_ECCV2024(self):
        abs_url = "https://www.ecva.net/papers/eccv_2024/papers_ECCV/html/4_ECCV_2024_paper.php"
        pdf_url = "https://www.ecva.net/papers/eccv_2024/papers_ECCV/papers/00004.pdf"
        paper_title = "Is Retain Set All You Need in Machine Unlearning? Restoring Performance of Unlearned Models with Out-Of-Distribution Images"
        paper_data = process_ecva_target(abs_url)
        scrape_metadata_ecva(paper_data)
        self.assertTrue(isinstance(paper_data, PaperData))
        self.assertEqual(paper_data.abs_url, abs_url)
        self.assertEqual(paper_data.pdf_url, pdf_url)
        self.assertEqual(paper_data.src_website, "ECVA")
        self.assertEqual(paper_data.title, paper_title)
        self.assertEqual(paper_data.year, 2024)
        self.assertEqual(paper_data.paper_venue, "ECCV")
        self.assertEqual(
            paper_data.authors,
            [
                "Jacopo Bonato",
                "Marco Cotogni",
                "Luigi Sabetta",
            ],
        )

    def test_ECCV2022(self):
        abs_url = "https://www.ecva.net/papers/eccv_2022/papers_ECCV/html/19_ECCV_2022_paper.php"
        pdf_url = (
            "https://www.ecva.net/papers/eccv_2022/papers_ECCV/papers/136610001.pdf"
        )
        paper_title = "Learning Depth from Focus in the Wild"
        paper_data = process_ecva_target(abs_url)
        scrape_metadata_ecva(paper_data)
        self.assertTrue(isinstance(paper_data, PaperData))
        self.assertEqual(paper_data.abs_url, abs_url)
        self.assertEqual(paper_data.pdf_url, pdf_url)
        self.assertEqual(paper_data.src_website, "ECVA")
        self.assertEqual(paper_data.title, paper_title)
        self.assertEqual(paper_data.year, 2022)
        self.assertEqual(paper_data.paper_venue, "ECCV")
        self.assertEqual(
            paper_data.authors,
            [
                "Changyeon Won",
                "Hae-Gon Jeon",
            ],
        )

    def test_ECCV2020(self):
        abs_url = "https://www.ecva.net/papers/eccv_2020/papers_ECCV/html/267_ECCV_2020_paper.php"
        pdf_url = (
            "https://www.ecva.net/papers/eccv_2020/papers_ECCV/papers/123460001.pdf"
        )
        paper_title = "Quaternion Equivariant Capsule Networks for 3D Point Clouds"
        paper_data = process_ecva_target(abs_url)
        scrape_metadata_ecva(paper_data)
        self.assertTrue(isinstance(paper_data, PaperData))
        self.assertEqual(paper_data.abs_url, abs_url)
        self.assertEqual(paper_data.pdf_url, pdf_url)
        self.assertEqual(paper_data.src_website, "ECVA")
        self.assertEqual(paper_data.title, paper_title)
        self.assertEqual(paper_data.year, 2020)
        self.assertEqual(paper_data.paper_venue, "ECCV")
        self.assertEqual(
            paper_data.authors,
            [
                "Yongheng Zhao",
                "Tolga Birdal",
                "Jan Eric Lenssen",
                "Emanuele Menegatti",
                "Leonidas Guibas",
                "Federico Tombari",
            ],
        )

    def test_ECCV2018(self):
        abs_url = "https://www.ecva.net/papers/eccv_2018/papers_ECCV/html/Yonggen_Ling_Modeling_Varying_Camera-IMU_ECCV_2018_paper.php"
        pdf_url = "https://www.ecva.net/papers/eccv_2018/papers_ECCV/papers/Yonggen_Ling_Modeling_Varying_Camera-IMU_ECCV_2018_paper.pdf"
        paper_title = "Modeling Varying Camera-IMU Time Offset in Optimization-Based Visual-Inertial Odometry"
        paper_data = process_ecva_target(abs_url)
        scrape_metadata_ecva(paper_data)
        self.assertTrue(isinstance(paper_data, PaperData))
        self.assertEqual(paper_data.abs_url, abs_url)
        self.assertEqual(paper_data.pdf_url, pdf_url)
        self.assertEqual(paper_data.src_website, "ECVA")
        self.assertEqual(paper_data.title, paper_title)
        self.assertEqual(paper_data.year, 2018)
        self.assertEqual(paper_data.paper_venue, "ECCV")
        self.assertEqual(
            paper_data.authors,
            [
                "Yonggen Ling",
                "Linchao Bao",
                "Zequn Jie",
                "Fengming Zhu",
                "Ziyang Li",
                "Shanmin Tang",
                "Yongsheng Liu",
                "Wei Liu",
                "Tong Zhang",
            ],
        )
