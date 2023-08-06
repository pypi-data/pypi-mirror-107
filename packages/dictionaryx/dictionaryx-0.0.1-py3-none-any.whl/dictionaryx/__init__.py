import os
import fnmatch
import msgpack

class DictionaryX(dict):
    """ An Extended Dictionary Resource """
    def __init_subclass__(cls) -> None:
        return super().__init_subclass__()
    
    def __init__(self, store, *args, **kwargs):
        self.store = store
        if os.path.isfile(self.store):
            f = open(self.store, 'rb+')
            self.update(**msgpack.unpackb(f.read(), raw=False))
            f.close()

    def commit(self):
        """ persist the state of a dictionary to disk. """
        f = open(self.store, 'wb+')
        f.write(msgpack.packb(self, use_bin_type=True))
        f.close()
    
    def scan(self, prefix):
        """ returns a list of keys that match the given prefix. """
        matches = []
        for key in self.keys():
            if fnmatch.fnmatch(key, prefix):
                matches.append(key)
        return matches