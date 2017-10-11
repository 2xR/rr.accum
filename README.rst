========
rr.accum
========

-----------------------------------------------------------
Simple, generic accumulator library for online computations
-----------------------------------------------------------

This simple library is heavily inspired by the `boost.accumulators library <http://www.boost.org/doc/libs/1_64_0/doc/html/accumulators.html>`_.

The library builds on two basic concepts:

1. An **accumulator** represents an online computation of some sort, that is assumed to be fairly expensive or to require large amounts of memory. An accumulator sees a stream of data and knows how to update itself incrementally (`Accumulator.insert()` method).

2. **Accumulator sets** tie things together and make it easier to use a set of related accumulators. Accumulator sets manage the dependencies of accumulators on other accumulators, and provide an attribute-like interface to access the current values of its constituent accumulators.

I know I know, this all sounds vague and confusing... To make things clearer, an example is due. The typical example in this kind of scenario is to use basic descriptive statistics, *e.g.* mean, sum, count, variance. The `rr.accum` library includes these and other simple statistics ready to use.

Suppose we're interested in observing the mean and variance of a stream of numbers. We declare an accumulator set with those two statistics:

.. code-block:: python

    from rr.accum import Accumulator, stats

    accums = Accumulator.Set(stats.Mean, stats.Variance)

We're now ready to start pumping numbers into the accumulator set:

.. code-block:: python

    import random

    for _ in range(10000):
        accums.insert(random.random())
        print("Online mean={0.mean} and variance={0.variance}".format(accums))

Because of the way accumulator sets work, we've declared that we were interested in mean and variance... (WIP)


Installation
============

From the github repo:

.. code-block:: bash

    pip install git+https://github.com/2xR/rr.accum.git
