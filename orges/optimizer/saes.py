# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import with_statement

from numpy.random import randn
from random import sample, gauss
from math import exp

from orges.args import ArgsCreator
from orges.optimizer.base import BaseOptimizer


class SAESOptimizer(BaseOptimizer):
    MU = 3
    LAMBDA = 3
    TAU0 = 0.5
    TAU1 = 0.5

    # TODO: Add parameters for MU, LAMBDA etc.
    def __init__(self):
        self._invoker = None
        self._f = None
        self.param_spec = None

        self.population = []
        self.scored_population = []
        self.best_scored_indivual = (None, None)

        self.generation = 1

    @property
    def invoker(self):
        return self._invoker

    @invoker.setter
    def invoker(self, invoker):
        invoker.caller = self
        self._invoker = invoker

    def optimize(self, f, param_spec, return_spec=None, minimize=True):
        self._f = f
        self.param_spec = param_spec

        self.initalize_population()
        self.score_population()

        while not self.exit_condition():
            self.add_offspring()
            self.score_population()
            self.select_parents()

            self.generation += 1

        return self.best_scored_indivual[0]

    def exit_condition(self):
        pass

    def initalize_population(self):
        args_creator = ArgsCreator(self.param_spec)

        for _ in xrange(SAESOptimizer.MU):
            args = args_creator.random()

            # TODO: Use default_mutation_stength method
            args_sigma = list(randn(len(args)))

            args_sigma = [float(sigma) for sigma in args_sigma]

            individual = (args, args_sigma)
            self.population.append(individual)

    def add_offspring(self):
        args_creator = ArgsCreator(self.param_spec)

        for _ in xrange(SAESOptimizer.LAMBDA):
            mother, father = sample(self.population, 2)

            child_args = args_creator.combine(mother[0], father[0])

            mean = lambda x1, x2: float((x1 + x2) / 2)
            child_args_sigma = map(mean, mother[1], father[1])

            child_args = args_creator.randomize(child_args, child_args_sigma)

            tau0_random = gauss(0, 1)

            def mutate_sigma(sigma):
                tau0 = SAESOptimizer.TAU0
                tau1 = SAESOptimizer.TAU1
                return sigma * exp(tau0 * tau0_random)\
                       * exp(tau1 * gauss(0, 1))

            child_args_sigma = map(mutate_sigma, child_args_sigma)

            child = (child_args, child_args_sigma)

            self.population.append(child)

    def score_population(self):
        for individual in self.population:
            args, _ = individual
            self.invoker.invoke(self._f, args, individual=individual)

        self.invoker.wait()

    def select_parents(self):
        self.scored_population.sort(key=lambda s: s[1])
        new_scored_population = self.scored_population[0:SAESOptimizer.MU]
        self.population = map(lambda s: s[0], new_scored_population)

    def on_result(self, result, args, individual):
        # _, fitness = result
        fitness = result
        scored_individual = (individual, fitness)
        self.scored_population.append(scored_individual)

        best_individual, best_fitness = self.best_scored_indivual

        if best_fitness is None or fitness < best_fitness:
            self.best_scored_indivual = scored_individual

    def on_error(self, args, individual):
        pass