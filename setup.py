# -*- coding: utf-8 -*-

from __future__ import with_statement

import sys
import os

from setuptools import setup, find_packages, Extension
from setuptools.command.test import test as TestCommand


class Tox(TestCommand):
    """Enables `python setup.py test` to run tox."""
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        #import here, cause outside the eggs aren't loaded
        import tox
        try:
            tox.cmdline(self.test_args)
        except SystemExit as exception:
            sys.exit(exception.code)

HANG_MODULE_EXTENSION = Extension(
    'orges.test.unit.hang',
    sources=['orges/test/unit/hangmodule.c']
)

setup(
    name='orges',
    version='0.0.1',
    description='OrgES Package - Organic Computing for Evolution Strategies',
    long_description=open("README.rst").read(),
    author='Renke Grunwald, Bengt Lüers, Jendrik Poloczek',
    author_email='info@orges.org',
    url='http://organic-es.tumblr.com/',
#    license=open("LICENSE.txt").read(), # travis will choke on this
    packages=find_packages(exclude=('tests', 'docs')),
    package_data={'': ['LICENSE', 'README.rst', 'requirements.txt']},
    ext_modules=[HANG_MODULE_EXTENSION],
    install_requires=open("requirements.txt").read().splitlines(),
    tests_require=['tox'],
    cmdclass={'test': Tox},
)
