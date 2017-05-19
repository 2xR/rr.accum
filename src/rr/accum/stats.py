from .accum import Accumulator


INF = float("inf")


class Min(Accumulator):

    name = "min"
    value = +INF

    def add(self, datum, **kwargs):
        if datum < self.value:
            self.value = datum


class Max(Accumulator):

    name = "max"
    value = -INF

    def add(self, datum, **kwargs):
        if datum > self.value:
            self.value = datum


class Count(Accumulator):

    name = "count"
    value = 0

    def add(self, datum, **kwargs):
        self.value += 1


class Sum(Accumulator):

    name = "sum"
    value = 0.0

    def add(self, datum, **kwargs):
        self.value += datum


class Mean(Accumulator):

    name = "mean"
    dependencies = [Sum, Count]

    @property
    def value(self):
        accum_set = self._accum_set
        return accum_set.sum / accum_set.count


def _example():
    import random

    a = Accumulator.Set(Mean, Min, Max)
    n = [random.random() for _ in range(1000)]
    map(a.add, n)
    assert a.min == min(n)
    assert a.max == max(n)
    assert a.count == len(n)
    assert a.sum == sum(n)
    assert a.mean == sum(n) / len(n)
