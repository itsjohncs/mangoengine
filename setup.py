#!/usr/bin/env python

import os
from setuptools import setup, find_packages

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "MangoEngine",
    version = read("VERSION").strip(),
    author = "John Sullivan",
    author_email = "john@galahgroup.com",
    description = "MangoEngine is a lightweight library for creating generic "
        "data models in Python.",
    license = "Unlicense",
    keywords = "json python models",
    url = "https://www.github.com/brownhead/mangoengine",
    packages = find_packages(),
    long_description = read("README.rst"),
    classifiers = [
        "License :: Public Domain",
    ]
)
