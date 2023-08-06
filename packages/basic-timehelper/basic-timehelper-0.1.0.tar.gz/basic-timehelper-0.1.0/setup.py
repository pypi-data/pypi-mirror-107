import pathlib
from setuptools import setup, find_packages

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="basic-timehelper",
    version="0.1.0",
    description="Collection of convenient methods to deal with time-related flow",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/timehelper",
    author="Paolo Gervasoni Vila",
    author_email="pgervila@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
    ],
    packages=find_packages(exclude=("tests",)),
    include_package_data=True,
    install_requires=["pytz", "pandas"]
)