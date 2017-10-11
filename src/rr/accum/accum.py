import collections
import itertools


class Accumulator:
    """An accumulator represents a quantity/value that is computed from a stream of data,
    i.e. in an online fashion. Accumulators can be used standalone, but are typically used
    through an accumulator set. See `rr.accum.stats` for examples of statistical accumulators.
    """

    name = "???"
    aliases = []
    dependencies = []
    value = NotImplemented

    def __init__(self, name=None, aliases=None, dependencies=None, value=None):
        if name is not None:
            self.name = name
        if aliases is not None:
            self.aliases = aliases
        if dependencies is not None:
            self.dependencies = dependencies
        if value is not None:
            self.value = value
        self._accum_set = None

    def __str__(self):
        return "{}({}: {})".format(type(self).__name__, self.name, self.value)

    def __repr__(self):
        return "<{} @{:x}>".format(str(self), id(self))

    def link(self, accum_set):
        """Link this accumulator to a parent accumulator set.

        The parent can be used to obtain the values of this accumulator's dependencies.
        """
        if self._accum_set is not None:
            raise ValueError("accumulator is already linked to an accumulator set")
        self._accum_set = accum_set

    def observe(self, datum, **kwargs):
        pass


class GeneratorBasedAccumulator(Accumulator):
    """Base class for accumulators that are better described as generators (`.observer()` method).

    Observations are passed to the generator through the `.send()` method as `(datum, kwargs)`
    pairs, and the generator should yield the updated value of the accumulator.
    """

    def __init__(self, *args, **kwargs):
        Accumulator.__init__(self, *args, **kwargs)
        self._observer = self.observer()  # create the generator object
        self.value = next(self._observer)  # and start it, receiving the initial value

    def observe(self, datum, **kwargs):
        self.value = self._observer.send((datum, kwargs))

    def observer(self):
        raise NotImplementedError()


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


# Provide aliases for GeneratorBasedAccumulator and AccumulatorSet through the Accumulator class.
# This way users don't have to import additional symbols. Less namespace littering ;)
Accumulator.Set = AccumulatorSet
Accumulator.GeneratorBased = GeneratorBasedAccumulator
