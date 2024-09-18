import random
from pgzero.builtins import *

class Builder:
    def __init__(self, pos):
        self.actor = Actor('builder-left', pos)
        self.y_value = 100
        self.bounce()
    
    def bounce(self):
        self.y_value = -self.y_value
        if self.y_value < 0:
            # moving up
            tween = 'accelerate'
        else:
            # moving down
            tween = 'decelerate'
        self.animation = animate(self.actor, tween, duration=0.2, pos=(self.actor.x, self.actor.y + self.y_value), on_finished=self.reschedule_bounce)

    def reschedule_bounce(self):
        if self.y_value < 0:
            # don't delay falling back down
            self.bounce()
        else:
            # add a slight delay to the next bounce
            clock.schedule(self.bounce, random.random())