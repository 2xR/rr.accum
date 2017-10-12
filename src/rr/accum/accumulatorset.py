import collections
import itertools

from .accumulator import Accumulator


class AccumulatorSet(Accumulator):
    """An accumulator set joins together a collection of accumulators, and allows them to use the
    services of other accumulators (i.e. their dependencies) to compute their value on demand.
    AccumulatorSet subclasses Accumulator to allow for nested accumulator structures.

    Individual accumulators are accessed either as attributes or keys in the accumulator set.
    """

    def __init__(self, *accums, **kwargs):
        Accumulator.__init__(self, **kwargs)
        self._index = {}  # identifier (name/alias) => accumulator map
        self._accums = []  # list of accumulators belonging to this accumset
        if len(accums) > 0:
            self.add(*accums)

    def add(self, *accums):
        added = []
        queue = collections.deque(accums)
        names = {a.name for a in self._accums}
        while len(queue) > 0:
            accum = queue.popleft()
            if not isinstance(accum, Accumulator):
                accum = resolve(accum)
            if accum.name in names:
                continue
            names.add(accum.name)
            accum.link(self)
            self._accums.append(accum)
            for identifier in itertools.chain([accum.name], resolve(accum.aliases)):
                if identifier in self._index:
                    raise NameError("duplicate accumulator identifier {!r}".format(identifier))
                self._index[identifier] = accum
            queue.extend(resolve(accum.dependencies))
            added.append(accum)
        return added

    def get(self, identifier):
        return self._index[identifier].value

    __getattr__ = __getitem__ = get

    def __dir__(self):
        return self._index.keys()

    def __iter__(self):
        return iter(self._accums)

    def __len__(self):
        return len(self._accums)

    def observe(self, datum, **kwargs):
        for accum in self._accums:
            accum.observe(datum, **kwargs)

    @property
    def value(self):
        return collections.OrderedDict((a.name, a.value) for a in self._accums)


def resolve(x):
    """Return the result of calling `x` with no arguments if it is a callable, otherwise simply
    return `x`.
    """
    return x() if callable(x) else x
