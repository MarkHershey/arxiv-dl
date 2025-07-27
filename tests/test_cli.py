import shutil
import subprocess
import unittest
from pathlib import Path

from arxiv_dl.helpers import DEFAULT_DOWNLOAD_PATH


class TestCLI(unittest.TestCase):
    """Test Command Line Interface"""

    def setUp(self):
        self.root_dir = Path(__file__).resolve().parent.parent
        self.test_dir = self.root_dir / "tests" / "test_tmp"
        self.test_dir.mkdir(exist_ok=True)
        self.test_target = "https://openaccess.thecvf.com/content/CVPR2021/html/Xu_SUTD-TrafficQA_A_Question_Answering_Benchmark_and_an_Efficient_Network_for_CVPR_2021_paper.html"

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)

    @unittest.skipIf(DEFAULT_DOWNLOAD_PATH.exists(), "Default download path exists")
    def test_simple(self):
        subprocess.run(
            f"paper {self.test_target}",
            shell=True,
            check=True,
        )
        shutil.rmtree(DEFAULT_DOWNLOAD_PATH, ignore_errors=True)

    def test_with_inline_env(self):
        subprocess.run(
            f"ARXIV_DOWNLOAD_FOLDER={self.test_dir} paper {self.test_target}",
            shell=True,
            check=True,
        )

    def test_with_flags(self):
        subprocess.run(
            f"paper -v -d {self.test_dir} {self.test_target} ",
            shell=True,
            check=True,
        )


if __name__ == "__main__":
    unittest.main()
