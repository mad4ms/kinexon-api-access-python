# setup.py
from setuptools import setup, find_packages

setup(
    name="bielemetrics_kinexon_api_wrapper",
    version="0.1.0",
    description="A wrapper for the Kinexon API for Bielemetrics",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="Michael Adams, Alexander David",
    author_email="madams@techfak.uni-bielefeld.de",
    url="https://github.com/mad4ms/kinexon-api-access-python",
    packages=find_packages(),
    install_requires=[
        "requests",
        "tqdm",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
