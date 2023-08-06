import setuptools
from pathlib import Path

setuptools.setup(
    name="sgdotlite",
    version='1.0.29',
    long_description=Path("README.md").read_text(),
    packages=setuptools.find_packages(
        exclude=["tests", "sgdotlite/data", "sgdotlite/examples"]),
    install_requires=Path("requirements.txt").read_text().split("\n")[:-1]
)
