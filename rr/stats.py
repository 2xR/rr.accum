from .accum import Accumulator


class Min(Accumulator):

    name = "min"
    value = None

    def __init__(self):
        Accumulator.__init__(self)
        self.value = None

    def add(self, datum, weight=None):
        current = self.value
        if current is None or datum < current:
            self.value = datum


class Count(Accumulator):

    name = "count"
    value = None

    def __init__(self):
        Accumulator.__init__(self)
        self.value = 0

    def add(self, datum, weight=None):
        self.value += 1


class Sum(Accumulator):

    name = "sum"
    value = None

    def __init__(self):
        Accumulator.__init__(self)
        self.value = 0.0

    def add(self, datum, weight=None):
        if weight is not None:
            datum *= weight
        self.value += datum


class Mean(Accumulator):

    name = "mean"
    value = None
    dependencies = [Count, Sum]

    def add(self, datum, weight=None):
        pass

    @property
    def value(self):
        accum_set = self._accum_set
        return accum_set.get("sum") / accum_set.get("count")


a = Accumulator.Set(Mean, Min)
