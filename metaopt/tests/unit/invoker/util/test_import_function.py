"""
Test for the import function utility.
"""
from metaopt.invoker.util.import_function import import_function
import nose
from metaopt.invoker.util.determine_package import determine_package


def f():
    return "My name is f."


class LocalClass(object):
    """Stub class as determination target."""

    def foo_method(self):
        """Stub method as determination target."""
        return "My name is foo_method."

    def bar_method(self):
        """Stub method as determination target."""
        return "My name is bar_method."


class TestImportFunction(object):
    """Tests for the import function utility."""

    def test_import_local_function(self):
        """A function can be imported by its own package."""
        import_function(determine_package(f))
        assert f() == "My name is f."

    def test_import_local_class(self):
        """A function can be imported by the package of a class next to it."""
        import_function(determine_package(LocalClass))
        assert f() == "My name is f."

    def test_import_local_method(self):
        """A function can be imported by the package of a method next to it."""
        import_function(determine_package(LocalClass().foo_method))
        assert f() == "My name is f."

    def test_import_local_methods(self):
        """Tests that two methods of the same class are in the same package."""
        package_foo = determine_package(LocalClass().foo_method)
        package_bar = determine_package(LocalClass().bar_method)
        assert package_foo == package_bar


if __name__ == '__main__':
    nose.runmodule()
