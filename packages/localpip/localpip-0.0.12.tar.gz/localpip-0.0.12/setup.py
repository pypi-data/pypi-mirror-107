from setuptools import setup
import sys
from pathlib import Path

CURRENT_DIR = Path(__file__).parent
sys.path.insert(0, str(CURRENT_DIR))  # for setuptools.build_meta


def get_long_description() -> str:
    return (CURRENT_DIR / "README.md").read_text(encoding="utf8")


setup(
    name="localpip",
    version="0.0.12",
    description="Offline package manager for Python",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    url="https://github.com/alexbourg/LocalPIP",
    author="Alex BOURG",
    author_email="alex.bourg@outlook.com",
    license="MIT",
    keywords=["localpip", "python", "offline", "package manager", "anaconda"],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: Microsoft :: Windows",
    ],
    packages=["localpip"],
    entry_points={
        "console_scripts": [
            "localpip = localpip.__main__:main",
            "lpip = localpip.__main__:main",
        ],
    },
)
