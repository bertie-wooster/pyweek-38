#physics for stackable blocks
from pgzero.builtins import *
import random

WIDTH=800
HEIGHT=600

blocks = []

right_ladders=[]

right_stone = []
left_stone = []

left_ladders=[]

class Block:
    def __init__(self, actor, collum, mass, hides_view):
        self.side = 50
        self.mass = mass
        self.hides_view = hides_view
        self.damaged = False
        self.fall = False
        self.actor = actor
        self.collum = collum
        self.second_clock = 0

    def draw(self):
        self.actor.draw()

    def update(self, rt):
        if self.mass == 100:
            for block in self.collum:
                if block is not self:
                    if self.actor.distance_to(block.actor.pos) < 50:
                        pass
                    else:
                        self.fall = True
            if self.fall:
                self.fall_down()
            blocks_above = []
            if self.damaged:
                self.actor.image = 'block_grey_damaged'
                for block in self.collum:
                    if block is not self:
                        if block.actor.y < self.actor.y:
                            blocks_above.append(block)

                if len(blocks_above) >= 3:
                    blocks.remove(self)
                    self.collum.remove(self)
                    self.create_rubble(3, random.choice(['rubble_stone_1', 'rubble_stone_1', 'rubble_stone_1']))
                    for block in blocks_above:
                        block.fall = True
        else:
            if self.damaged:
                for block in list(self.collum):
                    if block is not self:
                        if block.actor.y < self.actor.y:
                            block.create_rubble(3, random.choice(['rubble_ladder_1', 'rubble_ladder_2', 'rubble_ladder_3']))
                            blocks.remove(block)
                            self.collum.remove(block)
                self.create_rubble(3, random.choice(['rubble_ladder_1', 'rubble_ladder_2', 'rubble_ladder_3']))
                blocks.remove(self)
                self.collum.remove(self)

    def create_rubble(self, intensity, image):
        for i in range(2**intensity):
            rubble = Rubble(Actor('rubble_ladder_1', (self.actor.x, self.actor.y - 15)), size = intensity, image=image)
            rubbles.append(rubble)

    def fall_down(self):
        self.actor.y += 2
        for block in self.collum:
            if block is not self:
                if self.actor.colliderect(block.actor):
                    if block.fall != True:
                        self.fall = False
                        self.actor.y = block.actor.y - 50
                        return
        if self.actor.y >= HEIGHT - 105:
            self.fall = False
            self.actor.y = HEIGHT - 105
            return

    @classmethod
    def place_stone(cls, x, y, collum):
        stone = Block(Actor('block_grey', (x, y)), collum, mass=100, hides_view=True)
        blocks.append(stone)
        return stone

    @classmethod
    def place_ladder(cls, x, y, collum):
        ladder = Block(Actor('ladder', (x, y)), collum, mass=20, hides_view=False)
        blocks.append(ladder)
        return ladder

rubbles=[]
class Rubble:
    def __init__(self, actor, size, image):
        self.actor = actor
        self.start_y = self.actor.y
        self.actor.image = image
        self.image = self.actor.image
        self.size = size*3
        self.decay_clock = 0
        self.random_x_speed = random.random()*3*random.randint(-1, 1)*self.size/7
        self.random_y_speed = random.random()*3*random.randint(-1, 1)*self.size/7
        self.actor.angle = self.actor.angle_to((self.actor.x + self.random_x_speed, self.actor.y + self.random_y_speed)) - 90
        self.exist_time = random.randint(3, 5)*self.size
        self.exist_clock = 0

    def draw(self):
        self.actor.draw()

    def propell_randomly(self):
        #if self.exist_clock == self.exist_time:
        if self.actor.y >= HEIGHT - random.randint(-10, 20):
            self.decay_clock += 1
            if self.decay_clock >= random.randint(60, 600):
                rubbles.remove(self)
        else:
            self.exist_clock += 1
            self.actor.x += self.random_x_speed/3
            self.actor.y += self.random_y_speed/3
            self.actor.y += self.exist_clock/10

    def update(self):
        self.propell_randomly()
