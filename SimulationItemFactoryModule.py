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
        '''
        The Factory Method for items production
        '''
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

    def create_simulation_exchange_point(self, point_capacity=None):
        return SimulationExchangePoint(address=self.get_simulation_exchange_point_address(), point_capacity=point_capacity)

    def get_simulation_book_title(self):
        return fake.sentence(nb_words=3)

    def get_simulation_exchange_point_address(self):
        return fake.address()

    def get_simulation_user_name(self):
        return fake.name()

    def create_simulation_item(self, kind):
        if kind == 'book':
            return self.create_simulation_book()
        if kind == 'user':
            return self.create_simulation_user()
        if kind == 'point':
            return self.create_simulation_exchange_point()


class SimulationBookInterface(metaclass=abc.ABCMeta):

    @abc.abstractproperty
    def title(self):
        pass


class SimulationUserInterface:
    ''' Assume interface is there '''
    pass


class SimulationExchangePointInterface(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def put_book(self):
        pass

    @abc.abstractmethod
    def get_book(self):
        pass


class SimulationBook(SimulationBookInterface):

    def __init__(self, title, owner=None):
        log('Instantiated simulation Book with title "%s"' %title)
        self._title = title
        self.owner = owner

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
        self._own_books = []
        self.rating = 1

    @property
    def own_books(self):
        # log('User\'s \'%s\' books accessed' % self.name)
        return self._own_books

    @own_books.setter
    def own_books(self, value):
        # log('User\'s \'%s\' books setted' % self.name)
        self._own_books = value


class SimulationExchangePoint(SimulationExchangePointInterface):
    ''' Respresentation of shared physical space where users can exchange their books '''

    default_capacity = 10

    def __init__(self, address, point_capacity=None):
        self.address = address
        self.stored_books = []
        self.capacity = point_capacity or SimulationExchangePoint.default_capacity
        self.successor = None

        log('Instantiated simulation Exchange Point with address "%s" and capacity %i'\
            %(address, self.capacity))

    def put_book(self, book):
        self.stored_books.append(book)

    def get_book(self):
        return self.stored_books.pop()

    def set_successor(self, successor):
        self.successor = successor


class ExchangePointProxyInterface(SimulationExchangePointInterface, metaclass=abc.ABCMeta):
    pass


class ExchangePointProxy(ExchangePointProxyInterface):

    # Pattern: Proxy

    def __init__(self, proxied_point):
        self.proxied_point = proxied_point

    def get_book(self):
        if self.proxied_point.stored_books:
            return self.proxied_point.stored_books.pop()

    def put_book(self, book):

        # Pattern: Chain of Responsibility

        if self.point_is_not_full():
            self.proxied_point.put_book(book)
        else:
            successor_point = self.proxied_point.successor

            log('Trying exchange point successor %s' %successor_point)

            if successor_point:
                self.proxied_point = successor_point
                self.put_book(book)
            else:
                raise Exception("Can't add book %s, whole chain of exchange points is full." % book)

    def point_is_not_full(self):
        return self.proxied_point.capacity > len(self.proxied_point.stored_books)

    @property
    def stored_books(self):
        return self.proxied_point.stored_books