from math import inf, nan, sqrt

from .accumulator import Accumulator, GeneratorBasedAccumulator


class Min(Accumulator):

    name = "min"
    value = +inf

    def observe(self, datum, **kwargs):
        if datum < self.value:
            self.value = datum


class Max(Accumulator):

    name = "max"
    value = -inf

    def observe(self, datum, **kwargs):
        if datum > self.value:
            self.value = datum


class Range(Accumulator):

    name = "range"
    dependencies = [Min, Max]
    value = nan

    @property
    def value(self):
        accum_set = self._accum_set
        return accum_set.max - accum_set.min


class Count(Accumulator):

    name = "count"
    value = 0

    def observe(self, datum, **kwargs):
        self.value += 1


class Weight(Accumulator):

    name = "weight"
    value = 0.0

    def observe(self, datum, weight=1, **kwargs):
        self.value += weight


class Sum(Accumulator):

    name = "sum"
    value = 0.0

    def observe(self, datum, **kwargs):
        self.value += datum


class WeightedSum(Accumulator):

    name = "weighted_sum"
    aliases = ["wsum"]
    value = 0.0

    def observe(self, datum, weight=1, **kwargs):
        self.value += datum * weight


WSum = WeightedSum


class Mean(Accumulator):

    name = "mean"
    dependencies = [Sum, Count]

    @property
    def value(self):
        accum_set = self._accum_set
        n = accum_set.count
        s = accum_set.sum
        return nan if n == 0 else s / n


class WeightedMean(Accumulator):

    name = "weighted_mean"
    aliases = ["wmean"]
    dependencies = [WeightedSum, Weight]

    @property
    def value(self):
        accum_set = self._accum_set
        w = accum_set.weight
        s = accum_set.weighted_sum
        return nan if w == 0 else s / w


WMean = WeightedMean


class Variance(GeneratorBasedAccumulator):
    """Implementation of online variance statistic, taken from
    https://en.wikipedia.org/wiki/Algorithms_for_calculating_variance#Online_algorithm
    """

    name = "variance"
    aliases = ["var"]

    def observer(self):
        n = 0
        mean = 0.0
        M2 = 0.0
        var = nan
        while True:
            datum, kwargs = (yield var)  # yield current value and receive next observation
            n += 1
            delta = datum - mean
            mean += delta / n
            delta2 = datum - mean
            M2 += delta * delta2
            if n > 1:
                var = M2 / (n - 1)


Var = Variance


class WeightedVariance(GeneratorBasedAccumulator):
    """Implementation of online weighted variance statistic, taken from
    https://en.wikipedia.org/wiki/Algorithms_for_calculating_variance#Weighted_incremental_algorithm

    Note:
        This implementation uses Bessel's correction for sample variance with frequency weights.
        However, there is also weighted population variance (no correction) and a different
        correction for reliability weights. These use the exact same algorithm but compute the
        variance using slightly different expressions.
    """

    name = "weighted_variance"
    aliases = ["wvar"]

    def observer(self):
        wSum = 0.0
        wSum2 = 0.0
        mean = 0.0
        S = 0.0
        wVar = nan
        while True:
            datum, kwargs = (yield wVar)  # yield current value and receive next observation
            w = kwargs.get("weight", 1)
            wSum = wSum + w
            wSum2 = wSum2 + w * w
            meanOld = mean
            mean = meanOld + (w / wSum) * (datum - meanOld)
            S = S + w * (datum - meanOld) * (datum - mean)
            if wSum > 1:
                wVar = S / (wSum - 1)  # sample variance with frequency weights


WVar = WeightedVariance


class StandardDeviation(Accumulator):

    name = "standard_deviation"
    aliases = ["stddev"]
    dependencies = [Variance]

    @property
    def value(self):
        return sqrt(self._accum_set.variance)


StdDev = StandardDeviation


class WeightedStandardDeviation(Accumulator):

    name = "weighted_standard_deviation"
    aliases = ["wstddev"]
    dependencies = [WeightedVariance]

    @property
    def value(self):
        return sqrt(self._accum_set.weighted_variance)


WStdDev = WeightedStandardDeviation
