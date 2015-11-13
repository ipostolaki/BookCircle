from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand


app = Flask(__name__)
app.secret_key = 'fhdjksfh7h38h3489fh3489fh3489hf938h'

# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://ipostolaki@localhost/Books'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)


@app.route('/')
def index():
    pass

    return 'Hi there'



#### Models

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))

    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    holder_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    own_books = db.relationship(Book, backref='owner', lazy='dynamic', foreign_keys=[Book.owner_id])
    holded_books = db.relationship(Book, backref='holder', lazy='dynamic', foreign_keys=[Book.holder_id])



if __name__ == '__main__':
    manager.run()

    


