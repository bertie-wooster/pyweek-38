#physics for stackable blocks
import math
import random

WIDTH = 800
HEIGHT = 600

class Tower:
    pass

blocks=[]

def draw():
    for block in blocks:
        block.draw()

def update(rt):
    for block in blocks:
        block.update(rt)

def on_mouse_down(pos):
    block_1 = Block(pos)
    blocks.append(block_1)


###
###
###
class Vector:
    def __init__(self, magnitude, theta):
        self.magnitude = magnitude
        self.theta = theta

class AccelerationVector(Vector):
    pass

class ConstantVector(Vector):
    pass

blocks = []
class Block:
    def __init__(self, actor):
        self.side = 50
        self.actor = actor
        self.speed_x = 0
        self.speed_y = 0
        self.main_vector = ConstantVector(0, math.radians(-15))
        self.gravity_vector = Vector(0, 0)
        self.normal_ground_vector = Vector(0, 0)
        self.vectors = [self.main_vector, self.gravity_vector, self.normal_ground_vector]
        self.second_clock = 0

    def gravity(self):
        if self.actor.y < HEIGHT - self.side//2:
            self.gravity_vector = Vector(self.gravity_vector.magnitude + 9.8/60, math.radians(90))
        else:
            self.normal_ground_vector = Vector(self.gravity_vector.magnitude,
            math.radians(math.degrees(self.gravity_vector.theta) -180))

    def draw(self):
        self.actor.draw()

    def update(self, rt):
        self.gravity()
        for vector in self.vectors:
            if vector.magnitude > 0:
                self.speed_x += math.cos(vector.theta)*vector.magnitude
                self.speed_y += math.sin(vector.theta)*vector.magnitude
        self.actor.x += self.speed_x
        self.actor.y += self.speed_y
        self.speed_x = 0
        self.speed_y = 0
        self.vectors.clear()
        self.vectors.append(self.main_vector)
        self.vectors.append(self.gravity_vector)
        self.vectors.append(self.normal_ground_vector)

    @classmethod
    def create_block(cls, x, y):
        block = Block(Actor('block_grey', (x, y)))
        blocks.append(block)

Block.create_block(WIDTH//2, HEIGHT//2)

def draw():
    screen.clear()
    for block in blocks:
        block.draw()
def update(rt):
    for block in blocks:
        block.update(rt)
    if keyboard.a:
        for block in blocks:
            block.main_vector.theta += math.radians(3)
    if keyboard.d:
        for block in blocks:
            block.main_vector.theta -= math.radians(3)
def on_key_down(key):
    if key == keys.W:
        for block in blocks:
            block.main_vector.magnitude += 1
    if key == keys.S:
        for block in blocks:
            if block.main_vector.magnitude >= 1:
                block.main_vector.magnitude -= 1

