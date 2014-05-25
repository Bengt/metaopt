# -*- coding: utf-8 -*-
"""
SVM (SAES, global timeout)
================================
"""
# Future
from __future__ import absolute_import, division, print_function, \
    unicode_literals, with_statement

# Standard Library
from time import sleep

# First Party
from metaopt.core.optimize.optimize import optimize
from metaopt.core.paramspec.util import param
from metaopt.core.returnspec.util.decorator import maximize
from metaopt.optimizer.gridsearch import GridSearchOptimizer
from metaopt.plugin.timeout import TimeoutPlugin


@maximize("Score")
@param.float("a", interval=[0.1, 0.5], step=0.05)
def f(a):
    sleep(a)
    return a


def test_all_timings():
    for timeout_local in [0.05 * i for i in range(5)]:
        for timeout_global in [0.05 * o for o in range(5)]:

            #  print("testing global %s s and local %s s" % (timeout_global,
            #                                               timeout_local))

            optimizer = GridSearchOptimizer()
            plugins = [TimeoutPlugin(timeout_local)]

            optimum = optimize(f=f, timeout=timeout_global, optimizer=optimizer,
                               plugins=plugins)

            # print("The optimal parameters are %s." % str(optimum))

if __name__ == '__main__':
    import nose
    nose.runmodule()