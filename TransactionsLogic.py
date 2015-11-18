import abc

from common_logger import log


class Transaction:

    def __init__(self, book_to_transmit, book_destination, book_source=None):
        self.book_to_transmit = book_to_transmit
        self.book_destination = book_destination
        self.book_source = book_source


class QueueExecutorBase(metaclass=abc.ABCMeta):

    def __init__(self, queue):
        self.queue = queue

    # Pattern: Template Method
    def run(self):
        while not self.queue.empty():
            trn = self.queue.get()
            self.execute_transaction(trn)

    @abc.abstractmethod
    def execute_transaction(self, transaction):
        """ This sub method will be overridden differently for specific queues """


class OTPQueueExecutor(QueueExecutorBase):
    """ otp - from owners to exchange points """

    def execute_transaction(self, transaction):
        log('Execute transaction %s at otp queue %s' %(transaction, self.queue))

        book = transaction.book_to_transmit

        transaction.book_destination.put_book(book)
        book.owner.give_own_book(book)


def move_books_from_owners_to_points(simulation):

    users_own_books = []

    # get all own books of users
    for user in simulation.all_users:
        for book in user.own_books:
            users_own_books.append(book)

    # prepare list of transactions, to move books from owners, to exchange points
    for book in users_own_books:
        trn = Transaction(book_to_transmit=book, book_destination=simulation.get_last_exchange_point())
        simulation.q_otp.put(trn)

    execution = OTPQueueExecutor(queue=simulation.q_otp)
    execution.run()