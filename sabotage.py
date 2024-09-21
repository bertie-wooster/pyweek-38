import os
os.environ['SDL_VIDEO_WINDOW_POS'] = f'0,0'

import pgzrun

#from tower import Tower
from builders import Builder, World

world = World()

builders = [
    Builder((100, 500), world), 
    Builder((300, 500), world), 
    Builder((500, 500), world),
]

def draw():
    screen.clear()
    screen.fill((34, 117, 56))
    for builder in builders:
        builder.actor.draw()

def update():
    for builder in builders:
        builder.update()

pgzrun.go()
