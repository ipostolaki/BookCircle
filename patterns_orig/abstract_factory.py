class Identifiable(object):

    @classmethod
    def identified_instance(cls):
        """
        Abstract Factory
        Common identification logic during creation of different classes.
        Creates class instances counting and identifying them.
        """

        cls.id_counter += 1
        return cls(id=cls.id_counter)


class Book(Identifiable):
    id_counter = 0  # class shared

    def __init__(self, id):
        self.id = id


class User(Identifiable):
    id_counter = 0  # class shared

    def __init__(self, id):
        self.id = id


if __name__ == '__main__':

    ### Books

    b = Book.identified_instance()
    print(b.id)

    b2 = Book.identified_instance()
    print(b2.id)

    b3 = Book.identified_instance()
    print(b3.id)


    ### Users

    u = User.identified_instance()
    print(u.id)

    u2 = User.identified_instance()
    print(u2.id)

    u3 = User.identified_instance()
    print(u3.id)