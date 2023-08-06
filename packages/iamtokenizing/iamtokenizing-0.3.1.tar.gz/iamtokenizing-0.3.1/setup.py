#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import setuptools

with open("README.md", "r") as file:
    long_description_ = file.read()
    
setuptools.setup(
    name="iamtokenizing",
    version="0.3.1",
    author="François Konschelle - IAM CHU Bordeaux France",
    author_email="no_email@please.org",
    description="Tools to tokenize a string",
    long_description=long_description_,
    long_description_content_type="text/markdown",
    license="GNU GENERAL PUBLIC LICENSE v.3",
    url="https://framagit.org/fraschelle/tokenizer",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Text Processing",
        "Intended Audience :: Information Technology",
        "Intended Audience :: Science/Research",
    ],
    python_requires='>=3.7',
)
