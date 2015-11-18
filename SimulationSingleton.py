import random
import queue

from common_logger import log
from SimulationItems import SimulationItemFactory, ExchangePointProxy, SimulationUser
from BaseClasses.ObserverBaseClasses import ObserverBase
import TransactionsLogic


simulation_item_factory = SimulationItemFactory()


class Single:
    __shared_state = {}

    def __init__(self):
        self.__dict__ = self.__shared_state

    def __str__(self):
        return "Singleton base class"

# Pattern: Singleton

class Simulation(Single):
    """ Singleton managing simulation and storing process data """

    def __init__(self, users_count=None, max_books_per_user=None, exchange_points_count=None):
        # instantiating without args, returns new class instance with the same, shared, namespace
        super().__init__()

        if users_count and max_books_per_user and exchange_points_count:

            log('Simulation singleton instantiated')

            if max_books_per_user < 1:
                raise ValueError('max_books_per_user minimal value is 1, given %i' % max_books_per_user)

            self.all_books = []
            self.all_users = []
            self.all_exchange_points = []
            self.users_count = users_count
            self.max_books_per_user = max_books_per_user  # each user has limited random books amount
            self.exchange_points_count = exchange_points_count
            self.exchange_point_capacity = None
            self.q_otp = queue.Queue()  # otp - from owners to exchange points
            self.persistence_strategy = None


    def generate_items(self):

        log('Items generation...')

        users_observer = UserObserver()

        # generate random users
        for _ in range(self.users_count):
            new_simulation_user = simulation_item_factory.create_simulation_item('user')
            new_simulation_user.attach(users_observer)  # common observer for all users
            self.all_users.append(new_simulation_user)
            user_books_amount = random.randint(1, self.max_books_per_user)

            # for users generate random own books
            for _ in range(0, user_books_amount):
                new_book = simulation_item_factory.create_simulation_item('book')
                new_simulation_user.own_books.append(new_book)
                new_book.owner = new_simulation_user
                self.all_books.append(new_book)

        self.generate_exchange_points()


    def generate_exchange_points(self):

        # generate random exchange points
        last_added_point = None
        for _ in range(self.exchange_points_count):
            new_point = simulation_item_factory.create_simulation_exchange_point(point_capacity=self.exchange_point_capacity)

            if last_added_point:
                new_point.successor = last_added_point  # points chaining

            self.all_exchange_points.append(new_point)
            last_added_point = new_point


    def get_last_exchange_point(self):
        last_point = self.all_exchange_points[-1]
        point_proxy = ExchangePointProxy(proxied_point=last_point)
        return point_proxy

    def __str__(self):
        return "Simulation for users_count %i and max_books_per_user %i and exchange_points_count %i. Total Books %i " \
               % (self.users_count, self.max_books_per_user, self.exchange_points_count, len(self.all_books))

    def set_persistence_strategy(self, persistence_strategy):
        self.persistence_strategy = persistence_strategy

    def save_data(self, **args):
        if self.persistence_strategy:
            self.persistence_strategy.save_data(self, **args)

    def run(self):
        # Step 1: Create random exchange points, users and their books
        self.generate_items()

        # Step 2: Owners giving their books to Exchange Points
        TransactionsLogic.move_books_from_owners_to_points(simulation=self)

class UserObserver(ObserverBase):

    def notification_received(self, sender, notification):
        if notification == SimulationUser.NotificationUserGiveBook:
            user = sender
            user.rating += 1
