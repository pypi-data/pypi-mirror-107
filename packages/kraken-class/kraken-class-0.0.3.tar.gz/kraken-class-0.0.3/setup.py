import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="kraken-class",
    version="0.0.3",
    description="Kraken class",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/tactik8/kraken_class",
    author="Tactik8",
    author_email="info@tactik8.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
    ],
    packages=["kraken_class"],
    include_package_data=True,
    install_requires=["kraken-record", "kraken-db", "kraken-cache"],
    
)
