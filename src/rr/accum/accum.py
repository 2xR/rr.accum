class Accumulator(object):

    name = "???"
    aliases = []
    value = NotImplemented
    dependencies = []

    def __init__(self, name=None, aliases=None, value=None, dependencies=None):
        if name is not None:
            self.name = name
        if aliases is not None:
            self.aliases = aliases
        if value is not None:
            self.value = value
        if dependencies is not None:
            self.dependencies = dependencies
        self._accum_set = None

    def __str__(self):
        return "{}({}: {})".format(type(self).__name__, self.name, self.value)

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
        self._distinct_accums = []
        self._accums_map = {}
        self.attach(*accums)

    def attach(self, *accums):
        accums_list = self._distinct_accums
        accums_map = self._accums_map
        to_attach = list(accums)
        attached = []
        while len(to_attach) > 0:
            accum = to_attach.pop(0)
            if not isinstance(accum, Accumulator) and callable(accum):
                accum = accum()
            if accum.name not in accums_map:
                accum.link(self)
                accums_list.append(accum)
                accums_map[accum.name] = accum
                aliases = accum.aliases
                if callable(aliases):
                    aliases = aliases()
                for alias in aliases:
                    if alias not in accums_map:
                        accums_map[alias] = accum

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
        return self._aliases.keys()

    def add(self, datum, **kwargs):
        for accum in self._accums.itervalues():
            accum.add(datum, **kwargs)

    @property
    def value(self):
        return {name: accum.value for name, accum in self._accums.iteritems()}


Accumulator.Set = AccumulatorSet
