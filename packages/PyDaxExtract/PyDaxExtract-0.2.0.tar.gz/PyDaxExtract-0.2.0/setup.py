"""
Install daxextract
"""

import setuptools
import os

try:
    from sphinx.setup_command import BuildDoc
    cmdclass = {"build_sphinx": BuildDoc}
except ModuleNotFoundError:
    pass

def read_text(path):
    """
    Read some text.
    """
    with open(path, "r") as _fh:
        return _fh.read()

setuptools.setup(
    name="PyDaxExtract",
    version="0.2.0",
    description="Extract DAX expressions from Power BI template.",
    long_description=read_text("README.md"),
    long_description_content_type="text/markdown",
    platforms="any",
    author="Doug Shawhan",
    author_email="doug.shawhan@gmail.com",
    url="https://gitlab.com/doug.shawhan/pydaxextract",
    project_urls={
        "Bug Tracker": "https://gitlab.com/doug.shawhan/pydaxextract/issues",
        "Source Code": "https://gitlab.com/doug.shawhan/pydaxextract/tree/master",
        "Source Code": "https://gitlab.com/doug.shawhan/pydaxextract/tree/dev",
        "Documentation": "https://pydaxextract.readthedocs.io",
    },
    entry_points={
        "console_scripts": [
            "daxextract = scripts.daxextract:main",
        ],
    },
    include_package_data=True,
    packages=setuptools.find_packages(),
    license=read_text("LICENSE.txt"),
    zip_safe=True,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)
