import pathlib
from setuptools import setup, find_packages

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()


setup(
    name="scikit-fe",
    version="0.1.0",
    description="Feature Engineering Based On Scikit-learn",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/aitrek/scikit-fe",
    author="zhaojianqiang",
    author_email="zhaojianqiang@foxmail.com",
    packages=["skfe"]
)
