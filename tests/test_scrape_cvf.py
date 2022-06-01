import sys
import unittest
from pathlib import Path

from arxiv_dl.helpers import process_cvf_target
from arxiv_dl.models import PaperData
from arxiv_dl.scrapers import scrape_metadata_cvf

root_dir = Path(__file__).resolve().parent.parent

sys.path.insert(0, str(root_dir))


class TestScrapeCVF(unittest.TestCase):
    def test_CVPR2021(self):
        abs_url = "https://openaccess.thecvf.com/content/CVPR2021/html/Wu_Greedy_Hierarchical_Variational_Autoencoders_for_Large-Scale_Video_Prediction_CVPR_2021_paper.html"
        pdf_url = "https://openaccess.thecvf.com/content/CVPR2021/papers/Wu_Greedy_Hierarchical_Variational_Autoencoders_for_Large-Scale_Video_Prediction_CVPR_2021_paper.pdf"
        supp_url = "https://openaccess.thecvf.com/content/CVPR2021/supplemental/Wu_Greedy_Hierarchical_Variational_CVPR_2021_supplemental.pdf"
        paper_data: PaperData = process_cvf_target(abs_url)
        scrape_metadata_cvf(paper_data)
        self.assertTrue(isinstance(paper_data, PaperData))
        self.assertEqual(paper_data.abs_url, abs_url)
        self.assertEqual(paper_data.pdf_url, pdf_url)
        # self.assertEqual(paper_data.supp_url, supp_url)
        self.assertEqual(paper_data.src_website, "CVF")
        self.assertEqual(
            paper_data.title,
            "Greedy Hierarchical Variational Autoencoders for Large-Scale Video Prediction",
        )
        self.assertEqual(paper_data.year, 2021)
        self.assertEqual(paper_data.paper_venue, "CVPR")
        self.assertEqual(
            paper_data.authors,
            [
                "Bohan Wu",
                "Suraj Nair",
                "Roberto Martin-Martin",
                "Li Fei-Fei",
                "Chelsea Finn",
            ],
        )
        self.assertEqual(
            paper_data.abstract,
            "A video prediction model that generalizes to diverse scenes would enable intelligent agents such as robots to perform a variety of tasks via planning with the model. However, while existing video prediction models have produced promising results on small datasets, they suffer from severe underfitting when trained on large and diverse datasets. To address this underfitting challenge, we first observe that the ability to train larger video prediction models is often bottlenecked by the memory constraints of GPUs or TPUs. In parallel, deep hierarchical latent variable models can produce higher quality predictions by capturing the multi-level stochasticity of future observations, but end-to-end optimization of such models is notably difficult. Our key insight is that greedy and modular optimization of hierarchical autoencoders can simultaneously address both the memory constraints and the optimization challenges of large-scale video prediction. We introduce Greedy Hierarchical Variational Autoencoders (GHVAEs), a method that learns high-fidelity video predictions by greedily training each level of a hierarchical autoencoder. In comparison to state-of-the-art models, GHVAEs provide 17-55% gains in prediction performance on four video datasets, a 35-40% higher success rate on real robot tasks, and can improve performance monotonically by simply adding more modules.",
        )

    def test_CVPR2021_again(self):
        abs_url = "https://openaccess.thecvf.com/content/CVPR2021/html/Xu_SUTD-TrafficQA_A_Question_Answering_Benchmark_and_an_Efficient_Network_for_CVPR_2021_paper.html"
        pdf_url = "https://openaccess.thecvf.com/content/CVPR2021/papers/Xu_SUTD-TrafficQA_A_Question_Answering_Benchmark_and_an_Efficient_Network_for_CVPR_2021_paper.pdf"
        supp_url = "https://openaccess.thecvf.com/content/CVPR2021/supplemental/Xu_SUTD-TrafficQA_A_Question_CVPR_2021_supplemental.pdf"
        paper_data: PaperData = process_cvf_target(abs_url)
        scrape_metadata_cvf(paper_data)
        self.assertTrue(isinstance(paper_data, PaperData))
        self.assertEqual(paper_data.abs_url, abs_url)
        self.assertEqual(paper_data.pdf_url, pdf_url)
        # self.assertEqual(paper_data.supp_url, supp_url)
        self.assertEqual(paper_data.src_website, "CVF")
        self.assertEqual(
            paper_data.title,
            "SUTD-TrafficQA: A Question Answering Benchmark and an Efficient Network for Video Reasoning Over Traffic Events",
        )
        self.assertEqual(paper_data.year, 2021)
        self.assertEqual(paper_data.paper_venue, "CVPR")
        self.assertEqual(paper_data.authors, ["Li Xu", "He Huang", "Jun Liu"])
        self.assertEqual(
            paper_data.abstract,
            "Traffic event cognition and reasoning in videos is an important task that has a wide range of applications in intelligent transportation, assisted driving, and autonomous vehicles. In this paper, we create a novel dataset, SUTD-TrafficQA (Traffic Question Answering), which takes the form of video QA based on the collected 10,080 in-the-wild videos and annotated 62,535 QA pairs, for benchmarking the cognitive capability of causal inference and event understanding models in complex traffic scenarios. Specifically, we propose 6 challenging reasoning tasks corresponding to various traffic scenarios, so as to evaluate the reasoning capability over different kinds of complex yet practical traffic events. Moreover, we propose Eclipse, a novel Efficient glimpse network via dynamic inference, in order to achieve computation-efficient and reliable video reasoning. The experiments show that our method achieves superior performance while reducing the computation cost significantly.",
        )
