import abc

import flask_app

from StoredItemPrototype import StoredUserPrototype, StoredBookPrototype


class SimulationPersistenceStrategy(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def save_data(self, simulation, **kwargs):
        pass


class SimulationPersistenceFlaskSQL():

    def save_data(self, simulation, **kwargs):

        # Convert models for simulation into models for ORM

        for sim_user in simulation.all_users:
            stored_user = StoredUserPrototype(sim_user).clone()
            flask_app.db.session.add(stored_user)

        for sim_book in simulation.all_books:
            stored_book = StoredBookPrototype(sim_book).clone()
            flask_app.db.session.add(stored_book)

        commit = kwargs.get('commit', True)  # lets prevent real committing to the database

        if commit == True:
            flask_app.db.session.commit()
