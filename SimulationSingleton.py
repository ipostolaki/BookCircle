import random

from common_logger import log
from SimulationItemFactoryModule import SimulationItemFactory


simulation_item_factory = SimulationItemFactory()


class Single:
    __shared_state = {}

    def __init__(self):
        self.__dict__ = self.__shared_state

    def __str__(self):
        return "Singleton base class"


class Simulation(Single):

    def __init__(self, users_count, max_books_per_user, exchange_points_count):
        super().__init__()

        log('Simulation singleton instantiated')

        self.all_books = []
        self.all_users = []
        self.all_exchange_points = []
        self.users_count = users_count
        self.max_books_per_user = max_books_per_user  # each user has limited random books amount
        self.exchange_points_count = exchange_points_count

        if max_books_per_user < 1:
            raise ValueError('max_books_per_user minimal value is 1, given %i' % max_books_per_user)


    def generate_items(self):

        log('Items generation...')

        # generate random users
        for _ in range(self.users_count):
            new_simulation_user = simulation_item_factory.create_simulation_item('user')
            self.all_users.append(new_simulation_user)
            user_books_amount = random.randint(1, self.max_books_per_user)

            # for users generate random own books
            for _ in range(0, user_books_amount):
                new_book = simulation_item_factory.create_simulation_item('book')
                new_simulation_user.own_books.append(new_book)
                self.all_books.append(new_book)

        # generate random exchange points
        for _ in range(self.exchange_points_count):
            new_point = simulation_item_factory.create_simulation_item('point')
            self.all_exchange_points.append(new_point)


    def __str__(self):
        return "Simulation for users_count %i and max_books_per_user %i and exchange_points_count %i. Total Books %i " \
               % (self.users_count, self.max_books_per_user, self.exchange_points_count, len(self.all_books))