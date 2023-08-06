#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import io, os, re
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
    name='elle_beam2d',
    version='1.0.3',
    #license='BSD-3-Clause',
    description='Differentiable 2D beam model.',
    long_description='%s\n%s' % (
        re.compile('^.. start-badges.*^.. end-badges', re.M | re.S).sub('', read('README.md')),
        re.sub(':[a-z]+:`~?(.*?)`', r'``\1``', read('CHANGELOG.md'))
    ),
    author='Claudio Perez',
    author_email='claudio_perez@berkeley.edu',
    url='https://github.com/claudioperez/elle-beam2d',
    # packages=find_packages('elle/'),
    packages = ['elle.beam2d'],
    namespace_packages=['elle'],
    # package_dir={'': 'elle/'},
    # py_modules=[splitext(basename(path))[0] for path in glob('elle/*.py')],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Operating System :: Unix',
        'Operating System :: POSIX',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Utilities',
    ],
    project_urls={
        'Changelog': 'https://github.com/claudioperez/elle-beam2d/blob/master/CHANGELOG.md',
        'Issue Tracker': 'https://github.com/claudioperez/elle-beam2d/issues',
    },
    keywords=[
        'finite-element-analysis', 'beam', 'structural-analysis',
    ],
    python_requires='>=3.5',
    install_requires=[
        # eg: 'aspectlib==1.1.1', 'six>=1.7',
    ],

)
