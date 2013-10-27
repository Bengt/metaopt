from threading import Timer

from orges.invoker.base import Invoker, Caller

class PluggableInvoker(Invoker, Caller):
    def __init__(self, resources, invoker, plugins=[]):
        self.invoker = invoker
        self.invoker.caller = self

        self.plugins = plugins

    @property
    def caller(self):
        return self._caller

    @caller.setter
    def caller(self, value):
        self._caller = value

    def get_subinvoker(self, resources):
        pass

    def invoke(self, f, fargs, invocation=None, **kwargs):
        # TODO: Reuse exinsting invocation object
        invocation = Invocation()
        task = self.invoker.invoke(f, fargs, invocation=invocation)

        invocation.current_task = task
        invocation.fargs = fargs
        invocation.kwargs = kwargs

        for plugin in self.plugins:
            plugin.on_invoke(invocation)

    def on_result(self, result, fargs, invocation):
        invocation.current_result = result

        for plugin in self.plugins:
            plugin.on_result(invocation)

        self.caller.on_result(result, fargs, **invocation.kwargs)

    def on_error(self, fargs, invocation):

        for plugin in self.plugins:
            plugin.on_error(invocation)

        self.caller.on_error(fargs, **invocation.kwargs)

    def wait(self):
        self.invoker.wait()

class Invocation():
    @property
    def current_task(self):
        return self._current_task

    @current_task.setter
    def current_task(self, task):
        self._current_task = task

    @property
    def current_result(self):
        return self._current_result

    @current_result.setter
    def current_result(self, result):
        self._current_result = result

    @property
    def fargs(self):
        return self._args

    @fargs.setter
    def fargs(self, fargs):
        self._args = fargs

    @property
    def kwargs(self):
        return self._kwargs

    @kwargs.setter
    def kwargs(self, kwargs):
        self._kwargs = kwargs

    def __repr__(self):
        return str(self.fargs)


class InvocationPlugin():
    def on_invoke(self, invocation):
        pass

    def on_result(self, invocation):
        pass

    def on_error(self, invocation):
        pass


class PrintInvocationPlugin(InvocationPlugin):
    def on_invoke(self, invocation):
        print "Started", "f%s" % (invocation.fargs,)

    def on_result(self, invocation):
        result = invocation.current_result
        print "Finished", "f%s=%s" % (invocation.fargs, result)

    def on_error(self, invocation):
        print "Failed", "f%s" % (invocation.fargs,)


class TimeoutInvocationPlugin(InvocationPlugin):
    def __init__(self, timeout):
        self.timeout = timeout

    def on_invoke(self, invocation):
        current_task = invocation.current_task
        Timer(self.timeout, current_task.cancel).start()