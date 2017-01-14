#!/usr/bin/env python3

import os
import re
import sys
import time

from setuptools import find_packages, setup


with open(os.path.join("pyfastcopy", "__init__.py"), "rt") as f:
  version = re.search("__version__ = \"([^\"]+)\"", f.read()).group(1)

requirements = []
if not hasattr(os, "sendfile") and not sys.platform.startswith("win32"):
  requirements.append("pysendfile")
try:
  import unittest.mock
except ImportError:
  requirements.append("mock")
if not hasattr(time, "monotonic"):
  requirements.append("monotonic")

try:
  import pypandoc
  readme = pypandoc.convert("README.md", "rst")
except ImportError:
  with open("README.md", "rt") as f:
    readme = f.read()

setup(name="pyfastcopy",
      version=version,
      author="desbma",
      packages=find_packages(exclude=("tests",)),
      test_suite="tests",
      install_requires=requirements,
      description="Speed up shutil.copyfile by using sendfile system call",
      long_description=readme,
      url="https://github.com/desbma/pyfastcopy",
      download_url="https://github.com/desbma/pyfastcopy/archive/%s.tar.gz" % (version),
      keywords=["shutil", "copy", "copyfile", "file", "performance", "speed", "sendfile"],
      classifiers=["Development Status :: 4 - Beta",
                   "Intended Audience :: Developers",
                   "License :: OSI Approved :: Python Software Foundation License",
                   "Operating System :: Unix",
                   "Programming Language :: Python",
                   "Programming Language :: Python :: 2",
                   "Programming Language :: Python :: 2.7",
                   "Programming Language :: Python :: 3",
                   "Programming Language :: Python :: 3.0",
                   "Programming Language :: Python :: 3.1",
                   "Programming Language :: Python :: 3.2",
                   "Programming Language :: Python :: 3.3",
                   "Programming Language :: Python :: 3.4",
                   "Programming Language :: Python :: 3.5",
                   "Programming Language :: Python :: 3.6",
                   "Topic :: Software Development :: Libraries :: Python Modules"])
