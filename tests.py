import unittest

from common_logger import log
from SimulationItems import SimulationItemFactory, ExchangePointProxy, PublicLibraryAdapter, PublicLibrary
from StoredItemPrototype import StoredUserPrototype, StoredBookPrototype
from SimulationSingleton import Simulation
import TransactionsLogic
from BaseClasses.ObserverBaseClasses import ObserverBase
from BaseClasses.Resourse import ComputerResource, ComputerResourceImplementor, BookResource, BookResourceImplementor
from BookCircleFacade import BookCircle
from BaseClasses.Composite import ExchangePointsHierarchyComposite, ExchangePointsHierarchyLeaf
from BaseClasses import SimulationState, Mediator


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


class SimulationBookTests(unittest.TestCase):

    def test_owning(self):
        test_user = simulation_item_factory.create_simulation_user()
        test_book = simulation_item_factory.create_simulation_book()
        test_book.owner = test_user

        self.assertEqual(test_book.owner, test_user)


class SimulationTests(unittest.TestCase):

    def test_simulation_singleton(self):

        simulation_a = Simulation()
        simulation_b = Simulation()

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
        exchange_point = simulation_item_factory.create_simulation_exchange_point()
        self.assertTrue(exchange_point.address)

    def test_put_get_book(self):
        exchange_point = simulation_item_factory.create_simulation_exchange_point()

        book = simulation_item_factory.create_simulation_book()
        exchange_point.put_book(book)
        self.assertTrue(len(exchange_point.stored_books) == 1)

        gotten_book = exchange_point.get_book()
        self.assertEqual(gotten_book , book)
        self.assertTrue(len(exchange_point.stored_books) == 0)


class ExchangePointProxyTests(unittest.TestCase):

    def test_points_chaining(self):
        sim = Simulation(users_count=2, max_books_per_user=2, exchange_points_count=3)
        sim.exchange_point_capacity = 5
        sim.generate_items()
        test_point = sim.get_last_exchange_point()

        for _ in range(0,15):
            test_point.put_book(simulation_item_factory.create_simulation_book())

        for point in sim.all_exchange_points:
            self.assertTrue(len(point.stored_books)>0)

    def test_put_get_book(self):
        exchange_point = simulation_item_factory.create_simulation_exchange_point()
        point_proxy = ExchangePointProxy(proxied_point=exchange_point)

        book = simulation_item_factory.create_simulation_book()
        point_proxy.put_book(book)
        self.assertTrue(len(point_proxy.proxied_point.stored_books) == 1)

        gotten_book = point_proxy.get_book()
        self.assertEqual(gotten_book , book)
        self.assertTrue(len(point_proxy.proxied_point.stored_books) == 0)

    def test_full_point(self):
        exchange_point = simulation_item_factory.create_simulation_exchange_point()
        point_proxy = ExchangePointProxy(proxied_point=exchange_point)
        point_proxy.capacity = 10
        books_pool = [simulation_item_factory.create_simulation_book() for book in range(0, int(point_proxy.capacity/2))]

        for book in books_pool:
            point_proxy.put_book(book)

        self.assertTrue(point_proxy.point_is_not_full())


class TransactionsTests(unittest.TestCase):

    def test_otp_execution(self):
        simulation = Simulation(users_count=2, max_books_per_user=2, exchange_points_count=1)
        simulation.generate_items()

        TransactionsLogic.move_books_from_owners_to_points(simulation)
        point = simulation.get_last_exchange_point()
        self.assertTrue(len(point.stored_books) > 0)  # point received some books as result of transaction

        moved_book = point.stored_books[0]
        one_user = simulation.all_users[0]
        self.assertTrue(moved_book not in one_user.own_books)  # user has no book which is moved to exchange point


class ObserverTests(unittest.TestCase):

    TestNotification = 'TestNotification'

    class UserObserver(ObserverBase):
        def notification_received(self, sender, notification):
            if notification == ObserverTests.TestNotification:
                sender.observer_setted_test_flag = True

    def test_concrete_observer(self):

        new_user = simulation_item_factory.create_simulation_user()
        user_observer = ObserverTests.UserObserver()

        new_user.attach(user_observer)
        new_user.notify(ObserverTests.TestNotification)

        self.assertTrue(new_user.observer_setted_test_flag)
        self.assertTrue(ObserverTests.TestNotification in user_observer.received_notifications[new_user])

        new_user.detach(user_observer)
        self.assertTrue(user_observer not in new_user.observers)


class AdapterTests(unittest.TestCase):

    def test_public_library_adapter(self):

        lib = PublicLibrary()
        book = simulation_item_factory.create_simulation_book()
        lib_as_exchange_point = PublicLibraryAdapter(adaptee=lib)
        lib_as_exchange_point.put_book(book)
        gotten_book = lib_as_exchange_point.get_book()

        self.assertTrue(gotten_book, book)


class BridgeTests(unittest.TestCase):

    def test_resources(self):

        book_implementor = BookResourceImplementor()
        book = BookResource(implementor=book_implementor, title='Книга про UTF8', owner='Python3 User')

        book_description = book.get_resource_description()
        log(book_description)

        self.assertTrue(len(book_description)>0)
        self.assertTrue(book.implementor == book_implementor)


        computer_implementor = ComputerResourceImplementor()
        computer = ComputerResource(model='BRDG3', vendor='Pattern Computers', implementor=computer_implementor)

        computer_description = computer.get_resource_description()
        log(computer_description)

        self.assertTrue(len(computer_description)>0)
        self.assertTrue(computer.implementor == computer_implementor)




class CompositeTests(unittest.TestCase):

    def test_composite(self):

        point1 = simulation_item_factory.create_simulation_exchange_point()

        points_of_country = ExchangePointsHierarchyComposite()

        all_points_of_city_A = ExchangePointsHierarchyComposite()
        all_points_of_city_B = ExchangePointsHierarchyComposite()

        points_of_country.add_child(all_points_of_city_A)
        points_of_country.add_child(all_points_of_city_B)

        # Some books at different points in city A
        for _ in range(0, 3):
            new_exchange_point = simulation_item_factory.create_simulation_exchange_point()
            new_book = simulation_item_factory.create_simulation_book()
            new_exchange_point.put_book(new_book)
            all_points_of_city_A.add_child(ExchangePointsHierarchyLeaf(exchange_point=new_exchange_point))


        # Some books at different points in city B
        one_leaf_point_in_city_B = None
        for _ in range(0, 2):
            new_exchange_point = simulation_item_factory.create_simulation_exchange_point()
            new_book = simulation_item_factory.create_simulation_book()
            new_exchange_point.put_book(new_book)

            one_leaf_point_in_city_B = ExchangePointsHierarchyLeaf(exchange_point=new_exchange_point)

            all_points_of_city_B.add_child(one_leaf_point_in_city_B)

        # Pattern: Composite
        # Different components of hierarchy using same interface and able to be accessed with the same method

        log(points_of_country.get_subordinated_books_count())
        log(all_points_of_city_A.get_subordinated_books_count())
        log(all_points_of_city_B.get_subordinated_books_count())
        log(one_leaf_point_in_city_B.get_subordinated_books_count())


class StateTests(unittest.TestCase):

    def test_simulation_state(self):

        book_circle = BookCircle()
        book_circle.create_simulation(users_count=2, max_books_per_user=3, exchange_points_count=5)
        self.assertEqual(type(book_circle.simulation.state), type(SimulationState.ReadyToRunState()))

        book_circle.run_simulation()
        self.assertEqual(type(book_circle.simulation.state), type(SimulationState.ExecutedSimulationState()))


class MediatorTests(unittest.TestCase):

    def test_users_mediation(self):

        # simulation inherit MediatorMixin
        simulation = Simulation(users_count=2, max_books_per_user=2, exchange_points_count=1)
        simulation.generate_items()

        # each user inherit ColleagueMixin
        for user in simulation.all_users:
            user.set_mediator(simulation)

        simulation.broadcast_message_to_colleagues('Broadcasted message')
        user_colleague = simulation.all_users[0]
        user_colleague.send_message_to_mediator('new message')

        self.assertEqual(user_colleague.mediator, simulation)
        self.assertTrue(user_colleague in simulation.colleagues)

if __name__ == "__main__":
    unittest.main()
