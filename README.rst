========
rr.accum
========

-----------------------------------------------------------
Simple, generic accumulator library for online computations
-----------------------------------------------------------

This simple library is heavily inspired by the `boost.accumulators library <http://www.boost.org/doc/libs/1_64_0/doc/html/accumulators.html>`_.

The library builds on two basic concepts:

1. An **accumulator** represents an online computation of some sort, that is assumed to be fairly expensive or require large amounts of memory. An accumulator observes a stream of data and knows how to update itself incrementally (`Accumulator.observe()` method).

2. **Accumulator sets** tie things together and make it easier to use a set of related accumulators. Accumulator sets manage the dependencies of accumulators on other accumulators, and provide an attribute-like interface to access the current values of its constituent accumulators.

I know I know, this all sounds vague and confusing... To make things clearer, an example is due. The typical example in this kind of scenario is to use basic descriptive statistics, *e.g.* mean, sum, count, variance. The `rr.accum` library includes these and other simple statistics ready to use.

Suppose we're interested in observing the mean and variance of a stream of numbers. We declare an accumulator set with those two statistics:

.. code-block:: python

    from rr.accum import AccumulatorSet, stats

    accums = AccumulatorSet(stats.Mean, stats.Variance, name="foo")
    accums.value  # check initial values

We can immediately inspect the initial values, and be surprised to find out that the set includes two statistics that we didn't request: `sum` and `count`. These were added automatically by the accumulator set because the mean depends on the sum and count.

.. warning:: Always list the desired statistics explicitly when creating accumulator sets.

    This not only makes your code clearer, but also guarantees that those statistics will be available. Relying on implicit dependencies may suddenly stop working if a statistic's implementation changes and it stops depending on others.

Okay, we are now ready to start pumping numbers into the accumulator set:

.. code-block:: python

    import random

    for _ in range(10000):
        accums.observe(random.random())
        print("Online mean={} and variance={}".format(accums.mean, accums["variance"]))

The current value of individual statistics can be obtained either through attribute access or subscripting, by passing the statistic's name or one of its aliases. Some accumulators, like `WeightedStandardDeviation`, have shorter aliases (`wstddev`) for convenience.


Compatibility
=============

Developed and tested in Python 3.6+. The code may or may not work under earlier versions of Python 3 (perhaps back to 3.3).


Installation
============

From the github repo:

.. code-block:: bash

    pip install git+https://github.com/2xR/rr.accum.git


License
=======

This library is released as open source under the MIT License.

.. centered:: Copyright (c) 2017 Rui Rei
