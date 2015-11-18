import abc

import TransactionsLogic


class SimulationState(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def run(self, simulation):
        """ Run method behaviour depends on simulation state """


class ReadyToRunState(SimulationState):
    """ This is initial simulation state, when conditions are set and simulation can be started """

    def run(self, simulation):
        print('Run at ReadyToRunState')

        # Step 1: Create random exchange points, users and their books
        simulation.generate_items()

        # Step 2: Owners giving their books to Exchange Points
        TransactionsLogic.move_books_from_owners_to_points(simulation)


        simulation.state = ExecutedSimulationState()


class ExecutedSimulationState(SimulationState):
    """ Before consequent run, previous simulation data should be cleaned up """

    def run(self, simulation):
        print('Run at ExecutedSimulationState')
        self.clean_up(simulation)
        simulation.state = ReadyToRunState()
        simulation.run()

    def clean_up(self, simulation):

        simulation.all_books = []
        simulation.all_users = []
        simulation.all_exchange_points = []
        simulation.q_otp.queue.clear()