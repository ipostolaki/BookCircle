import abc


class AbstractExchangePointInterface(object):

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def allocate_storage(self):
        """ Will be implemented by concrete exchange point class"""

    @abc.abstractproperty
    def capacity(self):
        """ Will be implemented by concrete exchange point class"""


class SharedExchangePoint(AbstractExchangePointInterface):
    """ Represents model of shared exchange point. Shared means accessible for any person"""

    def __init__(self, storage_capacity):
        self._capacity = storage_capacity
        print('Shared point with capacity %i allocated' % storage_capacity, self)

    def allocate_storage(self):
        pass

    @property
    def capacity(self):
        return self._capacity

    @capacity.setter
    def capacity(self, value):
        self._capacity = value



class PrivateExchangePoint(AbstractExchangePointInterface):
    """ Represents model of private exchange point. Private means restricted access for specific person."""
    def __init__(self, storage_capacity):
        self._capacity = storage_capacity
        print('Private point with capacity %i allocated' % storage_capacity, self)

    def allocate_storage(self):
        pass

    @property
    def capacity(self):
        return self._capacity

    @capacity.setter
    def capacity(self, value):
        self._capacity = value


def create_exchange_point(demanded_point, storage_capacity, *args):
    """
    Factory method instantiating an object of concrete class inherited from AbstractExchangePoint interface
    """

    point = None

    if demanded_point in ['shared', 'SharedExchangePoint']:  # full class name check needed for example in prototype file
        point = SharedExchangePoint(storage_capacity)

    if demanded_point in ['private', 'PrivateExchangePoint']:
        point = PrivateExchangePoint(storage_capacity)

    return point


if __name__ == '__main__':
    create_exchange_point('shared', 10)
    create_exchange_point('private', 5)
