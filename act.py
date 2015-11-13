import app

user = app.User(username='the user 3')
print(user)

book = app.Book(title='title', owner=user)
print(book)
print(book.owner)

app.db.session.add(user)
app.db.session.add(book)

app.db.session.commit()
