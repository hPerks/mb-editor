class Cached:
    cached_attrs = []

    def __init__(self):
        self.cache = {}

    def populate_cache(self):
        for attr in self.cached_attrs:
            self.cache[attr] = getattr(self, attr)

    def clear_cache(self):
        self.cache = {}

    def __getattribute__(self, item):
        if item != 'cache' and item in self.cache:
            return self.cache[item]
        return object.__getattribute__(self, item)

    @property
    def cached(self):
        return Cached.Context(self)

    class Context:
        def __init__(self, object):
            self.object = object

        def __enter__(self):
            self.object.populate_cache()

        def __exit__(self, type, value, tb):
            self.object.clear_cache()


__all__ = ['Cached']
