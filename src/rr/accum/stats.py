from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from math import sqrt

from .accum import Accumulator

INF = float("inf")
NAN = float("nan")


@Accumulator.Generator.factory
def min(accumulator, initial_value=+INF):
    value = initial_value
    while True:
        datum, _ = yield value
        if datum < value:
            value = datum


@Accumulator.Generator.factory
def max(accumulator, initial_value=-INF):
    value = initial_value
    while True:
        datum, _ = yield value
        if datum > value:
            value = datum


@Accumulator.Generator.factory
def count(accumulator, initial_value=0):
    value = initial_value
    while True:
        yield value
        value += 1


@Accumulator.Generator.factory
def sum(accumulator, initial_value=0.0):
    value = initial_value
    while True:
        datum, _ = yield value
        value += datum


@Accumulator.Generator.factory(aliases=["avg", "average"], dependencies=[count, sum])
def mean(accumulator):
    accum_set = accumulator._accum_set
    yield NAN
    while True:
        yield accum_set.mean / accum_set.count


@Accumulator.Generator.factory(aliases=["var"])
def variance(accumulator):
    n = 0
    mean = 0.0
    M2 = 0.0
    datum, _ = yield NAN
    while True:
        n += 1
        delta = datum - mean
        mean += delta / n
        delta2 = datum - mean
        M2 += delta * delta2
        datum, _ = yield M2 / (n - 1)


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

    a = Accumulator.Set(Variance, Min, Max)
    n = [random.random() for _ in range(1000)]
    for x in n:
        a.insert(x)
    assert a.min == min(n)
    assert a.max == max(n)
    assert a.count == len(n)
    assert a.sum == sum(n)
    assert a.mean == sum(n) / len(n)
    return a
