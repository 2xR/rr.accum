# rr.accum - simple, generic accumulator framework for online computations

This simple framework is heavily inspired by the [`boost.accumulators` library](http://www.boost.org/doc/libs/1_64_0/doc/html/accumulators.html).

The idea is to provide a very simple concept of an accumulator, which should be an online computation of some sort, that is assumed to be fairly expensive or to require large amounts of memory. An accumulator sees a stream of data and knows how to update itself (`Accumulator.insert()` method). 

Tying things together to make a group of accumulators easier to use is the concept of accumulator set. An accumulator set groups together a number of accumulators. Since accumulators may declare dependencies, the accumulator set is responsible for using the minimum required set of accumulators to provide a desired set of features. I know I know, this all sounds vague and confusing.

To make things clearer, an example is due. The typical example in this kind of scenario is to use basic descriptive statistics, *e.g.* mean, sum, count, variance. The `rr.accum` library includes these and other simple statistics ready to use.

Suppose we're interested in observing the mean and variance of a stream of numbers. We declare an accumulator set with those two statistics...

```python
from rr.accum import Accumulator, stats

accums = Accumulator.Set(stats.Mean, stats.Variance)
```

We're now ready to start pumping numbers into the accumulator set.
 
```python
import random
 
for _ in range(10000):
    accums.insert(random.random())
    print("Online mean={0.mean] and variance={0.variance]".format(accums))
```

Because of the way accumulator sets work, we've declared that we were interested in mean and variance... (WIP)
