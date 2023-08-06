import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="corha",
    version="0.3.1",
    description="Collection Of Random Helpful Algorithms",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/mattl1598/project-corha",
    author="mattl1598",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
    ],
    packages=["corha"],
    include_package_data=True,
    install_requires=[
        'dotmap>=1.3.23'
    ]
)
