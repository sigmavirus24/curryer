#!/usr/bin/env python

import curryer
import os
import sys

from setuptools import setup
from setuptools.command.test import test as TestCommand

kwargs = {}
requires = []
packages = ['curryer']

kwargs['tests_require'] = ['pytest==2.4.2']
packages.append('tests')

if sys.argv[-1] in ('submit', 'publish'):
    os.system('python setup.py bdist_wheel sdist upload')
    sys.exit()

if not (hasattr(curryer, '__version__') and curryer.__version__):
    raise RuntimeError('Cannot find version information')

__version__ = curryer.__version__


class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = ['-q', 'tests/']
        self.test_suite = True

    def run_tests(self):
        #import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.test_args)
        sys.exit(errno)

setup(
    name='curryer',
    version=__version__,
    description='Haskell style currying for Python3.3+ callables',
    long_description="\n\n".join([open("README.rst").read(),
                                  open("HISTORY.rst").read()]),
    license=open('LICENSE').read(),
    author="Ian Cordasco",
    author_email="graffatcolmingov@gmail.com",
    url="https://curryer.readthedocs.org",
    packages=packages,
    package_data={'': ['LICENSE', 'AUTHORS.rst']},
    include_package_data=True,
    install_requires=requires,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: Implementation :: CPython',
    ],
    extras_require={'test': kwargs['tests_require']},
    cmdclass={'test': PyTest},
    **kwargs
)
