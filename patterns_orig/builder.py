import abc
import warnings

import factory_method


class PointBuilderInterface:
    """ This builder could be used to create new ExchangePoint in cases when \
     initialization data is provided step by step, but not at once"""

    __metaclass__ = abc.ABCMeta

    @abc.abstractproperty
    def stored_books(self):
        pass

    @abc.abstractproperty
    def name(self):
        pass

    @abc.abstractproperty
    def capacity(self):
        pass

    @abc.abstractproperty
    def point_kind(self):
        """ Kind of point which will be passed to factory method  """

    @abc.abstractproperty
    def made_point(self):
        """ Returns point constructed from collected data """

### Methods

    @abc.abstractmethod
    def build_point(self):
        pass


class ComplexPointBuilder(PointBuilderInterface):

    def __init__(self):
        self._stored_books = None
        self._capacity = None
        self._name = None
        self._point_kind = None

        self._made_point = None

    @property
    def stored_books(self):
        return self._stored_books

    @stored_books.setter
    def stored_books(self, value):
        self._stored_books = value


    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value


    @property
    def capacity(self):
        return self._capacity

    @capacity.setter
    def capacity(self, value):
        self._capacity = value


    @property
    def point_kind(self):
        return self._point_kind

    @point_kind.setter
    def point_kind(self, value):
        self._point_kind = value


    @property
    def made_point(self):
        return self._made_point

### Methods

    def build_point(self):

        if self._point_kind and self._capacity and self._name and self._stored_books:
            self._made_point = factory_method.create_exchange_point(self._point_kind,
                                                                    self._capacity,
                                                                    self._name,
                                                                    self._stored_books
                                                                    )
        else:
            warnings.warn('ExchangePoint not builded, insufuccient initialization data provided')

        return self._made_point





def main():
    # Create the builder
    # Provide data and get created object
    # This process, in GOF context, conventionally named 'Building Direction'
    point_builder = ComplexPointBuilder()
    point_builder.capacity = 10
    point_builder.name = 'Point name'
    point_builder.stored_books = ['a','b','c']
    point_builder.point_kind = 'shared'
    point_builder.build_point()

    print(point_builder.made_point)
