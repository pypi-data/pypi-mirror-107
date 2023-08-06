#!/usr/bin/env python3

from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()
setup(
    name='metrics_exporter',
    version='0.0.1',
    author='Alessio Gandelli & Nicola Toscan',
    license='MIT',
    description='Metrics exporter.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/WikiCommunityHealth/metrics_exporter',
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
