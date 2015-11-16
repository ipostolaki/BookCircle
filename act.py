import flask_app
from StoredItemPrototype import StoredUserPrototype, StoredBookPrototype
from SimulationSingleton import Simulation
from common_logger import log

import TransactionsLogic

#### Step 1: Create random exchange points, users and their books

simulation = Simulation(users_count=2, max_books_per_user=2, exchange_points_count=3)
simulation.generate_items()

#### Step 2: Owners giving their books to Exchange Points

TransactionsLogic.move_books_from_owners_to_points()

# Save generated objects to persistent storage
# Convert models for simulation into models for ORM

for sim_user in simulation.all_users:
    stored_user = StoredUserPrototype(sim_user).clone()
    flask_app.db.session.add(stored_user)

for sim_book in simulation.all_books:
    stored_book = StoredBookPrototype(sim_book).clone()
    flask_app.db.session.add(stored_book)

# app.db.session.commit()

log(simulation)