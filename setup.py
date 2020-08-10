from setuptools import find_packages
from setuptools import setup

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="Password Validation",
    version="0.1.1",
    author="Jack Wardell",
    description="A simple API to validate passwords according to basic guidelines",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jackwardell/PasswordValidation",
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
