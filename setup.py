#!/usr/bin/env python
import io
import os
import re

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

requirements = [
    'numpy',
    'pandas',
    'xlrd',
    'subprocess',
    'click',
    'PyQt5',
    'opendssdirect',
    'bokeh',
    #'ast',
    #'pyproj'
]

# Read the version from the __init__.py file without importing it
def read(*names, **kwargs):
    with io.open(
        os.path.join(os.path.dirname(__file__), *names),
        encoding=kwargs.get("encoding", "utf8")
    ) as fp:
        return fp.read()

def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")

setup(name='PyDSS',
      version=find_version("PyDSS", "__init__.py"),
      description='a high level python interface for OpenDSS',
      author='Aadil Latif',
      author_email='Aadil.Latif@nrel.gov',
      url='https://github.nrel.gov/alatif/PyDSS',
      packages=['PyDSS'],
      install_requires=requirements,
      package_data={'PyDSS': []},
     )