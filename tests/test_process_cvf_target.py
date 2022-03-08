import sys
import unittest
from pathlib import Path

root_dir = Path(__file__).resolve().parent.parent

sys.path.insert(0, str(root_dir))

from arxiv_dl.helpers import process_cvf_target
from arxiv_dl.models import PaperData


class TestProcessCVFTarget(unittest.TestCase):
    def test_CVPR2021(self):
        abs_url = "https://openaccess.thecvf.com/content/CVPR2021/html/Wu_Greedy_Hierarchical_Variational_Autoencoders_for_Large-Scale_Video_Prediction_CVPR_2021_paper.html"
        pdf_url = "https://openaccess.thecvf.com/content/CVPR2021/papers/Wu_Greedy_Hierarchical_Variational_Autoencoders_for_Large-Scale_Video_Prediction_CVPR_2021_paper.pdf"
        paper_data = process_cvf_target(abs_url)
        self.assertTrue(isinstance(paper_data, PaperData))
        self.assertEqual(paper_data.abs_url, abs_url)
        self.assertEqual(paper_data.pdf_url, pdf_url)
        paper_data = process_cvf_target(pdf_url)
        self.assertTrue(isinstance(paper_data, PaperData))
        self.assertEqual(paper_data.abs_url, abs_url)
        self.assertEqual(paper_data.pdf_url, pdf_url)

    def test_ICCV2021(self):
        abs_url = "https://openaccess.thecvf.com/content/ICCV2021/html/Shi_AdaSGN_Adapting_Joint_Number_and_Model_Size_for_Efficient_Skeleton-Based_ICCV_2021_paper.html"
        pdf_url = "https://openaccess.thecvf.com/content/ICCV2021/papers/Shi_AdaSGN_Adapting_Joint_Number_and_Model_Size_for_Efficient_Skeleton-Based_ICCV_2021_paper.pdf"
        paper_data = process_cvf_target(abs_url)
        self.assertTrue(isinstance(paper_data, PaperData))
        self.assertEqual(paper_data.abs_url, abs_url)
        self.assertEqual(paper_data.pdf_url, pdf_url)
        paper_data = process_cvf_target(pdf_url)
        self.assertTrue(isinstance(paper_data, PaperData))
        self.assertEqual(paper_data.abs_url, abs_url)
        self.assertEqual(paper_data.pdf_url, pdf_url)

    def test_CVPR2013(self):
        abs_url = "https://openaccess.thecvf.com/content_cvpr_2013/html/Kim_Deformable_Spatial_Pyramid_2013_CVPR_paper.html"
        pdf_url = "https://openaccess.thecvf.com/content_cvpr_2013/papers/Kim_Deformable_Spatial_Pyramid_2013_CVPR_paper.pdf"
        paper_data = process_cvf_target(abs_url)
        self.assertTrue(isinstance(paper_data, PaperData))
        self.assertEqual(paper_data.abs_url, abs_url)
        self.assertEqual(paper_data.pdf_url, pdf_url)
        paper_data = process_cvf_target(pdf_url)
        self.assertTrue(isinstance(paper_data, PaperData))
        self.assertEqual(paper_data.abs_url, abs_url)
        self.assertEqual(paper_data.pdf_url, pdf_url)
