from pgzero.builtins import Actor
from builders import World
from typing import Tuple

class Player:
    def __init__(self, pos: Tuple[float, float], world: World):
        self.actor = Actor('player', pos)
        self.world = world
    
    def move_left(self):
        self.actor.x -= 5
    
    def move_right(self):
        self.actor.x += 5
    
    def draw(self):
        self.actor.draw()