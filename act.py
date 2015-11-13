import app
import SimulationItemFactory as sf

#### Step 1: create random users and their books

simulation_factory = sf.SimulationItemFactory()

items_count = 10

books = []
users = []


for i in range(items_count):

    simulation_book = simulation_factory.create_simulation_item('book')
    books.append(simulation_book)


    simulation_user = simulation_factory.create_simulation_item('user')
    users.append(simulation_user)


for sim_book in books:
    stored_book = app.StoredBook(title=sim_book.title)
    app.db.session.add(stored_book)


app.db.session.commit()
