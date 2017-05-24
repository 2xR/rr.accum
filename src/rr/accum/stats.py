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
        self.k = 0
        self.m_k = NAN
        self.v_k = NAN

    def insert(self, datum, **kwargs):
        k0 = self.k
        if k0 == 0:
            self.k = 1
            self.m_k = datum
            self.v_k = 0.0
        else:
            k = k0 + 1
            m_k0 = self.m_k
            m_k = m_k0 + (datum - m_k0) / k
            v_k0 = self.v_k
            v_k = v_k0 + (datum - m_k0) * (datum - m_k)
            self.k = k
            self.m_k = m_k
            self.v_k = v_k
            self.value = v_k / k0


Var = Variance


class StandardDeviation(Accumulator):

    name = "standard_deviation"
    aliases = ["stddev"]
    dependencies = [Variance]

    @property
    def value(self):
        return sqrt(self._accum_set.variance)


StdDev = StandardDeviation


def _example():
    import random

    a = Accumulator.Set(StandardDeviation, Mean, Range)
    n = [random.random() for _ in range(1000)]
    for x in n:
        a.insert(x)
    assert a.min == min(n)
    assert a.max == max(n)
    assert a.count == len(n)
    assert a.sum == sum(n)
    assert a.mean == sum(n) / len(n)
    return a
