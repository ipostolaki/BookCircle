import abc


# Pattern: Composite

class ExchangePointsHierarchyComponentInterface(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def get_subordinated_books_count(self):
        """ Common Component method, should be implemented both in Composite and Leaf classes """

    @abc.abstractmethod
    def get_subordinated_books_count(self):
        """ Common Component method, should be implemented both in Composite and Leaf classes """

    def add_child(self, child):
        """ should be implemented only in Composite class, not in Leaf """

    def remove_child(self, child):
        """ should be implemented only in Composite Class, not in Leaf """


class ExchangePointsHierarchyComposite(ExchangePointsHierarchyComponentInterface):

    def __init__(self):
        self.children = None

    def add_child(self, child):
        if not self.children:
            self.children = []
        self.children.append(child)

    def remove_child(self, child):
        self.children.remove(child)


    def get_subordinated_books_count(self):

        book_count = 0
        if self.children:
            for child in self.children:
                book_count = book_count + child.get_subordinated_books_count()

        return book_count


class ExchangePointsHierarchyLeaf(ExchangePointsHierarchyComponentInterface):

    def __init__(self, exchange_point):
        self.exchange_point = exchange_point

    def get_subordinated_books_count(self):
        return len(self.exchange_point.stored_books)