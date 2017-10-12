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
