from BookCircleFacade import BookCircle

book_circle = BookCircle()
book_circle.create_simulation(users_count=2, max_books_per_user=3, exchange_points_count=5)
book_circle.run_simulation()
book_circle.save_simulation_data(commit=False)