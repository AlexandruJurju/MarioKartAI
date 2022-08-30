from individual import Individual


class Kart(Individual):

    def __init__(self):
        super().__init__()

        self.is_alive = True
        self.won_track = False

        self.fitness = 0
        self.score = 0
        self.distance = 0
        self.time_alive = 0
        self.laps_made = 0

    def calculate_fitness(self):
        return (self.laps_made * 10) * self.distance
