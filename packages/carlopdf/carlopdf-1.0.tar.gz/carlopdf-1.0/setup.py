import setuptools
from pathlib import Path

setuptools.setup(
    name="carlopdf",
    version=1.0,
    long_description=Path("README.md").read_text(),
    # excludes test and data directories
    packages=setuptools.find_packages(exclude=["tests", "data"])
)
