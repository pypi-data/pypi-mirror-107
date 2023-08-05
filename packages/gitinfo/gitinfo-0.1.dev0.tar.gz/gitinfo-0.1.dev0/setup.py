from setuptools import setup, find_packages

setup(
    name="gitinfo",
    version="0.1dev",
    description="Quickly get information about a Github repository",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "gitinfo = gitinfo.__init__:main",
        ]
    },
)
