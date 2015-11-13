import abc
import copy

import factory_method


class PrototypeInterface():

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def clone(self):
        """ Defines required interface for derived classes """


class PointPrototypeA(PrototypeInterface):

    @staticmethod
    def clone(orig):
        original_point_kind = orig.__class__.__name__
        original_point_capacity = orig.capacity
        cloned_point = factory_method.create_exchange_point(original_point_kind, original_point_capacity)
        return cloned_point


class PointPrototypeB(PrototypeInterface):
    """ Prototype cloning using python copy module """

    @staticmethod
    def clone(orig):
        return copy.deepcopy(orig)


orig_point = factory_method.PrivateExchangePoint(10)

new_point = PointPrototypeA.clone(orig_point)

print('Clones have identical class', orig_point.__class__, orig_point.__class__ == new_point.__class__)
print('Clones have identical capacity', orig_point.capacity, orig_point.capacity == new_point.capacity)

new_point2 = PointPrototypeB.clone(orig_point)
print('new_point2', new_point2)
