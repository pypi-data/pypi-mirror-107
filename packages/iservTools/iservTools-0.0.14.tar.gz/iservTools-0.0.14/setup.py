import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="iservTools",
    version="0.0.14",
    description="Tools for iServ school servers",
    long_description=README,
    long_description_content_type="text/markdown",
    url="",
    author="Christian Eckhardt",
    author_email="Christian.Eckhardt@gmx.de",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["iServTools"],
    include_package_data=True,
    install_requires=["selenium", "openpyxl"],
    
)