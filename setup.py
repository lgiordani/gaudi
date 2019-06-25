#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    # TODO: put package requirements here
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='gaudi',
    version='1.0.1',
    description="A helper library for Clean Architectures in Python",
    long_description=readme + '\n\n' + history,
    author="Leonardo Giordani",
    author_email='giordani.leonardo@gmail.com',
    url='https://github.com/lgiordani/gaudi',
    packages=[
        'gaudi',
    ],
    package_dir={'gaudi':
                 'gaudi'},
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords='gaudi',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
