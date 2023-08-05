import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="PyEmission",
    version="0.1",
    description="PyEmission is a Python library for the estimation of vehicular emissions and fuel consumption",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/mamunur-ipe",
    author="Md Mamunur Rahman; Ruby Nguyen",
    author_email="mdmamunur.rahman@inl.gov",
    license="MIT",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=[],
    install_requires=["numpy", "pandas", "matplotlib"],

)