class Single:
    __shared_state = {}

    # print('Single instantiation')

    def __init__(self):
        self.__dict__ = self.__shared_state

    def __str__(self):
        return "Singleton base class"
