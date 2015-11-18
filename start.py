from BookCircleFacade import BookCircle

book_circle = BookCircle()
book_circle.run_simulation(users_count=2, max_books_per_user=3, exchange_points_count=5)
book_circle.save_simulation_data(commit=False)