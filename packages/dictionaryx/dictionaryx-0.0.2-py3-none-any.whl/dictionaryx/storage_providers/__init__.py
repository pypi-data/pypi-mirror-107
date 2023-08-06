import os
import io

class StorageProvider:
    """ The base class that provides storage methods for all StorageProviders. """
    def __init__(self):
        pass

    def commit(self):
        raise NotImplementedError("you must implement a commit method")
    
    def __del__(self):
        pass

class InMemory(StorageProvider):
    def __init_subclass__(cls) -> None:
        return super().__init_subclass__()
    
    def __init__(self):
        """ setup the storage provider. """
        self.fp = io.BytesIO()
    
    def load(self):
        """ load the state """
        return None

    def commit(self, state: bytes):
        """ commit the state of the dictionary. """
        self.fp.write(state)

    def __del__(self):
        """ teardown the storage provider. """
        self.fp.close()

class LocalFile(StorageProvider):
    def __init_subclass__(cls) -> None:
        return super().__init_subclass__()
    
    def __init__(self, path):
        """ setup the storage provider. """
        self.path = path
    
    def load(self):
        """ load the state """
        if os.path.isfile(self.path):
            f = open(self.path, 'rb+')
            return f.read()

    def commit(self, state: bytes):
        """ commit the state of the dictionary. """
        self.fp = open(self.path, 'wb+')
        self.fp.write(state)
        self.fp.close()

    def __del__(self):
        """ teardown the storage provider. """
        pass