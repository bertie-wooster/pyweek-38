#Double Trouble
import random

WIDTH = 600
HEIGHT = 450

dots = []

class Dot:
    def __init__(self, team, player):
        self.team = team
        self.player = player
        self.start_pos = self.find_start_pos()
        self.actor = Actor(self.team, self.start_pos)
        self.in_cover = False

    def find_start_pos(self):
        if self.team == 'red_dot':
            x = random.randint(0, WIDTH//2)
        elif self.team == 'blue_dot':
            x = random.randint(WIDTH//2+1, WIDTH)
        y = random.randint(0, HEIGHT)
        return x, y

    def draw(self):
        self.actor.draw()

    def update(self, rt):
        if self.player == True:
            if keyboard.A:
                self.actor.x -= 1
            if keyboard.D:
                self.actor.x += 1
            if keyboard.W:
                self.actor.y -= 1
            if keyboard.S:
                self.actor.y += 1

    @classmethod
    def create_dot(cls, team, player):
        dot = Dot(team=team, player=player)
        dots.append(dot)
for i in range(10):
    Dot.create_dot('red_dot', False)
for i in range(10):
    Dot.create_dot('blue_dot', False)
Player = Dot.create_dot('red_dot', True)

covers = []
class Cover:
    def __init__(self):
        self.start_pos = self.find_start_pos()
        self.size = random.randint(20, 60)

    def find_start_pos(self):
        x = random.randint(10, WIDTH-10)
        y = random.randint(10, HEIGHT-10)
        return x, y

    def draw(self):
        screen.draw.filled_circle(self.start_pos, self.size, (10, 100, 10))

    def update(self, rt):
        pass

    @classmethod
    def create_cover(cls):
        cover = Cover()
        covers.append(cover)
for i in range(6):
    Cover.create_cover()

def draw():
    screen.clear()
    for cover in covers:
        cover.draw()
    for dot in dots:
        dot.draw()

def update(rt):
    for dot in dots:
        dot.update(rt)
    for cover in covers:
        cover.draw()

def on_key_down(key):
    if key == keys.SPACE:
        for dot in dots:
            if dot.player == True:
                for cover in covers:
                    if dot.actor.distance_to(cover.start_pos) < cover.size:
                        dot.in_cover = True
                if dot.in_cover == True:
                    if dot.team == 'red_dot':
                        dot.team = 'blue_dot'
                    else:
                        dot.team = 'red_dot'
                dot.actor.image = dot.team
                dot.in_cover = False
