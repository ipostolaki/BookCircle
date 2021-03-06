from flask_app import flask_app

from SimulationSingleton import Simulation
from BaseClasses import SimulationPersistenceStrategy

from common_logger import log


# Pattern: Facade

class BookCircle:

    def __init__(self):
        self.simulation = None

    def create_simulation(self, users_count, max_books_per_user, exchange_points_count):
        """ Initialize and run simulation with given conditions """
        self.simulation = Simulation(users_count, max_books_per_user, exchange_points_count)

    def run_simulation(self):
        self.simulation.run()
        log(self.simulation)

    def run_web_app(self):
        flask_app.run()

    def save_simulation_data(self, **kwargs):
        # Save simulation objects to persistent storage

        sql_persistence = SimulationPersistenceStrategy.SimulationPersistenceFlaskSQL()
        self.simulation.set_persistence_strategy(sql_persistence)
        self.simulation.save_data(**kwargs)
