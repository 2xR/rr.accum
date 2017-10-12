import collections
import itertools

from .accumulator import Accumulator


class AccumulatorSet(Accumulator):
    """An accumulator set joins together a collection of accumulators, and allows them to use the
    services of other accumulators (i.e. their dependencies) to compute their value on demand.
    AccumulatorSet subclasses Accumulator to allow for nested accumulator structures.

    Individual accumulators are accessed either as attributes or keys in the accumulator set.
    """

    def __init__(self, *accums):
        Accumulator.__init__(self)
        self._accums = collections.OrderedDict()
        self._aliases = {}
        for accum in accums:
            self.add(accum)

    def add(self, accum):
        queue = collections.deque([accum])
        added = []
        while len(queue) > 0:
            accum = queue.popleft()
            if not isinstance(accum, Accumulator) and callable(accum):
                accum = accum()
            if accum.name in self._accums:
                continue
            accum.link(self)
            self._accums[accum.name] = accum
            aliases = accum.aliases
            if callable(aliases):
                aliases = aliases()
            for alias in itertools.chain([accum.name], aliases):
                if alias in self._aliases:
                    raise ValueError("conflicting accumulator alias {!r}".format(alias))
                self._aliases[alias] = accum
            deps = accum.dependencies
            if callable(deps):
                deps = deps()
            queue.extend(deps)
            added.append(accum)
        return added

    def get(self, name):
        return self._aliases[name].value

    __getattr__ = __getitem__ = get

    def __dir__(self):
        return self._aliases.keys()

    def observe(self, datum, **kwargs):
        for accum in self._accums.values():
            accum.observe(datum, **kwargs)

    @property
    def value(self):
        return collections.OrderedDict(
            (name, accum.value)
            for name, accum in self._accums.items()
        )
