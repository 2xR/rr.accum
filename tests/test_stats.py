import math
import random

import pytest
from rr.accum import Accumulator, stats


@pytest.fixture
def accum_and_nums():
    accum = Accumulator.Set(
        stats.Min,
        stats.Max,
        stats.Range,
        stats.Count,
        stats.Sum,
        stats.Mean,
        stats.Variance,
        stats.StandardDeviation,
    )
    nums = [random.random() for _ in range(1000)]
    for n in nums:
        accum.insert(n)
    return accum, nums


def mean(nums):
    return sum(nums) / len(nums)


def var(nums):
    mu = mean(nums)
    return sum((n - mu) ** 2 for n in nums) / (len(nums) - 1)


def stddev(nums):
    return math.sqrt(var(nums))


def test_min(accum_and_nums):
    accum, nums = accum_and_nums
    assert accum.min == min(nums)


def test_max(accum_and_nums):
    accum, nums = accum_and_nums
    assert accum.max == max(nums)


def test_range(accum_and_nums):
    accum, nums = accum_and_nums
    assert accum.range == max(nums) - min(nums)


def test_count(accum_and_nums):
    accum, nums = accum_and_nums
    assert accum.count == len(nums)


def test_sum(accum_and_nums):
    accum, nums = accum_and_nums
    assert accum.sum == sum(nums)


def test_mean(accum_and_nums):
    accum, nums = accum_and_nums
    assert accum.mean == mean(nums)


def test_variance(accum_and_nums):
    accum, nums = accum_and_nums
    assert accum.variance == pytest.approx(var(nums))


def test_standard_deviation(accum_and_nums):
    accum, nums = accum_and_nums
    assert accum.standard_deviation == pytest.approx(stddev(nums))
