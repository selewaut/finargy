#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

# with open('README.rst') as readme_file:
#     readme = readme_file.read()

# with open('HISTORY.rst') as history_file:
#     history = history_file.read()

requirements = [ ]

test_requirements = ['pytest>=3', ]

setup(
    install_requires=requirements,
    # long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='finargy',
    name='finargy',
    packages=find_packages(include=['finargy', 'finargy.*']),
    test_suite='tests',
    tests_require=test_requirements,
    version='0.0.1',
    zip_safe=False,
)