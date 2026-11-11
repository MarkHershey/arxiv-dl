import unittest
from unittest import mock

from arxiv_dl import __main__ as main_module


class TestNThreadsValidation(unittest.TestCase):
    """The --help text caps --n-threads at 16; out-of-range values must
    fail fast with a usage error instead of reaching the download."""

    def run_cli(self, argv):
        with (
            mock.patch("sys.argv", ["paper", *argv]),
            mock.patch.object(main_module, "download_paper") as mock_download,
        ):
            with self.assertRaises(SystemExit) as ctx:
                main_module.cli()
        return ctx.exception.code, mock_download

    def test_n_threads_zero_rejected(self):
        code, mock_download = self.run_cli(["-n", "0", "1512.03385"])
        self.assertEqual(code, 2)
        mock_download.assert_not_called()

    def test_n_threads_above_max_rejected(self):
        code, mock_download = self.run_cli(
            ["--n-threads", "17", "--skip-update-check", "1512.03385"]
        )
        self.assertEqual(code, 2)
        mock_download.assert_not_called()

    def test_n_threads_valid_reaches_download(self):
        with (
            mock.patch(
                "sys.argv",
                ["paper", "-n", "4", "--skip-update-check", "1512.03385"],
            ),
            mock.patch.object(
                main_module, "download_paper", return_value=True
            ) as mock_download,
        ):
            with self.assertRaises(SystemExit) as ctx:
                main_module.cli()
        self.assertEqual(ctx.exception.code, 0)
        mock_download.assert_called_once()


if __name__ == "__main__":
    unittest.main()
