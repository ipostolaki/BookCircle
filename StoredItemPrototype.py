import abc

from flask_app import StoredBook, StoredUser
from common_logger import log


class StoredItemPrototypeInterface(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def clone(self):
        pass

    @abc.abstractclassmethod
    def __init__(self, item_to_clone):
        pass


class StoredUserPrototype(StoredItemPrototypeInterface):

    def __init__(self, item_to_clone):
        self.item_to_clone = item_to_clone

    def clone(self):
        cloned = StoredUser(username=self.item_to_clone.name)
        log('New StoredUser instance derived from simulation prototype %s', cloned)
        return cloned


class StoredBookPrototype(StoredItemPrototypeInterface):

    def __init__(self, item_to_clone):
        self.item_to_clone = item_to_clone

    def clone(self):
        cloned = StoredBook(title=self.item_to_clone.title)
        log('New StoredBook instance derived from simulation prototype %s', cloned)
        return cloned
