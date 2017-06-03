from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from math import sqrt

from .accum import Accumulator

INF = float("inf")
NAN = float("nan")


class Min(Accumulator):

    name = "min"
    value = +INF

    def insert(self, datum, **kwargs):
        if datum < self.value:
            self.value = datum


class Max(Accumulator):

    name = "max"
    value = -INF

    def insert(self, datum, **kwargs):
        if datum > self.value:
            self.value = datum


class Range(Accumulator):

    name = "range"
    dependencies = [Min, Max]
    value = NAN

    @property
    def value(self):
        accum_set = self._accum_set
        return accum_set.max - accum_set.min


class Count(Accumulator):

    name = "count"
    value = 0

    def insert(self, datum, **kwargs):
        self.value += 1


class Sum(Accumulator):

    name = "sum"
    value = 0.0

    def insert(self, datum, **kwargs):
        self.value += datum


class Mean(Accumulator):

    name = "mean"
    dependencies = [Sum, Count]

    @property
    def value(self):
        accum_set = self._accum_set
        n = accum_set.count
        s = accum_set.sum
        return NAN if n == 0 else s / n


class Variance(Accumulator):
    """Implementation of online variance statistic, taken from
        https://en.wikipedia.org/wiki/Algorithms_for_calculating_variance#Online_algorithm
    """

    name = "variance"
    aliases = ["var"]
    dependencies = []
    value = NAN

    def __init__(self, name=None, aliases=None):
        Accumulator.__init__(self, name=name, aliases=aliases)
        self.n = 0
        self.mu = 0.0
        self.m2 = 0.0

    def insert(self, datum, **kwargs):
        n = self.n + 1
        self.n = n
        delta = datum - self.mu
        self.mu += delta / n
        delta2 = datum - self.mu
        self.m2 += delta * delta2
        if n > 1:
            self.value = self.m2 / (n - 1)


Var = Variance


class StandardDeviation(Accumulator):

    name = "standard_deviation"
    aliases = ["stddev"]
    dependencies = [Variance]

    @property
    def value(self):
        return sqrt(self._accum_set.variance)


StdDev = StandardDeviation
