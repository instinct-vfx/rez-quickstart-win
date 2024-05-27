"""Package setup"""
import setuptools


with open("README.md", "r") as f:
    long_description = f.read()

requirements = ["click"]


setuptools.setup(
    name="rez-quickstart-win",
    version="0.1.0",
    author="Thorsten Kaufmann",
    description="Create initial rez packages for platform, os, arch and python",
    packages=setuptools.find_packages(
        exclude=["dist", "build", "*.egg-info", "tests"]
    ),
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "rez-quickstart = rez-quickstart.cli:cli"
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
    ],
)
