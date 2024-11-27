import sys
import unittest
from pathlib import Path

from arxiv_dl.models import PaperData
from arxiv_dl.scrapers import scrape_metadata_cvf
from arxiv_dl.target_parser import process_cvf_target

root_dir = Path(__file__).resolve().parent.parent

sys.path.insert(0, str(root_dir))


class TestScrapeCVF(unittest.TestCase):
    def test_ICCV2023(self):
        abs_url = "https://openaccess.thecvf.com/content/CVPR2023/html/Xu_Meta_Compositional_Referring_Expression_Segmentation_CVPR_2023_paper.html"
        pdf_url = "https://openaccess.thecvf.com/content/CVPR2023/papers/Xu_Meta_Compositional_Referring_Expression_Segmentation_CVPR_2023_paper.pdf"
        paper_data = process_cvf_target(abs_url)
        scrape_metadata_cvf(paper_data)
        ...

    def test_CVPR2023(self):
        abs_url = "https://openaccess.thecvf.com/content/CVPR2023/html/Xu_Meta_Compositional_Referring_Expression_Segmentation_CVPR_2023_paper.html"
        pdf_url = "https://openaccess.thecvf.com/content/CVPR2023/papers/Xu_Meta_Compositional_Referring_Expression_Segmentation_CVPR_2023_paper.pdf"
        paper_title = "Meta Compositional Referring Expression Segmentation"
        paper_data = process_cvf_target(abs_url)
        scrape_metadata_cvf(paper_data)
        self.assertTrue(isinstance(paper_data, PaperData))
        self.assertEqual(paper_data.abs_url, abs_url)
        self.assertEqual(paper_data.pdf_url, pdf_url)
        self.assertEqual(paper_data.src_website, "CVF")
        self.assertEqual(paper_data.title, paper_title)
        self.assertEqual(paper_data.year, 2023)
        self.assertEqual(paper_data.paper_venue, "CVPR")
        self.assertEqual(
            paper_data.authors,
            [
                "Li Xu",
                "Mark He Huang",
                "Xindi Shang",
                "Zehuan Yuan",
                "Ying Sun",
                "Jun Liu",
            ],
        )

    def test_WACV2023(self):
        abs_url = "https://openaccess.thecvf.com/content/WACV2023/html/Qiu_3D_Change_Localization_and_Captioning_From_Dynamic_Scans_of_Indoor_WACV_2023_paper.html"
        pdf_url = "https://openaccess.thecvf.com/content/WACV2023/papers/Qiu_3D_Change_Localization_and_Captioning_From_Dynamic_Scans_of_Indoor_WACV_2023_paper.pdf"
        paper_data = process_cvf_target(abs_url)
        scrape_metadata_cvf(paper_data)
        ...

    def test_CVPR2022(self):
        abs_url = "https://openaccess.thecvf.com/content/CVPR2022/html/Granot_Drop_the_GAN_In_Defense_of_Patches_Nearest_Neighbors_As_CVPR_2022_paper.html"
        pdf_url = "https://openaccess.thecvf.com/content/CVPR2022/papers/Granot_Drop_the_GAN_In_Defense_of_Patches_Nearest_Neighbors_As_CVPR_2022_paper.pdf"
        paper_data = process_cvf_target(abs_url)
        scrape_metadata_cvf(paper_data)
        ...

    def test_CVPR2022W(self):
        abs_url = "https://openaccess.thecvf.com/content/CVPR2022W/WAD/html/Zheng_Multi-Modal_3D_Human_Pose_Estimation_With_2D_Weak_Supervision_in_CVPRW_2022_paper.html"
        pdf_url = "https://openaccess.thecvf.com/content/CVPR2022W/WAD/papers/Zheng_Multi-Modal_3D_Human_Pose_Estimation_With_2D_Weak_Supervision_in_CVPRW_2022_paper.pdf"
        paper_data = process_cvf_target(abs_url)
        scrape_metadata_cvf(paper_data)
        ...

    def test_WACV2022(self):
        abs_url = "https://openaccess.thecvf.com/content/WACV2022/html/Agarwal_Does_Data_Repair_Lead_to_Fair_Models_Curating_Contextually_Fair_WACV_2022_paper.html"
        pdf_url = "https://openaccess.thecvf.com/content/WACV2022/papers/Agarwal_Does_Data_Repair_Lead_to_Fair_Models_Curating_Contextually_Fair_WACV_2022_paper.pdf"
        paper_data = process_cvf_target(abs_url)
        scrape_metadata_cvf(paper_data)
        ...

    def test_WACV2022W(self):
        abs_url = "https://openaccess.thecvf.com/content/WACV2022W/VAQ/html/Mastan_DILIE_Deep_Internal_Learning_for_Image_Enhancement_WACVW_2022_paper.html"
        pdf_url = "https://openaccess.thecvf.com/content/WACV2022W/VAQ/papers/Mastan_DILIE_Deep_Internal_Learning_for_Image_Enhancement_WACVW_2022_paper.pdf"
        paper_data = process_cvf_target(abs_url)
        scrape_metadata_cvf(paper_data)
        ...

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

    def test_CVPR2021W(self):
        abs_url = "https://openaccess.thecvf.com/content/CVPR2021W/JRDB/html/He_Know_Your_Surroundings_Panoramic_Multi-Object_Tracking_by_Multimodality_Collaboration_CVPRW_2021_paper.html"
        pdf_url = "https://openaccess.thecvf.com/content/CVPR2021W/JRDB/papers/He_Know_Your_Surroundings_Panoramic_Multi-Object_Tracking_by_Multimodality_Collaboration_CVPRW_2021_paper.pdf"
        paper_data = process_cvf_target(abs_url)
        scrape_metadata_cvf(paper_data)
        ...

    def test_ICCV2021(self):
        abs_url = "https://openaccess.thecvf.com/content/ICCV2021/html/Shi_AdaSGN_Adapting_Joint_Number_and_Model_Size_for_Efficient_Skeleton-Based_ICCV_2021_paper.html"
        pdf_url = "https://openaccess.thecvf.com/content/ICCV2021/papers/Shi_AdaSGN_Adapting_Joint_Number_and_Model_Size_for_Efficient_Skeleton-Based_ICCV_2021_paper.pdf"
        paper_data = process_cvf_target(abs_url)
        scrape_metadata_cvf(paper_data)
        ...

    def test_ICCV2021W(self):
        abs_url = "https://openaccess.thecvf.com/content/ICCV2021W/MMVRA/html/Peng_The_Multi-Modal_Video_Reasoning_and_Analyzing_Competition_ICCVW_2021_paper.html"
        pdf_url = "https://openaccess.thecvf.com/content/ICCV2021W/MMVRA/papers/Peng_The_Multi-Modal_Video_Reasoning_and_Analyzing_Competition_ICCVW_2021_paper.pdf"
        paper_data = process_cvf_target(abs_url)
        scrape_metadata_cvf(paper_data)
        ...

    def test_WACV2021(self):
        abs_url = "https://openaccess.thecvf.com/content/WACV2021/html/Fortin_Towards_Contextual_Learning_in_Few-Shot_Object_Classification_WACV_2021_paper.html"
        pdf_url = "https://openaccess.thecvf.com/content/WACV2021/papers/Fortin_Towards_Contextual_Learning_in_Few-Shot_Object_Classification_WACV_2021_paper.pdf"
        paper_data = process_cvf_target(abs_url)
        scrape_metadata_cvf(paper_data)
        ...

    def test_WACV2021W(self):
        abs_url = "https://openaccess.thecvf.com/content/WACV2021W/HADCV/html/Godil_2020_Sequestered_Data_Evaluation_for_Known_Activities_in_Extended_Video_WACVW_2021_paper.html"
        pdf_url = "https://openaccess.thecvf.com/content/WACV2021W/HADCV/papers/Godil_2020_Sequestered_Data_Evaluation_for_Known_Activities_in_Extended_Video_WACVW_2021_paper.pdf"
        paper_data = process_cvf_target(abs_url)
        scrape_metadata_cvf(paper_data)
        ...

    def test_CVPR2020(self):
        abs_url = "https://openaccess.thecvf.com/content_CVPR_2020/html/Qin_Forward_and_Backward_Information_Retention_for_Accurate_Binary_Neural_Networks_CVPR_2020_paper.html"
        pdf_url = "https://openaccess.thecvf.com/content_CVPR_2020/papers/Qin_Forward_and_Backward_Information_Retention_for_Accurate_Binary_Neural_Networks_CVPR_2020_paper.pdf"
        paper_data = process_cvf_target(abs_url)
        scrape_metadata_cvf(paper_data)
        ...

    def test_CVPR2020W(self):
        abs_url = "https://openaccess.thecvf.com/content_CVPRW_2020/html/w54/He_Image2Audio_Facilitating_Semi-Supervised_Audio_Emotion_Recognition_With_Facial_Expression_Image_CVPRW_2020_paper.html"
        pdf_url = "https://openaccess.thecvf.com/content_CVPRW_2020/papers/w54/He_Image2Audio_Facilitating_Semi-Supervised_Audio_Emotion_Recognition_With_Facial_Expression_Image_CVPRW_2020_paper.pdf"
        paper_data = process_cvf_target(abs_url)
        scrape_metadata_cvf(paper_data)
        ...

    def test_WACV2020(self):
        abs_url = "https://openaccess.thecvf.com/content_WACV_2020/html/Sang_Inferring_Super-Resolution_Depth_from_a_Moving_Light-Source_Enhanced_RGB-D_Sensor_WACV_2020_paper.html"
        pdf_url = "https://openaccess.thecvf.com/content_WACV_2020/papers/Sang_Inferring_Super-Resolution_Depth_from_a_Moving_Light-Source_Enhanced_RGB-D_Sensor_WACV_2020_paper.pdf"
        paper_data = process_cvf_target(abs_url)
        scrape_metadata_cvf(paper_data)
        ...

    def test_WACV2020W(self):
        abs_url = "https://openaccess.thecvf.com/content_WACVW_2020/html/w1/Albiero_Analysis_of_Gender_Inequality_In_Face_Recognition_Accuracy_WACVW_2020_paper.html"
        pdf_url = "https://openaccess.thecvf.com/content_WACVW_2020/papers/w1/Albiero_Analysis_of_Gender_Inequality_In_Face_Recognition_Accuracy_WACVW_2020_paper.pdf"
        paper_data = process_cvf_target(abs_url)
        scrape_metadata_cvf(paper_data)
        ...

    def test_CVPR2019(self):
        abs_url = "https://openaccess.thecvf.com/content_CVPR_2019/html/Li_Finding_Task-Relevant_Features_for_Few-Shot_Learning_by_Category_Traversal_CVPR_2019_paper.html"
        pdf_url = "https://openaccess.thecvf.com/content_CVPR_2019/papers/Li_Finding_Task-Relevant_Features_for_Few-Shot_Learning_by_Category_Traversal_CVPR_2019_paper.pdf"
        paper_data = process_cvf_target(abs_url)
        scrape_metadata_cvf(paper_data)
        ...

    def test_CVPR2019W(self):
        abs_url = "https://openaccess.thecvf.com/content_CVPRW_2019/html/BCMCVAI/Jourdan_A_Probabilistic_Model_of_the_Bitcoin_Blockchain_CVPRW_2019_paper.html"
        pdf_url = "https://openaccess.thecvf.com/content_CVPRW_2019/papers/BCMCVAI/Jourdan_A_Probabilistic_Model_of_the_Bitcoin_Blockchain_CVPRW_2019_paper.pdf"
        paper_data = process_cvf_target(abs_url)
        scrape_metadata_cvf(paper_data)
        ...

    def test_ICCV2019(self):
        abs_url = "https://openaccess.thecvf.com/content_ICCV_2019/html/Rossler_FaceForensics_Learning_to_Detect_Manipulated_Facial_Images_ICCV_2019_paper.html"
        pdf_url = "https://openaccess.thecvf.com/content_ICCV_2019/papers/Rossler_FaceForensics_Learning_to_Detect_Manipulated_Facial_Images_ICCV_2019_paper.pdf"
        paper_data = process_cvf_target(abs_url)
        scrape_metadata_cvf(paper_data)
        ...

    def test_ICCV2019W(self):
        abs_url = "https://openaccess.thecvf.com/content_ICCVW_2019/html/VISDrone/Zhang_How_to_Fully_Exploit_The_Abilities_of_Aerial_Image_Detectors_ICCVW_2019_paper.html"
        pdf_url = "https://openaccess.thecvf.com/content_ICCVW_2019/papers/VISDrone/Zhang_How_to_Fully_Exploit_The_Abilities_of_Aerial_Image_Detectors_ICCVW_2019_paper.pdf"
        paper_data = process_cvf_target(abs_url)
        scrape_metadata_cvf(paper_data)
        ...
