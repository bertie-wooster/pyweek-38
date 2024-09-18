#from tower import Tower
from builders import Builder

builders = [
    Builder((100, 500)), 
    Builder((300, 500)), 
    Builder((500, 500)),
]

def draw():
    screen.clear()
    screen.fill((34, 117, 56))
    for builder in builders:
        builder.actor.draw()

def update():
    pass