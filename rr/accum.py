import collections


class Accumulator(object):

    name = "???"
    value = NotImplemented
    dependencies = []

    def __init__(self, name=None, value=None, dependencies=None):
        if name is not None:
            self.name = name
        if value is not None:
            self.value = value
        if dependencies is not None:
            self.dependencies = dependencies
        self._accum_set = None

    def __str__(self):
        return "{}({})".format(self.name, self.value)

    def __repr__(self):
        return "<{} @{:x}>".format(str(self), id(self))

    def link(self, accum_set):
        if self._accum_set is not None:
            raise ValueError("accumulator is already linked to an accumulator set")
        self._accum_set = accum_set

    def add(self, datum, **kwargs):
        pass


class AccumulatorSet(Accumulator):

    def __init__(self, *accums):
        Accumulator.__init__(self)
        self._accums = collections.OrderedDict()
        self.attach(*accums)

    def attach(self, *accums):
        to_attach = collections.deque(accums)
        attached = []
        while len(to_attach) > 0:
            accum = to_attach.popleft()
            if not isinstance(accum, Accumulator) and callable(accum):
                accum = accum()
            if accum.name not in self._accums:
                accum.link(self)
                self._accums[accum.name] = accum
                deps = accum.dependencies
                if callable(deps):
                    deps = deps()
                to_attach.extend(deps)
                attached.append(accum)
        return attached

    def get(self, name):
        return self._accums[name].value

    __getattr__ = __getitem__ = get

    def __dir__(self):
        return self._accums.keys()

    def add(self, datum, **kwargs):
        for accum in self._accums.itervalues():
            accum.add(datum, **kwargs)

    @property
    def value(self):
        return {name: accum.value for name, accum in self._accums.iteritems()}


Accumulator.Set = AccumulatorSet
