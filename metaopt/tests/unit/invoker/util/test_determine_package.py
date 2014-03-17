"""
Tests for the determine_package utility.
"""
from __future__ import division, print_function, with_statement

import string

import nose
from nose.tools.trivial import eq_

from metaopt.invoker.util.determine_package import determine_package
from metaopt.tests.util.functions import FUNCTIONS_INTEGER_WORKING


def local_function():
    """Stub function that is located in the same package of the tests."""
    pass


class LocalClass(object):
    """Stub class as determination target."""

    def local_method(self):
        """Stub method as determination target."""
        pass

    def foo_method(self):
        """Stub method as determination target."""
        pass

    def bar_method(self):
        """Stub method as determination target."""
        pass


class TestDeterminePackage(object):
    """Tests for the determine package utility."""

    def __init__(self):
        self._package_local_class = None
        self._package_local_method = None
        self._package_local_function = None

    def setup(self):
        """Nose will run this method before every test method."""
        self._package_local_function = determine_package(local_function)
        self._package_local_class = determine_package(LocalClass)
        self._package_local_method = determine_package(LocalClass.local_method)

    def teardown(self):
        """Nose will run this method after every test method."""
        pass

    def test_determine_local_function(self):
        eq_(self._package_local_function,
            "metaopt.tests.unit.invoker.util.test_determine_package")

        __import__(name=self._package_local_function, globals=globals(),
                   locals=locals(), fromlist=())

    def test_determine_local_class(self):
        eq_(self._package_local_class,
            "metaopt.tests.unit.invoker.util.test_determine_package")

        __import__(name=self._package_local_class, globals=globals(),
                   locals=locals(), fromlist=())

    def test_determine_local_method(self):
        eq_(self._package_local_method,
            "metaopt.tests.unit.invoker.util.test_determine_package")

        __import__(name=self._package_local_method, globals=globals(),
                   locals=locals(), fromlist=())

    def test_determine_imported(self):
        for index, function in enumerate(FUNCTIONS_INTEGER_WORKING):
            package_remote_function = determine_package(function)
            eq_(package_remote_function,
               ("metaopt.tests.util.function.integer.working." +
                string.ascii_lowercase[5 + index]))

            __import__(name=package_remote_function, globals=globals(),
                   locals=locals(), fromlist=())

if __name__ == '__main__':
    nose.runmodule()
