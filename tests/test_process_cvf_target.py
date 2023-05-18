import sys
import unittest
from pathlib import Path

from arxiv_dl.helpers import process_cvf_target
from arxiv_dl.models import PaperData

root_dir = Path(__file__).resolve().parent.parent

sys.path.insert(0, str(root_dir))


class TestProcessCVFTarget(unittest.TestCase):

    ################################################################
    # 2023
    # content/venue

    def test_CVPR2023(self):
        abs_url = "https://openaccess.thecvf.com/content/CVPR2023/html/Xu_Meta_Compositional_Referring_Expression_Segmentation_CVPR_2023_paper.html"
        pdf_url = "https://openaccess.thecvf.com/content/CVPR2023/papers/Xu_Meta_Compositional_Referring_Expression_Segmentation_CVPR_2023_paper.pdf"
        paper_data = process_cvf_target(abs_url)
        self.assertTrue(isinstance(paper_data, PaperData))
        self.assertEqual(paper_data.abs_url, abs_url)
        self.assertEqual(paper_data.pdf_url, pdf_url)
        self.assertEqual(paper_data.paper_venue, "CVPR")
        self.assertEqual(paper_data.year, 2023)
        paper_data = process_cvf_target(pdf_url)
        self.assertTrue(isinstance(paper_data, PaperData))
        self.assertEqual(paper_data.abs_url, abs_url)
        self.assertEqual(paper_data.pdf_url, pdf_url)
        self.assertEqual(paper_data.paper_venue, "CVPR")
        self.assertEqual(paper_data.year, 2023)

    def test_WACV2023(self):
        abs_url = "https://openaccess.thecvf.com/content/WACV2023/html/Kundu_FLOAT_Fast_Learnable_Once-for-All_Adversarial_Training_for_Tunable_Trade-Off_Between_WACV_2023_paper.html"
        pdf_url = "https://openaccess.thecvf.com/content/WACV2023/papers/Kundu_FLOAT_Fast_Learnable_Once-for-All_Adversarial_Training_for_Tunable_Trade-Off_Between_WACV_2023_paper.pdf"
        paper_data = process_cvf_target(abs_url)
        self.assertTrue(isinstance(paper_data, PaperData))
        self.assertEqual(paper_data.abs_url, abs_url)
        self.assertEqual(paper_data.pdf_url, pdf_url)
        self.assertEqual(paper_data.paper_venue, "WACV")
        self.assertEqual(paper_data.year, 2023)
        paper_data = process_cvf_target(pdf_url)
        self.assertTrue(isinstance(paper_data, PaperData))
        self.assertEqual(paper_data.abs_url, abs_url)
        self.assertEqual(paper_data.pdf_url, pdf_url)
        self.assertEqual(paper_data.paper_venue, "WACV")
        self.assertEqual(paper_data.year, 2023)

    ################################################################
    # 2022
    # content/venue
    # workshop: content/venue/workshop_name/html/
    # workshop: content/venue/workshop_name/papers/

    def test_CVPR2022(self):
        abs_url = "https://openaccess.thecvf.com/content/CVPR2022/html/Granot_Drop_the_GAN_In_Defense_of_Patches_Nearest_Neighbors_As_CVPR_2022_paper.html"
        pdf_url = "https://openaccess.thecvf.com/content/CVPR2022/papers/Granot_Drop_the_GAN_In_Defense_of_Patches_Nearest_Neighbors_As_CVPR_2022_paper.pdf"
        paper_data = process_cvf_target(abs_url)
        self.assertTrue(isinstance(paper_data, PaperData))
        self.assertEqual(paper_data.abs_url, abs_url)
        self.assertEqual(paper_data.pdf_url, pdf_url)
        self.assertEqual(paper_data.paper_venue, "CVPR")
        self.assertEqual(paper_data.year, 2022)
        paper_data = process_cvf_target(pdf_url)
        self.assertTrue(isinstance(paper_data, PaperData))
        self.assertEqual(paper_data.abs_url, abs_url)
        self.assertEqual(paper_data.pdf_url, pdf_url)
        self.assertEqual(paper_data.paper_venue, "CVPR")
        self.assertEqual(paper_data.year, 2022)

    def test_CVPR2022W(self):
        abs_url = "https://openaccess.thecvf.com/content/CVPR2022W/WAD/html/Zheng_Multi-Modal_3D_Human_Pose_Estimation_With_2D_Weak_Supervision_in_CVPRW_2022_paper.html"
        pdf_url = "https://openaccess.thecvf.com/content/CVPR2022W/WAD/papers/Zheng_Multi-Modal_3D_Human_Pose_Estimation_With_2D_Weak_Supervision_in_CVPRW_2022_paper.pdf"
        paper_data = process_cvf_target(abs_url)
        self.assertTrue(isinstance(paper_data, PaperData))
        self.assertEqual(paper_data.abs_url, abs_url)
        self.assertEqual(paper_data.pdf_url, pdf_url)
        self.assertEqual(paper_data.paper_venue, "CVPR_Workshops")
        self.assertEqual(paper_data.year, 2022)
        paper_data = process_cvf_target(pdf_url)
        self.assertTrue(isinstance(paper_data, PaperData))
        self.assertEqual(paper_data.abs_url, abs_url)
        self.assertEqual(paper_data.pdf_url, pdf_url)
        self.assertEqual(paper_data.paper_venue, "CVPR_Workshops")
        self.assertEqual(paper_data.year, 2022)

    def test_WACV2022(self):
        abs_url = "https://openaccess.thecvf.com/content/WACV2022/html/Agarwal_Does_Data_Repair_Lead_to_Fair_Models_Curating_Contextually_Fair_WACV_2022_paper.html"
        pdf_url = "https://openaccess.thecvf.com/content/WACV2022/papers/Agarwal_Does_Data_Repair_Lead_to_Fair_Models_Curating_Contextually_Fair_WACV_2022_paper.pdf"
        paper_data = process_cvf_target(abs_url)
        self.assertTrue(isinstance(paper_data, PaperData))
        self.assertEqual(paper_data.abs_url, abs_url)
        self.assertEqual(paper_data.pdf_url, pdf_url)
        self.assertEqual(paper_data.paper_venue, "WACV")
        self.assertEqual(paper_data.year, 2022)
        paper_data = process_cvf_target(pdf_url)
        self.assertTrue(isinstance(paper_data, PaperData))
        self.assertEqual(paper_data.abs_url, abs_url)
        self.assertEqual(paper_data.pdf_url, pdf_url)
        self.assertEqual(paper_data.paper_venue, "WACV")
        self.assertEqual(paper_data.year, 2022)

    def test_WACV2022W(self):
        abs_url = "https://openaccess.thecvf.com/content/WACV2022W/VAQ/html/Mastan_DILIE_Deep_Internal_Learning_for_Image_Enhancement_WACVW_2022_paper.html"
        pdf_url = "https://openaccess.thecvf.com/content/WACV2022W/VAQ/papers/Mastan_DILIE_Deep_Internal_Learning_for_Image_Enhancement_WACVW_2022_paper.pdf"
        paper_data = process_cvf_target(abs_url)
        self.assertTrue(isinstance(paper_data, PaperData))
        self.assertEqual(paper_data.abs_url, abs_url)
        self.assertEqual(paper_data.pdf_url, pdf_url)
        self.assertEqual(paper_data.paper_venue, "WACV_Workshops")
        self.assertEqual(paper_data.year, 2022)
        paper_data = process_cvf_target(pdf_url)
        self.assertTrue(isinstance(paper_data, PaperData))
        self.assertEqual(paper_data.abs_url, abs_url)
        self.assertEqual(paper_data.pdf_url, pdf_url)
        self.assertEqual(paper_data.paper_venue, "WACV_Workshops")
        self.assertEqual(paper_data.year, 2022)

    ################################################################
    # 2021
    # content/venue
    # workshop: content/venue/workshop_name/html/
    # workshop: content/venue/workshop_name/papers/

    def test_CVPR2021(self):
        abs_url = "https://openaccess.thecvf.com/content/CVPR2021/html/Wu_Greedy_Hierarchical_Variational_Autoencoders_for_Large-Scale_Video_Prediction_CVPR_2021_paper.html"
        pdf_url = "https://openaccess.thecvf.com/content/CVPR2021/papers/Wu_Greedy_Hierarchical_Variational_Autoencoders_for_Large-Scale_Video_Prediction_CVPR_2021_paper.pdf"
        paper_data = process_cvf_target(abs_url)
        self.assertTrue(isinstance(paper_data, PaperData))
        self.assertEqual(paper_data.abs_url, abs_url)
        self.assertEqual(paper_data.pdf_url, pdf_url)
        self.assertEqual(paper_data.paper_venue, "CVPR")
        self.assertEqual(paper_data.year, 2021)
        paper_data = process_cvf_target(pdf_url)
        self.assertTrue(isinstance(paper_data, PaperData))
        self.assertEqual(paper_data.abs_url, abs_url)
        self.assertEqual(paper_data.pdf_url, pdf_url)
        self.assertEqual(paper_data.paper_venue, "CVPR")
        self.assertEqual(paper_data.year, 2021)

    def test_CVPR2021W(self):
        abs_url = "https://openaccess.thecvf.com/content/CVPR2021W/JRDB/html/He_Know_Your_Surroundings_Panoramic_Multi-Object_Tracking_by_Multimodality_Collaboration_CVPRW_2021_paper.html"
        pdf_url = "https://openaccess.thecvf.com/content/CVPR2021W/JRDB/papers/He_Know_Your_Surroundings_Panoramic_Multi-Object_Tracking_by_Multimodality_Collaboration_CVPRW_2021_paper.pdf"
        paper_data = process_cvf_target(abs_url)
        self.assertTrue(isinstance(paper_data, PaperData))
        self.assertEqual(paper_data.abs_url, abs_url)
        self.assertEqual(paper_data.pdf_url, pdf_url)
        self.assertEqual(paper_data.paper_venue, "CVPR_Workshops")
        self.assertEqual(paper_data.year, 2021)
        paper_data = process_cvf_target(pdf_url)
        self.assertTrue(isinstance(paper_data, PaperData))
        self.assertEqual(paper_data.abs_url, abs_url)
        self.assertEqual(paper_data.pdf_url, pdf_url)
        self.assertEqual(paper_data.paper_venue, "CVPR_Workshops")
        self.assertEqual(paper_data.year, 2021)

    def test_ICCV2021(self):
        abs_url = "https://openaccess.thecvf.com/content/ICCV2021/html/Shi_AdaSGN_Adapting_Joint_Number_and_Model_Size_for_Efficient_Skeleton-Based_ICCV_2021_paper.html"
        pdf_url = "https://openaccess.thecvf.com/content/ICCV2021/papers/Shi_AdaSGN_Adapting_Joint_Number_and_Model_Size_for_Efficient_Skeleton-Based_ICCV_2021_paper.pdf"
        paper_data = process_cvf_target(abs_url)
        self.assertTrue(isinstance(paper_data, PaperData))
        self.assertEqual(paper_data.abs_url, abs_url)
        self.assertEqual(paper_data.pdf_url, pdf_url)
        self.assertEqual(paper_data.paper_venue, "ICCV")
        self.assertEqual(paper_data.year, 2021)
        paper_data = process_cvf_target(pdf_url)
        self.assertTrue(isinstance(paper_data, PaperData))
        self.assertEqual(paper_data.abs_url, abs_url)
        self.assertEqual(paper_data.pdf_url, pdf_url)
        self.assertEqual(paper_data.paper_venue, "ICCV")
        self.assertEqual(paper_data.year, 2021)

    def test_ICCV2021W(self):
        abs_url = "https://openaccess.thecvf.com/content/ICCV2021W/MMVRA/html/Peng_The_Multi-Modal_Video_Reasoning_and_Analyzing_Competition_ICCVW_2021_paper.html"
        pdf_url = "https://openaccess.thecvf.com/content/ICCV2021W/MMVRA/papers/Peng_The_Multi-Modal_Video_Reasoning_and_Analyzing_Competition_ICCVW_2021_paper.pdf"
        paper_data = process_cvf_target(abs_url)
        self.assertTrue(isinstance(paper_data, PaperData))
        self.assertEqual(paper_data.abs_url, abs_url)
        self.assertEqual(paper_data.pdf_url, pdf_url)
        self.assertEqual(paper_data.paper_venue, "ICCV_Workshops")
        self.assertEqual(paper_data.year, 2021)
        paper_data = process_cvf_target(pdf_url)
        self.assertTrue(isinstance(paper_data, PaperData))
        self.assertEqual(paper_data.abs_url, abs_url)
        self.assertEqual(paper_data.pdf_url, pdf_url)
        self.assertEqual(paper_data.paper_venue, "ICCV_Workshops")
        self.assertEqual(paper_data.year, 2021)

    def test_WACV2021(self):
        abs_url = "https://openaccess.thecvf.com/content/WACV2021/html/Fortin_Towards_Contextual_Learning_in_Few-Shot_Object_Classification_WACV_2021_paper.html"
        pdf_url = "https://openaccess.thecvf.com/content/WACV2021/papers/Fortin_Towards_Contextual_Learning_in_Few-Shot_Object_Classification_WACV_2021_paper.pdf"
        paper_data = process_cvf_target(abs_url)
        self.assertTrue(isinstance(paper_data, PaperData))
        self.assertEqual(paper_data.abs_url, abs_url)
        self.assertEqual(paper_data.pdf_url, pdf_url)
        self.assertEqual(paper_data.paper_venue, "WACV")
        self.assertEqual(paper_data.year, 2021)
        paper_data = process_cvf_target(pdf_url)
        self.assertTrue(isinstance(paper_data, PaperData))
        self.assertEqual(paper_data.abs_url, abs_url)
        self.assertEqual(paper_data.pdf_url, pdf_url)
        self.assertEqual(paper_data.paper_venue, "WACV")
        self.assertEqual(paper_data.year, 2021)

    def test_WACV2021W(self):
        abs_url = "https://openaccess.thecvf.com/content/WACV2021W/HADCV/html/Godil_2020_Sequestered_Data_Evaluation_for_Known_Activities_in_Extended_Video_WACVW_2021_paper.html"
        pdf_url = "https://openaccess.thecvf.com/content/WACV2021W/HADCV/papers/Godil_2020_Sequestered_Data_Evaluation_for_Known_Activities_in_Extended_Video_WACVW_2021_paper.pdf"
        paper_data = process_cvf_target(abs_url)
        self.assertTrue(isinstance(paper_data, PaperData))
        self.assertEqual(paper_data.abs_url, abs_url)
        self.assertEqual(paper_data.pdf_url, pdf_url)
        self.assertEqual(paper_data.paper_venue, "WACV_Workshops")
        self.assertEqual(paper_data.year, 2021)
        paper_data = process_cvf_target(pdf_url)
        self.assertTrue(isinstance(paper_data, PaperData))
        self.assertEqual(paper_data.abs_url, abs_url)
        self.assertEqual(paper_data.pdf_url, pdf_url)
        self.assertEqual(paper_data.paper_venue, "WACV_Workshops")
        self.assertEqual(paper_data.year, 2021)

    ################################################################
    # 2020
    # content_venue/
    # workshop: html/workshop_name
    # workshop: papers/workshop_name

    def test_CVPR2020(self):
        abs_url = "https://openaccess.thecvf.com/content_CVPR_2020/html/Qin_Forward_and_Backward_Information_Retention_for_Accurate_Binary_Neural_Networks_CVPR_2020_paper.html"
        pdf_url = "https://openaccess.thecvf.com/content_CVPR_2020/papers/Qin_Forward_and_Backward_Information_Retention_for_Accurate_Binary_Neural_Networks_CVPR_2020_paper.pdf"
        paper_data = process_cvf_target(abs_url)
        self.assertTrue(isinstance(paper_data, PaperData))
        self.assertEqual(paper_data.abs_url, abs_url)
        self.assertEqual(paper_data.pdf_url, pdf_url)
        self.assertEqual(paper_data.paper_venue, "CVPR")
        self.assertEqual(paper_data.year, 2020)
        paper_data = process_cvf_target(pdf_url)
        self.assertTrue(isinstance(paper_data, PaperData))
        self.assertEqual(paper_data.abs_url, abs_url)
        self.assertEqual(paper_data.pdf_url, pdf_url)
        self.assertEqual(paper_data.paper_venue, "CVPR")
        self.assertEqual(paper_data.year, 2020)

    def test_CVPR2020W(self):
        abs_url = "https://openaccess.thecvf.com/content_CVPRW_2020/html/w54/He_Image2Audio_Facilitating_Semi-Supervised_Audio_Emotion_Recognition_With_Facial_Expression_Image_CVPRW_2020_paper.html"
        pdf_url = "https://openaccess.thecvf.com/content_CVPRW_2020/papers/w54/He_Image2Audio_Facilitating_Semi-Supervised_Audio_Emotion_Recognition_With_Facial_Expression_Image_CVPRW_2020_paper.pdf"
        paper_data = process_cvf_target(abs_url)
        self.assertTrue(isinstance(paper_data, PaperData))
        self.assertEqual(paper_data.abs_url, abs_url)
        self.assertEqual(paper_data.pdf_url, pdf_url)
        self.assertEqual(paper_data.paper_venue, "CVPR_Workshops")
        self.assertEqual(paper_data.year, 2020)
        paper_data = process_cvf_target(pdf_url)
        self.assertTrue(isinstance(paper_data, PaperData))
        self.assertEqual(paper_data.abs_url, abs_url)
        self.assertEqual(paper_data.pdf_url, pdf_url)
        self.assertEqual(paper_data.paper_venue, "CVPR_Workshops")
        self.assertEqual(paper_data.year, 2020)

    def test_WACV2020(self):
        abs_url = "https://openaccess.thecvf.com/content_WACV_2020/html/Sang_Inferring_Super-Resolution_Depth_from_a_Moving_Light-Source_Enhanced_RGB-D_Sensor_WACV_2020_paper.html"
        pdf_url = "https://openaccess.thecvf.com/content_WACV_2020/papers/Sang_Inferring_Super-Resolution_Depth_from_a_Moving_Light-Source_Enhanced_RGB-D_Sensor_WACV_2020_paper.pdf"
        paper_data = process_cvf_target(abs_url)
        self.assertTrue(isinstance(paper_data, PaperData))
        self.assertEqual(paper_data.abs_url, abs_url)
        self.assertEqual(paper_data.pdf_url, pdf_url)
        self.assertEqual(paper_data.paper_venue, "WACV")
        self.assertEqual(paper_data.year, 2020)
        paper_data = process_cvf_target(pdf_url)
        self.assertTrue(isinstance(paper_data, PaperData))
        self.assertEqual(paper_data.abs_url, abs_url)
        self.assertEqual(paper_data.pdf_url, pdf_url)
        self.assertEqual(paper_data.paper_venue, "WACV")
        self.assertEqual(paper_data.year, 2020)

    def test_WACV2020W(self):
        abs_url = "https://openaccess.thecvf.com/content_WACVW_2020/html/w1/Albiero_Analysis_of_Gender_Inequality_In_Face_Recognition_Accuracy_WACVW_2020_paper.html"
        pdf_url = "https://openaccess.thecvf.com/content_WACVW_2020/papers/w1/Albiero_Analysis_of_Gender_Inequality_In_Face_Recognition_Accuracy_WACVW_2020_paper.pdf"
        paper_data = process_cvf_target(abs_url)
        self.assertTrue(isinstance(paper_data, PaperData))
        self.assertEqual(paper_data.abs_url, abs_url)
        self.assertEqual(paper_data.pdf_url, pdf_url)
        self.assertEqual(paper_data.paper_venue, "WACV_Workshops")
        self.assertEqual(paper_data.year, 2020)
        paper_data = process_cvf_target(pdf_url)
        self.assertTrue(isinstance(paper_data, PaperData))
        self.assertEqual(paper_data.abs_url, abs_url)
        self.assertEqual(paper_data.pdf_url, pdf_url)
        self.assertEqual(paper_data.paper_venue, "WACV_Workshops")
        self.assertEqual(paper_data.year, 2020)

    ################################################################
    # 2019
    # workshop: html/workshop_name
    # workshop: papers/workshop_name

    def test_CVPR2019(self):
        abs_url = "https://openaccess.thecvf.com/content_CVPR_2019/html/Li_Finding_Task-Relevant_Features_for_Few-Shot_Learning_by_Category_Traversal_CVPR_2019_paper.html"
        pdf_url = "https://openaccess.thecvf.com/content_CVPR_2019/papers/Li_Finding_Task-Relevant_Features_for_Few-Shot_Learning_by_Category_Traversal_CVPR_2019_paper.pdf"
        paper_data = process_cvf_target(abs_url)
        self.assertTrue(isinstance(paper_data, PaperData))
        self.assertEqual(paper_data.abs_url, abs_url)
        self.assertEqual(paper_data.pdf_url, pdf_url)
        self.assertEqual(paper_data.paper_venue, "CVPR")
        self.assertEqual(paper_data.year, 2019)
        paper_data = process_cvf_target(pdf_url)
        self.assertTrue(isinstance(paper_data, PaperData))
        self.assertEqual(paper_data.abs_url, abs_url)
        self.assertEqual(paper_data.pdf_url, pdf_url)
        self.assertEqual(paper_data.paper_venue, "CVPR")
        self.assertEqual(paper_data.year, 2019)

    def test_CVPR2019W(self):
        # NOTE: strange pdf url
        abs_url = "https://openaccess.thecvf.com/content_CVPRW_2019/html/BCMCVAI/Jourdan_A_Probabilistic_Model_of_the_Bitcoin_Blockchain_CVPRW_2019_paper.html"
        pdf_url = "https://openaccess.thecvf.com/content_CVPRW_2019/papers/BCMCVAI/Jourdan_A_Probabilistic_Model_of_the_Bitcoin_Blockchain_CVPRW_2019_paper.pdf"
        paper_data = process_cvf_target(abs_url)
        self.assertTrue(isinstance(paper_data, PaperData))
        self.assertEqual(paper_data.abs_url, abs_url)
        self.assertEqual(paper_data.pdf_url, pdf_url)
        self.assertEqual(paper_data.paper_venue, "CVPR_Workshops")
        self.assertEqual(paper_data.year, 2019)
        paper_data = process_cvf_target(pdf_url)
        self.assertTrue(isinstance(paper_data, PaperData))
        self.assertEqual(paper_data.abs_url, abs_url)
        self.assertEqual(paper_data.pdf_url, pdf_url)
        self.assertEqual(paper_data.paper_venue, "CVPR_Workshops")
        self.assertEqual(paper_data.year, 2019)

    def test_ICCV2019(self):
        abs_url = "https://openaccess.thecvf.com/content_ICCV_2019/html/Rossler_FaceForensics_Learning_to_Detect_Manipulated_Facial_Images_ICCV_2019_paper.html"
        pdf_url = "https://openaccess.thecvf.com/content_ICCV_2019/papers/Rossler_FaceForensics_Learning_to_Detect_Manipulated_Facial_Images_ICCV_2019_paper.pdf"
        paper_data = process_cvf_target(abs_url)
        self.assertTrue(isinstance(paper_data, PaperData))
        self.assertEqual(paper_data.abs_url, abs_url)
        self.assertEqual(paper_data.pdf_url, pdf_url)
        self.assertEqual(paper_data.paper_venue, "ICCV")
        self.assertEqual(paper_data.year, 2019)
        paper_data = process_cvf_target(pdf_url)
        self.assertTrue(isinstance(paper_data, PaperData))
        self.assertEqual(paper_data.abs_url, abs_url)
        self.assertEqual(paper_data.pdf_url, pdf_url)
        self.assertEqual(paper_data.paper_venue, "ICCV")
        self.assertEqual(paper_data.year, 2019)

    def test_ICCV2019W(self):
        abs_url = "https://openaccess.thecvf.com/content_ICCVW_2019/html/VISDrone/Zhang_How_to_Fully_Exploit_The_Abilities_of_Aerial_Image_Detectors_ICCVW_2019_paper.html"
        pdf_url = "https://openaccess.thecvf.com/content_ICCVW_2019/papers/VISDrone/Zhang_How_to_Fully_Exploit_The_Abilities_of_Aerial_Image_Detectors_ICCVW_2019_paper.pdf"
        paper_data = process_cvf_target(abs_url)
        self.assertTrue(isinstance(paper_data, PaperData))
        self.assertEqual(paper_data.abs_url, abs_url)
        self.assertEqual(paper_data.pdf_url, pdf_url)
        self.assertEqual(paper_data.paper_venue, "ICCV_Workshops")
        self.assertEqual(paper_data.year, 2019)
        paper_data = process_cvf_target(pdf_url)
        self.assertTrue(isinstance(paper_data, PaperData))
        self.assertEqual(paper_data.abs_url, abs_url)
        self.assertEqual(paper_data.pdf_url, pdf_url)
        self.assertEqual(paper_data.paper_venue, "ICCV_Workshops")
        self.assertEqual(paper_data.year, 2019)

    ################################################################
    # 2018
    # workshop: workshop_name/html
    # workshop: papers/workshop_name

    def test_CVPR2018(self):
        abs_url = "https://openaccess.thecvf.com/content_cvpr_2018/html/Das_Embodied_Question_Answering_CVPR_2018_paper.html"
        pdf_url = "https://openaccess.thecvf.com/content_cvpr_2018/papers/Das_Embodied_Question_Answering_CVPR_2018_paper.pdf"
        paper_data = process_cvf_target(abs_url)
        self.assertTrue(isinstance(paper_data, PaperData))
        self.assertEqual(paper_data.abs_url, abs_url)
        self.assertEqual(paper_data.pdf_url, pdf_url)
        self.assertEqual(paper_data.paper_venue, "CVPR")
        self.assertEqual(paper_data.year, 2018)
        paper_data = process_cvf_target(pdf_url)
        self.assertTrue(isinstance(paper_data, PaperData))
        self.assertEqual(paper_data.abs_url, abs_url)
        self.assertEqual(paper_data.pdf_url, pdf_url)
        self.assertEqual(paper_data.paper_venue, "CVPR")
        self.assertEqual(paper_data.year, 2018)

    def test_CVPR2018W(self):

        abs_url = "https://openaccess.thecvf.com/content_cvpr_2018_workshops/w3/html/Naphade_The_2018_NVIDIA_CVPR_2018_paper.html"
        pdf_url = "https://openaccess.thecvf.com/content_cvpr_2018_workshops/papers/w3/Naphade_The_2018_NVIDIA_CVPR_2018_paper.pdf"
        paper_data = process_cvf_target(abs_url)
        self.assertTrue(isinstance(paper_data, PaperData))
        self.assertEqual(paper_data.abs_url, abs_url)
        self.assertEqual(paper_data.pdf_url, pdf_url)
        self.assertEqual(paper_data.paper_venue, "CVPR_Workshops")
        self.assertEqual(paper_data.year, 2018)
        paper_data = process_cvf_target(pdf_url)
        self.assertTrue(isinstance(paper_data, PaperData))
        self.assertEqual(paper_data.abs_url, abs_url)
        self.assertEqual(paper_data.pdf_url, pdf_url)
        self.assertEqual(paper_data.paper_venue, "CVPR_Workshops")
        self.assertEqual(paper_data.year, 2018)

    ################################################################
    # 2017 ICCV
    # workshop: workshop_name/html
    # workshop: papers/workshop_name

    def test_ICCV2017(self):
        abs_url = "https://openaccess.thecvf.com/content_iccv_2017/html/Campbell_Globally-Optimal_Inlier_Set_ICCV_2017_paper.html"
        pdf_url = "https://openaccess.thecvf.com/content_ICCV_2017/papers/Campbell_Globally-Optimal_Inlier_Set_ICCV_2017_paper.pdf"
        paper_data = process_cvf_target(abs_url)
        self.assertTrue(isinstance(paper_data, PaperData))
        self.assertEqual(paper_data.abs_url, abs_url)
        self.assertEqual(paper_data.pdf_url, pdf_url)
        self.assertEqual(paper_data.paper_venue, "ICCV")
        self.assertEqual(paper_data.year, 2017)
        paper_data = process_cvf_target(pdf_url)
        self.assertTrue(isinstance(paper_data, PaperData))
        self.assertEqual(paper_data.abs_url, abs_url)
        self.assertEqual(paper_data.pdf_url, pdf_url)
        self.assertEqual(paper_data.paper_venue, "ICCV")
        self.assertEqual(paper_data.year, 2017)

    def test_ICCV2017W(self):
        abs_url = "https://openaccess.thecvf.com/content_ICCV_2017_workshops/w1/html/Pape_Solving_Large_Multicut_ICCV_2017_paper.html"
        pdf_url = "https://openaccess.thecvf.com/content_ICCV_2017_workshops/papers/w1/Pape_Solving_Large_Multicut_ICCV_2017_paper.pdf"
        paper_data = process_cvf_target(abs_url)
        self.assertTrue(isinstance(paper_data, PaperData))
        self.assertEqual(paper_data.abs_url, abs_url)
        self.assertEqual(paper_data.pdf_url, pdf_url)
        self.assertEqual(paper_data.paper_venue, "ICCV_Workshops")
        self.assertEqual(paper_data.year, 2017)
        paper_data = process_cvf_target(pdf_url)
        self.assertTrue(isinstance(paper_data, PaperData))
        self.assertEqual(paper_data.abs_url, abs_url)
        self.assertEqual(paper_data.pdf_url, pdf_url)
        self.assertEqual(paper_data.paper_venue, "ICCV_Workshops")
        self.assertEqual(paper_data.year, 2017)

    ################################################################
    # 2017 CVPR
    # workshop: workshop_name/html
    # workshop: workshop_name/papers

    def test_CVPR2017(self):
        abs_url = "https://openaccess.thecvf.com/content_cvpr_2017/html/Teney_Graph-Structured_Representations_for_CVPR_2017_paper.html"
        pdf_url = "https://openaccess.thecvf.com/content_cvpr_2017/papers/Teney_Graph-Structured_Representations_for_CVPR_2017_paper.pdf"
        paper_data = process_cvf_target(abs_url)
        self.assertTrue(isinstance(paper_data, PaperData))
        self.assertEqual(paper_data.abs_url, abs_url)
        self.assertEqual(paper_data.pdf_url, pdf_url)
        self.assertEqual(paper_data.paper_venue, "CVPR")
        self.assertEqual(paper_data.year, 2017)
        paper_data = process_cvf_target(pdf_url)
        self.assertTrue(isinstance(paper_data, PaperData))
        self.assertEqual(paper_data.abs_url, abs_url)
        self.assertEqual(paper_data.pdf_url, pdf_url)
        self.assertEqual(paper_data.paper_venue, "CVPR")
        self.assertEqual(paper_data.year, 2017)

    def test_CVPR2017W(self):
        abs_url = "https://openaccess.thecvf.com/content_cvpr_2017_workshops/w12/html/Ancuti_Locally_Adaptive_Color_CVPR_2017_paper.html"
        pdf_url = "https://openaccess.thecvf.com/content_cvpr_2017_workshops/w12/papers/Ancuti_Locally_Adaptive_Color_CVPR_2017_paper.pdf"
        paper_data = process_cvf_target(abs_url)
        self.assertTrue(isinstance(paper_data, PaperData))
        self.assertEqual(paper_data.abs_url, abs_url)
        self.assertEqual(paper_data.pdf_url, pdf_url)
        self.assertEqual(paper_data.paper_venue, "CVPR_Workshops")
        self.assertEqual(paper_data.year, 2017)
        paper_data = process_cvf_target(pdf_url)
        self.assertTrue(isinstance(paper_data, PaperData))
        self.assertEqual(paper_data.abs_url, abs_url)
        self.assertEqual(paper_data.pdf_url, pdf_url)
        self.assertEqual(paper_data.paper_venue, "CVPR_Workshops")
        self.assertEqual(paper_data.year, 2017)

    ################################################################
    # 2016
    # workshop: workshop_name/html
    # workshop: workshop_name/papers

    def test_CVPR2016(self):
        abs_url = "https://openaccess.thecvf.com/content_cvpr_2016/html/Hendricks_Deep_Compositional_Captioning_CVPR_2016_paper.html"
        pdf_url = "https://openaccess.thecvf.com/content_cvpr_2016/papers/Hendricks_Deep_Compositional_Captioning_CVPR_2016_paper.pdf"
        paper_data = process_cvf_target(abs_url)
        self.assertTrue(isinstance(paper_data, PaperData))
        self.assertEqual(paper_data.abs_url, abs_url)
        self.assertEqual(paper_data.pdf_url, pdf_url)
        self.assertEqual(paper_data.paper_venue, "CVPR")
        self.assertEqual(paper_data.year, 2016)
        paper_data = process_cvf_target(pdf_url)
        self.assertTrue(isinstance(paper_data, PaperData))
        self.assertEqual(paper_data.abs_url, abs_url)
        self.assertEqual(paper_data.pdf_url, pdf_url)
        self.assertEqual(paper_data.paper_venue, "CVPR")
        self.assertEqual(paper_data.year, 2016)

    def test_CVPR2016W(self):
        abs_url = "https://openaccess.thecvf.com/content_cvpr_2016_workshops/w3/html/Mostegel_UAV-Based_Autonomous_Image_CVPR_2016_paper.html"
        pdf_url = "https://openaccess.thecvf.com/content_cvpr_2016_workshops/w3/papers/Mostegel_UAV-Based_Autonomous_Image_CVPR_2016_paper.pdf"
        paper_data = process_cvf_target(abs_url)
        self.assertTrue(isinstance(paper_data, PaperData))
        self.assertEqual(paper_data.abs_url, abs_url)
        self.assertEqual(paper_data.pdf_url, pdf_url)
        self.assertEqual(paper_data.paper_venue, "CVPR_Workshops")
        self.assertEqual(paper_data.year, 2016)
        paper_data = process_cvf_target(pdf_url)
        self.assertTrue(isinstance(paper_data, PaperData))
        self.assertEqual(paper_data.abs_url, abs_url)
        self.assertEqual(paper_data.pdf_url, pdf_url)
        self.assertEqual(paper_data.paper_venue, "CVPR_Workshops")
        self.assertEqual(paper_data.year, 2016)

    ################################################################
    # 2015 ICCV
    # workshop: workshop_name/html
    # workshop: workshop_name/papers

    def test_ICCV2015(self):
        abs_url = "https://openaccess.thecvf.com/content_iccv_2015/html/Malinowski_Ask_Your_Neurons_ICCV_2015_paper.html"
        pdf_url = "https://openaccess.thecvf.com/content_iccv_2015/papers/Malinowski_Ask_Your_Neurons_ICCV_2015_paper.pdf"
        paper_data = process_cvf_target(abs_url)
        self.assertTrue(isinstance(paper_data, PaperData))
        self.assertEqual(paper_data.abs_url, abs_url)
        self.assertEqual(paper_data.pdf_url, pdf_url)
        self.assertEqual(paper_data.paper_venue, "ICCV")
        self.assertEqual(paper_data.year, 2015)
        paper_data = process_cvf_target(pdf_url)
        self.assertTrue(isinstance(paper_data, PaperData))
        self.assertEqual(paper_data.abs_url, abs_url)
        self.assertEqual(paper_data.pdf_url, pdf_url)
        self.assertEqual(paper_data.paper_venue, "ICCV")
        self.assertEqual(paper_data.year, 2015)

    def test_ICCV2015W(self):
        abs_url = "https://openaccess.thecvf.com/content_iccv_2015_workshops/w1/html/Wu_Hierarchical_Union-of-Subspaces_Model_ICCV_2015_paper.html"
        pdf_url = "https://openaccess.thecvf.com/content_iccv_2015_workshops/w1/papers/Wu_Hierarchical_Union-of-Subspaces_Model_ICCV_2015_paper.pdf"
        paper_data = process_cvf_target(abs_url)
        self.assertTrue(isinstance(paper_data, PaperData))
        self.assertEqual(paper_data.abs_url, abs_url)
        self.assertEqual(paper_data.pdf_url, pdf_url)
        self.assertEqual(paper_data.paper_venue, "ICCV_Workshops")
        self.assertEqual(paper_data.year, 2015)
        paper_data = process_cvf_target(pdf_url)
        self.assertTrue(isinstance(paper_data, PaperData))
        self.assertEqual(paper_data.abs_url, abs_url)
        self.assertEqual(paper_data.pdf_url, pdf_url)
        self.assertEqual(paper_data.paper_venue, "ICCV_Workshops")
        self.assertEqual(paper_data.year, 2015)

    ################################################################
    # 2015 CVPR
    # workshop: workshop_name/html
    # workshop: workshop_name/papers

    def test_CVPR2015(self):
        abs_url = "https://openaccess.thecvf.com/content_cvpr_2015/html/Szegedy_Going_Deeper_With_2015_CVPR_paper.html"
        pdf_url = "https://openaccess.thecvf.com/content_cvpr_2015/papers/Szegedy_Going_Deeper_With_2015_CVPR_paper.pdf"
        paper_data = process_cvf_target(abs_url)
        self.assertTrue(isinstance(paper_data, PaperData))
        self.assertEqual(paper_data.abs_url, abs_url)
        self.assertEqual(paper_data.pdf_url, pdf_url)
        self.assertEqual(paper_data.paper_venue, "CVPR")
        self.assertEqual(paper_data.year, 2015)
        paper_data = process_cvf_target(pdf_url)
        self.assertTrue(isinstance(paper_data, PaperData))
        self.assertEqual(paper_data.abs_url, abs_url)
        self.assertEqual(paper_data.pdf_url, pdf_url)
        self.assertEqual(paper_data.paper_venue, "CVPR")
        self.assertEqual(paper_data.year, 2015)

    def test_CVPR2015W(self):
        abs_url = "https://openaccess.thecvf.com/content_cvpr_workshops_2015/W01/html/Kaur_From_Photography_to_2015_CVPR_paper.html"
        pdf_url = "https://openaccess.thecvf.com/content_cvpr_workshops_2015/W01/papers/Kaur_From_Photography_to_2015_CVPR_paper.pdf"
        paper_data = process_cvf_target(abs_url)
        self.assertTrue(isinstance(paper_data, PaperData))
        self.assertEqual(paper_data.abs_url, abs_url)
        self.assertEqual(paper_data.pdf_url, pdf_url)
        self.assertEqual(paper_data.paper_venue, "CVPR_Workshops")
        self.assertEqual(paper_data.year, 2015)
        paper_data = process_cvf_target(pdf_url)
        self.assertTrue(isinstance(paper_data, PaperData))
        self.assertEqual(paper_data.abs_url, abs_url)
        self.assertEqual(paper_data.pdf_url, pdf_url)
        self.assertEqual(paper_data.paper_venue, "CVPR_Workshops")
        self.assertEqual(paper_data.year, 2015)

    ################################################################
    # 2014

    def test_CVPR2014(self):
        abs_url = "https://openaccess.thecvf.com/content_cvpr_2014/html/Cheng_Fast_and_Accurate_2014_CVPR_paper.html"
        pdf_url = "https://openaccess.thecvf.com/content_cvpr_2014/papers/Cheng_Fast_and_Accurate_2014_CVPR_paper.pdf"
        paper_data = process_cvf_target(abs_url)
        self.assertTrue(isinstance(paper_data, PaperData))
        self.assertEqual(paper_data.abs_url, abs_url)
        self.assertEqual(paper_data.pdf_url, pdf_url)
        self.assertEqual(paper_data.paper_venue, "CVPR")
        self.assertEqual(paper_data.year, 2014)
        paper_data = process_cvf_target(pdf_url)
        self.assertTrue(isinstance(paper_data, PaperData))
        self.assertEqual(paper_data.abs_url, abs_url)
        self.assertEqual(paper_data.pdf_url, pdf_url)
        self.assertEqual(paper_data.paper_venue, "CVPR")
        self.assertEqual(paper_data.year, 2014)

    def test_CVPR2014W(self):
        abs_url = "https://openaccess.thecvf.com/content_cvpr_workshops_2014/W14/html/Slimani_Human_Interaction_Recognition_2014_CVPR_paper.html"
        pdf_url = "https://openaccess.thecvf.com/content_cvpr_workshops_2014/W14/papers/Slimani_Human_Interaction_Recognition_2014_CVPR_paper.pdf"
        paper_data = process_cvf_target(abs_url)
        self.assertTrue(isinstance(paper_data, PaperData))
        self.assertEqual(paper_data.abs_url, abs_url)
        self.assertEqual(paper_data.pdf_url, pdf_url)
        self.assertEqual(paper_data.paper_venue, "CVPR_Workshops")
        self.assertEqual(paper_data.year, 2014)
        paper_data = process_cvf_target(pdf_url)
        self.assertTrue(isinstance(paper_data, PaperData))
        self.assertEqual(paper_data.abs_url, abs_url)
        self.assertEqual(paper_data.pdf_url, pdf_url)
        self.assertEqual(paper_data.paper_venue, "CVPR_Workshops")
        self.assertEqual(paper_data.year, 2014)

    ################################################################
    # 2013

    def test_ICCV2013(self):
        abs_url = "https://openaccess.thecvf.com/content_iccv_2013/html/Jia_Latent_Task_Adaptation_2013_ICCV_paper.html"
        pdf_url = "https://openaccess.thecvf.com/content_iccv_2013/papers/Jia_Latent_Task_Adaptation_2013_ICCV_paper.pdf"
        paper_data = process_cvf_target(abs_url)
        self.assertTrue(isinstance(paper_data, PaperData))
        self.assertEqual(paper_data.abs_url, abs_url)
        self.assertEqual(paper_data.pdf_url, pdf_url)
        self.assertEqual(paper_data.paper_venue, "ICCV")
        self.assertEqual(paper_data.year, 2013)
        paper_data = process_cvf_target(pdf_url)
        self.assertTrue(isinstance(paper_data, PaperData))
        self.assertEqual(paper_data.abs_url, abs_url)
        self.assertEqual(paper_data.pdf_url, pdf_url)
        self.assertEqual(paper_data.paper_venue, "ICCV")
        self.assertEqual(paper_data.year, 2013)

    def test_ICCV2013W(self):
        abs_url = "https://openaccess.thecvf.com/content_iccv_workshops_2013/W23/html/Choe_Semantic_Video-to-Video_Search_2013_ICCV_paper.html"
        pdf_url = "https://openaccess.thecvf.com/content_iccv_workshops_2013/W23/papers/Choe_Semantic_Video-to-Video_Search_2013_ICCV_paper.pdf"
        paper_data = process_cvf_target(abs_url)
        self.assertTrue(isinstance(paper_data, PaperData))
        self.assertEqual(paper_data.abs_url, abs_url)
        self.assertEqual(paper_data.pdf_url, pdf_url)
        self.assertEqual(paper_data.paper_venue, "ICCV_Workshops")
        self.assertEqual(paper_data.year, 2013)
        paper_data = process_cvf_target(pdf_url)
        self.assertTrue(isinstance(paper_data, PaperData))
        self.assertEqual(paper_data.abs_url, abs_url)
        self.assertEqual(paper_data.pdf_url, pdf_url)
        self.assertEqual(paper_data.paper_venue, "ICCV_Workshops")
        self.assertEqual(paper_data.year, 2013)

    def test_CVPR2013(self):
        abs_url = "https://openaccess.thecvf.com/content_cvpr_2013/html/Kim_Deformable_Spatial_Pyramid_2013_CVPR_paper.html"
        pdf_url = "https://openaccess.thecvf.com/content_cvpr_2013/papers/Kim_Deformable_Spatial_Pyramid_2013_CVPR_paper.pdf"
        paper_data = process_cvf_target(abs_url)
        self.assertTrue(isinstance(paper_data, PaperData))
        self.assertEqual(paper_data.abs_url, abs_url)
        self.assertEqual(paper_data.pdf_url, pdf_url)
        self.assertEqual(paper_data.paper_venue, "CVPR")
        self.assertEqual(paper_data.year, 2013)
        paper_data = process_cvf_target(pdf_url)
        self.assertTrue(isinstance(paper_data, PaperData))
        self.assertEqual(paper_data.abs_url, abs_url)
        self.assertEqual(paper_data.pdf_url, pdf_url)
        self.assertEqual(paper_data.paper_venue, "CVPR")
        self.assertEqual(paper_data.year, 2013)

    def test_CVPR2013W(self):
        abs_url = "https://openaccess.thecvf.com/content_cvpr_workshops_2013/W02/html/Kose_Shape_and_Texture_2013_CVPR_paper.html"
        pdf_url = "https://openaccess.thecvf.com/content_cvpr_workshops_2013/W02/papers/Kose_Shape_and_Texture_2013_CVPR_paper.pdf"
        paper_data = process_cvf_target(abs_url)
        self.assertTrue(isinstance(paper_data, PaperData))
        self.assertEqual(paper_data.abs_url, abs_url)
        self.assertEqual(paper_data.pdf_url, pdf_url)
        self.assertEqual(paper_data.paper_venue, "CVPR_Workshops")
        self.assertEqual(paper_data.year, 2013)
        paper_data = process_cvf_target(pdf_url)
        self.assertTrue(isinstance(paper_data, PaperData))
        self.assertEqual(paper_data.abs_url, abs_url)
        self.assertEqual(paper_data.pdf_url, pdf_url)
        self.assertEqual(paper_data.paper_venue, "CVPR_Workshops")
        self.assertEqual(paper_data.year, 2013)
