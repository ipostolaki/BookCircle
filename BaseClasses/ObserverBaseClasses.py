import abc


# Pattern: Observer

class ObservableSubjectBase():

    observers = None  # default for new instances

    def attach(self, observer):
        if not self.observers:
            self.observers = []
        self.observers.append(observer)

    def detach(self, observer):
        try:
            self.observers.remove(observer)
        except ValueError:
            print('No observer to remove: ', observer)

    def notify(self, notification):
        for observer in self.observers:
            observer.update(sender=self, notification=notification)


class ObserverBase(metaclass=abc.ABCMeta):

    def __init__(self):
        self.received_notifications = {}

    def update(self, sender, notification):
        if sender in self.received_notifications:
            self.received_notifications[sender].append(notification)
        else:
            self.received_notifications[sender] = [notification]

        self.notification_received(sender, notification)

    @abc.abstractmethod
    def notification_received(self, sender, notification):
        pass