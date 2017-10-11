import math
import random

import pytest
from rr.accum import AccumulatorSet, stats


# --------
# Fixtures
# --------

@pytest.fixture
def accumset_and_data():
    accumset = AccumulatorSet(
        stats.Min,
        stats.Max,
        stats.Range,
        stats.Count,
        stats.Sum,
        stats.Mean,
        stats.Variance,
        stats.StandardDeviation,
        stats.Weight,
        stats.WeightedSum,
        stats.WeightedMean,
        stats.WeightedVariance,
        stats.WeightedStandardDeviation,
    )
    sample_size = 10000
    nums = [random.gauss(0, 1) for _ in range(sample_size)]
    weights = [random.uniform(1, 10) for _ in range(sample_size)]
    for num, weight in zip(nums, weights):
        accumset.observe(num, weight=weight)
    return accumset, nums, weights


# -------------------
# Auxiliary functions
# -------------------

def mean(nums):
    return sum(nums) / len(nums)


def var(nums):
    mu = mean(nums)
    return sum((n - mu) ** 2 for n in nums) / (len(nums) - 1)


def stddev(nums):
    return math.sqrt(var(nums))


def wmean(nums, weights):
    return sum(w * n for n, w in zip(nums, weights)) / sum(weights)


def wvar(nums, weights):
    wmu = wmean(nums, weights)
    return sum(w * (n - wmu)**2 for n, w in zip(nums, weights)) / (sum(weights) - 1)


def wstddev(nums, weights):
    return math.sqrt(wvar(nums, weights))


# -----
# Tests
# -----

def test_min(accumset_and_data):
    accumset, nums, weights = accumset_and_data
    assert accumset.min == min(nums)


def test_max(accumset_and_data):
    accumset, nums, weights = accumset_and_data
    assert accumset.max == max(nums)


def test_range(accumset_and_data):
    accumset, nums, weights = accumset_and_data
    assert accumset.range == max(nums) - min(nums)


def test_count(accumset_and_data):
    accumset, nums, weights = accumset_and_data
    assert accumset.count == len(nums)


def test_sum(accumset_and_data):
    accumset, nums, weights = accumset_and_data
    assert accumset.sum == sum(nums)


def test_mean(accumset_and_data):
    accumset, nums, weights = accumset_and_data
    assert accumset.mean == mean(nums)


def test_variance(accumset_and_data):
    accumset, nums, weights = accumset_and_data
    assert accumset.variance == pytest.approx(var(nums))


def test_standard_deviation(accumset_and_data):
    accumset, nums, weights = accumset_and_data
    assert accumset.standard_deviation == pytest.approx(stddev(nums))


def test_weight(accumset_and_data):
    accumset, nums, weights = accumset_and_data
    assert accumset.weight == sum(weights)


def test_weighted_sum(accumset_and_data):
    accumset, nums, weights = accumset_and_data
    assert accumset.weighted_sum == sum(w * n for n, w in zip(nums, weights))


def test_weighted_mean(accumset_and_data):
    accumset, nums, weights = accumset_and_data
    assert accumset.weighted_mean == wmean(nums, weights)


def test_weighted_variance(accumset_and_data):
    accumset, nums, weights = accumset_and_data
    assert accumset.weighted_variance == pytest.approx(wvar(nums, weights))


def test_weighted_standard_deviation(accumset_and_data):
    accumset, nums, weights = accumset_and_data
    assert accumset.weighted_standard_deviation == pytest.approx(wstddev(nums, weights))
