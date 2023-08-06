import setuptools

#! /usr/bin/python
# -*- coding: utf-8 -*-

from typing import List
from setuptools import setup, find_packages

PACKAGE_VERSION = '1.0.0'


def parse_requirements(path: str = 'requirements.txt') -> List[str]:
    with open(path) as f:
        return f.readlines()


def write_version_py(filename='polygenic/version.py'):
    cnt = """
# THIS FILE IS GENERATED FROM SETUP.PY
version = '{}'
"""
    with open(filename, 'w') as f:
        f.write(cnt.format(PACKAGE_VERSION))


write_version_py()

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="polygenic",
    version=PACKAGE_VERSION,
    author="Marcin Piechota",
    author_email="piechota@intelliseq.com",
    description="Package allowing for computing polygenic scores",
    #long_description=long_description,
    #long_description_content_type="text/reStructuredText",
    url="https://github.com/marpiech/polygenic",
    packages=setuptools.find_packages(),
    package_data={'polygenic': ['*.cfg']},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=['threaded','regex'],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'polygenic=polygenic:main',
        ],
    },
    test_suite='nose.collector',
    tests_require=['nose>=1.0'],
    setup_requires=['nose>=1.0'],
)
