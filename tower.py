#physics for stackable blocks
from pgzero.builtins import *

WIDTH=800
HEIGHT=600

blocks = []

right_ladders=[]

right_stone = []
middle_stone = []
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
                    for block in blocks_above:
                        block.fall = True
        else:
            if self.damaged:
                for block in list(self.collum):
                    if block is not self:
                        if block.actor.y < self.actor.y:
                            block.create_rubble(3)
                            blocks.remove(block)
                            self.collum.remove(block)
                self.create_rubble(3)
                blocks.remove(self)
                self.collum.remove(self)

    def create_rubble(self, intensity):
        for i in range(10**intensity):
            pass

    def fall_down(self):
        self.actor.y += 2
        for block in self.collum:
            if block is not self:
                if self.actor.colliderect(block.actor):
                    if block.fall != True:
                        self.fall = False
                        self.actor.y = block.actor.y - 50
                        return
        if self.actor.y >= HEIGHT - 25:
            self.fall = False
            self.actor.y = HEIGHT - 25
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
