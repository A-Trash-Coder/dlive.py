from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf8") as fh:
    long_desc = fh.read()

setup(
    name="dlive.py",
    author="Gavyn Stanley",
    url="https://github.com/A-Trash-Coder/dlive.py",
    project_urls={
        "Documentation": "",
        "Issue tracker": "https://github.com/A-Trash-Coder/dlive.py/issues",
    },
    version="0.0.2",
    packages=find_packages(),
    license='MIT',
    description='A Python wrapper for the DLive API',
    long_description=long_desc,
    long_description_content_type="text/markdown",
    install_requires=["websockets", "aiohttp"],
    python_requires='>=3.5.3',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Topic :: Internet',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
    ]
)