from setuptools import setup, find_packages

setup(
    name="gitsort",
    version="0.1dev",
    description="Sort various Github things",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "gitsort = gitsort.cli:development",
        ]
    },
)
