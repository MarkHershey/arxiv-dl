from setuptools import find_namespace_packages, setup

MAJOR = 1
MINOR = 1
MICRO = 5
VERSION = "%d.%d.%d" % (MAJOR, MINOR, MICRO)


def update_version_file():
    VERSION_FILE = "VERSION"
    with open(VERSION_FILE, "w") as f:
        f.write(VERSION)


update_version_file()

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="arxiv-dl",
    version=VERSION,
    author="Mark He Huang",
    author_email="dev@markhh.com",
    description="Command-line arXiv Papers Downloader. Citation extraction and PDF naming automation.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MarkHershey/arxiv-dl",
    packages=find_namespace_packages(include=["arxiv_dl"]),
    scripts=[
        "arxiv_dl/bin/arxiv-dl",
        "arxiv_dl/bin/getpaper",
        "arxiv_dl/bin/paper",
    ],
    install_requires=[
        "colorlog>=4.1.0",
        "requests",
        "pydantic",
        "pypdf>=3.10.0",
        "beautifulsoup4",
        "setuptools",
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
