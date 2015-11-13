import unittest

from SimulationItemFactoryModule import SimulationItemFactory
from StoredItemPrototype import StoredUserPrototype, StoredBookPrototype
from SimulationSingleton import Simulation


simulation_item_factory = SimulationItemFactory()


class PrototypeTests(unittest.TestCase):

    def test_user_clone(self):

        simulation_user = simulation_item_factory.create_simulation_user()
        stored_user = StoredUserPrototype(simulation_user).clone()
        self.assertEqual(simulation_user.name, stored_user.username)

    def test_book_clone(self):

        simulation_book = simulation_item_factory.create_simulation_book()
        stored_book = StoredBookPrototype(simulation_book).clone()
        self.assertEqual(simulation_book.title, stored_book.title)


class SimulationUserTests(unittest.TestCase):

    def test_own_books(self):
        sim_book = simulation_item_factory.create_simulation_book()
        books_list = [sim_book]
        sim_user = simulation_item_factory.create_simulation_user()
        sim_user.own_books = books_list

        self.assertTrue(sim_book in sim_user.own_books)
        
        
class SimulationTests(unittest.TestCase):

    def test_simulation_singleton(self):

        simulation_a = Simulation(users_count=3, max_books_per_user=3, exchange_points_count=5)
        simulation_b = Simulation(users_count=3, max_books_per_user=3, exchange_points_count=5)

        simulation_a.common_data = 'test data'

        self.assertEqual(simulation_a.common_data, simulation_b.common_data)


    def test_generate_items(self):
        simulation = Simulation(users_count=3, max_books_per_user=3, exchange_points_count=5)
        simulation.generate_items()
        self.assertTrue(len(simulation.all_books) > 0)
        self.assertTrue(len(simulation.all_users) > 0)
        self.assertTrue(len(simulation.all_exchange_points) > 0)


class SimulationExchangePointTests(unittest.TestCase):
    
    def test_point_creation(self):
        exchange_point =  simulation_item_factory.create_simulation_exchange_point()
        self.assertTrue(exchange_point.address)






if __name__ == "__main__":
    unittest.main()



