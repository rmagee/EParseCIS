#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'Click>=6.0',
    # TODO: put package requirements here
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='eparsecis',
    version='0.2.0',
    description="Python lxml parsing for EPCIS Events.",
    long_description=readme + '\n\n' + history,
    author="Serial Lab, LLC",
    author_email='slab@serial-lab.com',
    url='https://gitlab.com/serial-lab/eparsecis',
    packages=[
        'eparsecis',
    ],
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
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
