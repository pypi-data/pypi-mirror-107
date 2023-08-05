#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function

import io
import re
from glob import glob
from os.path import basename
from os.path import dirname
from os.path import join
from os.path import splitext

from setuptools import find_packages
from setuptools import setup


def read(*names, **kwargs):
    with io.open(
        join(dirname(__file__), *names),
        encoding=kwargs.get('encoding', 'utf8')
    ) as fh:
        return fh.read()


setup(
    name='paylense-sdk',
    version='1.0.1',
    license='MIT license',
    description='Python wrapper for the Winopay Paylense API.',
    long_description='%s\n%s' % (
        re.compile('^.. start-badges.*^.. end-badges', re.M | re.S).sub('', read('README.md')),
        re.sub(':[a-z]+:`~?(.*?)`', r'``\1``', read('CHANGELOG.md'))
    ),
    long_description_content_type='text/markdown',
    author='Winopay',
    author_email='acellam.guy@gmail.com',
    url='https://github.com/winopay/paylense-python-sdk',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        # complete classifier list: http://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Unix',
        'Operating System :: POSIX',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Utilities',
    ],
    keywords=[
        'Paylense API', 'Paylense API Python Wrapper','Paylense API Python', 'Paylense API'
    ],
    install_requires=[
        'requests == 2.21.0',
        'Click==7.0',
        'phonenumbers'

        # eg: 'aspectlib==1.1.1', 'six>=1.7',
    ],

    setup_requires=["pytest-runner", "pytest-cov"],


    extras_require={'test': ['pytest', 'pytest-watch', 'tox',
                             'pytest-cov',
                             'pytest-pep8',
                             'pytest-cov',
                             'pytest-sugar',
                             'mock',
                             'pytest-instafail',
                             'pytest-bdd'], "dev": ["semver"]},
    entry_points={
        'console_scripts': [
            'paylense = paylense.cli:main',
        ]
    },
)
