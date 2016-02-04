import abc

from common_logger import log


# Pattern: Mediator

class MediatorInterface(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def send_message_to_colleague(self, message):
        pass

    @abc.abstractmethod
    def broadcast_message_to_colleagues(self, message):
        pass

    @abc.abstractmethod
    def register_colleague(self, ):
        pass

    @abc.abstractmethod
    def unregister_colleague(self, colleague):
        pass

    @abc.abstractmethod
    def receive_message_from_colleague(self, message, sender):
        pass


class ColleagueInterface:

    @abc.abstractmethod
    def send_message_to_mediator(self, message):
        pass

    @abc.abstractmethod
    def receive_message_from_mediator(self, message):
        pass

    @abc.abstractmethod
    def set_mediator(self, mediator):
        pass


class MediatorMixin(MediatorInterface):

    colleagues = None

    def __init__(self):
        self.colleagues = []

    def send_message_to_colleague(self, message, colleague):
        colleague.receive_message_from_mediator(self, message)

    def broadcast_message_to_colleagues(self, message):
        for col in self.colleagues:
            col.receive_message_from_mediator(message)

    def register_colleague(self, colleague):
        if not self.colleagues:
            self.colleagues = []

        if colleague not in self.colleagues:
            self.colleagues.append(colleague)

    def unregister_colleague(self, colleague):
        self.colleagues.remove(colleague)

    def receive_message_from_colleague(self, message, sender):
        log('Received message "%s" from colleague %s' % (message, sender))


class ColleagueMixin(ColleagueInterface):

    def __init__(self, mediator):
        self.set_mediator(mediator)

    def send_message_to_mediator(self, message):
        self.mediator.receive_message_from_colleague(sender=self, message=message)

    def receive_message_from_mediator(self, message):
        log('Received message "%s" from mediator' % message)

    def set_mediator(self, mediator):
        self.mediator = mediator
        mediator.register_colleague(self)
