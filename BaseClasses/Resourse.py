import abc


# Pattern: Bridge

class ResourceAbstractClass(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def __init__(self, implementor):
        pass

    @abc.abstractmethod
    def get_resource_description(self):
        pass


class ResourceImplementorInterface(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def get_resource_description(self, resource):
        pass


#### Book Resource

class BookResource(ResourceAbstractClass):

    def __init__(self, title, owner, implementor):
        self.implementor = implementor
        self.title = title
        self.owner = owner

    def get_resource_description(self):
        return self.implementor.get_resource_description(self)


class BookResourceImplementor(ResourceImplementorInterface):

    def get_resource_description(self, book_resource):
        return "This book with title '%s' belongs to %s" % (book_resource.title, book_resource.owner)


#### Computer Resource


class ComputerResource(ResourceAbstractClass):

    def __init__(self, model, vendor, implementor):
        self.implementor = implementor
        self.model = model
        self.vendor = vendor

    def get_resource_description(self):
        return self.implementor.get_resource_description(self)


class ComputerResourceImplementor(ResourceImplementorInterface):

    def get_resource_description(self, computer_resource):
        return "This computer of model '%s' is produced by '%s'" % (computer_resource.model, computer_resource.vendor)
