from setuptools import setup, find_packages
 
with open("README.md", "r", encoding="utf8") as fh:
    long_desc = fh.read()

setup(
    name="dlive.py",
    version="0.0.2",
    author="Gavyn Stanley",
    description="An API Wrapper for interacting with DLive",
    long_description=long_desc,
    long_description_content_type="text/markdown",
    url="https://github.com/A-Trash-Coder/dlive.py",
    packages=find_packages()
)
