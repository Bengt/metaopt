# -*- coding: utf-8 -*-
"""
Example demonstrating the saes target algorithm and the grid search optimizer.
"""
from __future__ import division, print_function, with_statement

import orges.param as param
from orges.main import optimize
from orges.plugins.print import PrintPlugin
from orges.plugins.timeout import TimeoutPlugin
from orges.optimizer.gridsearch import GridSearchOptimizer
from orges.examples.algorithm.saes import f as saes


@param.int("mu", interval=(5, 10), title="μ")
@param.int("lambd", interval=(5, 10), title="λ")
@param.float("tau0", interval=(0, 1), step=0.5, title="τ0")
@param.float("tau1", interval=(0, 1), step=0.5, title="τ1")
def f(mu, lambd, tau0, tau1):
    args = dict()

    args["d"] = 10
    args["epsilon"] = 0.0001
    args["mu"] = mu
    args["lambd"] = lambd
    args["tau0"] = tau0
    args["tau1"] = tau1

    return saes(args)

if __name__ == '__main__':
    # Local timeout after 1 second
    PLUGINS = [TimeoutPlugin(1), PrintPlugin()]
    print(optimize(function=f, optimizer=GridSearchOptimizer(),
                   plugins=PLUGINS))
