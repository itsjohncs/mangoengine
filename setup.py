#!/usr/bin/env python

import os
from setuptools import setup, find_packages

def read(fname):
    """
    Returns the contents of the file in the top level directory with the name
    ``fname``.

    """

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
    ],
    # This ensures that the MANIFEST.IN file is used for both binary and source
    # distributions.
    include_package_data = True
)
