import random

class Agent:
    def __init__(self, pos, energy):
        self.pos = pos
        self.energy = energy
        self.alive = True

    def move(self, wind_direction):
        if not self.alive:
            return
        # Simple movement model (replace with your logic)
        dx = random.uniform(-1, 1)
        dy = random.uniform(-1, 1)
        self.pos = (self.pos[0] + dx, self.pos[1] + dy)
