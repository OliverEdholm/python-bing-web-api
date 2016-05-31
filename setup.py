#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''Setup file for Bing web search API

This is the module for setting up the Bing search API.

Oliver Edholm 2016-05-30 20:56
'''
# Imports
from setuptools import setup
from setuptools import find_packages
from pip.req import parse_requirements


# Functions
def get_requirements_file():
    '''Returns the packages in requirements.txt.'''
    install_reqs = parse_requirements('requirements.txt', session=False)

    return [str(ir.req) for ir in install_reqs]


def get_required_packages():
    '''Returns all the required packages.'''
    return get_requirements_file()


def setup_package():
    '''Setups the Bing web search API.'''
    setup(
        name='bingsearch',
        version='0.1',
        description='Python Bing web API.',
        author='Oliver Edholm',
        author_email='oliver.edholm@gmail.com',
        packages=find_packages(),
        install_requires=get_required_packages()
    )


if __name__ == "__main__":  # If the user runs this file.
    setup_package()
