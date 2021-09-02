from setuptools import find_namespace_packages, setup

MAJOR = 1
MINOR = 0
MICRO = 1
VERSION = "%d.%d.%d" % (MAJOR, MINOR, MICRO)

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="arxiv-dl",
    version=VERSION,
    author="Mark Huang",
    author_email="mark.h.huang@gmail.com",
    description="Command-line arXiv.org Papers Downloader. Citation extraction and PDF naming automation.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MarkHershey/arxiv-dl",
    packages=find_namespace_packages(include=["arxiv_dl"]),
    scripts=[
        "arxiv_dl/bin/getpaper",
        "arxiv_dl/bin/add-paper",
        "arxiv_dl/bin/dl-paper",
    ],
    install_requires=[
        "colorlog>=4.1.0",
        # "orderedset>=2.0.0",
        "requests",
        "beautifulsoup4",
    ],
    extras_require={
        "dev": [
            "check-manifest",
            "pytest",
            "tox",
            "twine",
            "wheel",
        ]
    },
    classifiers=[
        "Topic :: Utilities",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent",
        "Natural Language :: English",
    ],
    python_requires=">=3.6",
)
