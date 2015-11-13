import abc
from common_logger import log

from faker import Faker  # pip package for fake string entities generation


fake = Faker()


class AbstractSimulationItemFactory(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def create_simulation_book(self):
        pass

    @abc.abstractmethod
    def create_simulation_user(self):
        pass

    @abc.abstractmethod
    def create_simulation_item(self):
        pass

    @abc.abstractmethod
    def get_simulation_book_title(self):
        pass

    @abc.abstractmethod
    def get_simulation_user_name(self):
        pass


class SimulationItemFactory(AbstractSimulationItemFactory):
    '''
    This concrete factory produces simulation items with random fake data
    '''

    def create_simulation_book(self):
        return SimulationBook(title=self.get_simulation_book_title())

    def create_simulation_user(self):
        return SimulationUser(name=self.get_simulation_user_name())

    def get_simulation_book_title(self):
        return fake.sentence(nb_words=3)

    def get_simulation_user_name(self):
        return fake.name()

    def create_simulation_item(self, kind):
        if kind == 'book':
            return self.create_simulation_book()
        if kind == 'user':
            return self.create_simulation_user()


class SimulationBookInterface(metaclass=abc.ABCMeta):

    @abc.abstractproperty
    def title(self):
        pass

class SimulationUserInterface:
    ''' Assume interface is there '''
    pass


class SimulationBook(SimulationBookInterface):

    def __init__(self, title):
        log('Instantiated simulation Book with title "%s"' %title)
        self._title = title

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        self._title = value


class SimulationUser:

    def __init__(self, name):
        log('Instantiated simulation User with name "%s"' %name)
        self.name = name
