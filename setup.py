#!/usr/bin/env python

from setuptools import setup
from setuptools import find_packages

import derpibooru

setup(
  name = "DerPyBooru-NonStandard",
  description = "Python bindings for Derpibooru's API - Non-Standard Modifications",
  url = "https://github.com/ChlorideCull/DerPyBooru",
  version = "0.6-1",
  author = "Joshua Stone, Chloride Cull",
  author_email = "steamruler@gmail.com",
  license = "Simplified BSD License",
  platforms = ["any"],
  packages = find_packages(),
  install_requires = ["requests"],
  include_package_data = True,
  download_url = "https://github.com/ChlorideCull/DerPyBooru/archive/non-standard-changes.tar.gz",
  classifiers = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "Operating System :: OS Independent",
    "License :: OSI Approved :: BSD License",
    "Topic :: Software Development :: Libraries :: Python Modules",
    "Programming Language :: Python :: 3"
  ]
)
