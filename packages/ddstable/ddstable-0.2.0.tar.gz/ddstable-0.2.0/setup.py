#!/usr/bin/env python

# https://packaging.python.org/tutorials/packaging-projects
# docker run -it  -v $PWD:/app  -w /app python:3.8  bash
# python3 -m pip install --user --upgrade twine
# python3 setup.py sdist clean
# python3 setup.py sdist bdist_wheel
# python3 -m twine upload --skip-existing --verbose dist/*

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ddstable", 
    version="0.2.0",
    author="xrgopher",
    author_email='xrgopher@outlook.com',
    url='https://gitlab.com/xrgopher/ddstable',
    description="DDS table for contract bridge",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(include=['ddstable','*']),
    package_data={'ddstable': ['*.dll','*.so']},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
