from abc import abstractmethod


class Individual:
    def __init__(self):
        pass

    @abstractmethod
    def calculate_fitness(self):
        raise NotImplemented

    @property
    def fitness(self):
        raise NotImplemented
