#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'lxml==3.7.2',
    'epcpyyes',
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='eparsecis',
    version='0.1.0',
    description="Python lxml parsing for EPCIS Events.",
    long_description=readme + '\n\n' + history,
    author="Rob Magee",
    author_email='slab@serial-lab.com',
    maintainer="SerialLab Corp",
    url='https://gitlab.com/serial-lab/eparsecis',
    packages=find_packages(),
    package_dir={'eparsecis':
                 'eparsecis'},
    entry_points={
        'console_scripts': [
            'eparsecis=eparsecis.cli:main'
        ]
    },
    include_package_data=True,
    install_requires=requirements,
    license="GNU General Public License v3",
    zip_safe=False,
    keywords='eparsecis',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
