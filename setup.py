from setuptools import find_packages
from setuptools import setup

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="Password Entropy",
    version="0.0.1",
    author="Jack Wardell",
    long_description=long_description,
    packages=find_packages(),
    include_package_data=True,
    python_requires='>=3.6',
)
