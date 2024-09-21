import os
os.environ['SDL_VIDEO_WINDOW_POS'] = f'0,0'

import pgzrun

from tower import Block, Rubble, blocks, rubbles, right_ladders, right_stone, left_stone, left_ladders, WIDTH, HEIGHT
from builders import Builder, World

world = World()

builders = [
    Builder((100, 500), world),
    Builder((300, 500), world),
    Builder((500, 500), world),
]

def draw():
    screen.clear()
    screen.fill((100, 117, 100))
    for block in blocks:
        block.draw()
    for rubble in rubbles:
        rubble.draw()
    for builder in builders:
        builder.draw()

def update(rt):
    for builder in builders:
        builder.update(rt)
    for block in blocks:
        block.update(rt)
    for rubble in rubbles:
        rubble.update()

def on_mouse_down(pos, button):
    if button == mouse.RIGHT:
        closest_click = 100000
        for block in blocks:
            mouse_pos_dist = block.actor.distance_to(pos)
            if mouse_pos_dist < closest_click:
                closest_click = mouse_pos_dist
                closest_block = block
        closest_block.damaged = True

def on_key_down(key):
    if key == keys.Q:
        placed_block = Block.place_stone(WIDTH//2-25, HEIGHT-105-(len(left_stone)*50), left_stone)
        left_stone.append(placed_block)
    if key == keys.E:
        placed_block = Block.place_stone(WIDTH//2+25, HEIGHT-105-(len(right_stone)*50), right_stone)
        right_stone.append(placed_block)
    if key == keys.LEFT:
        placed_block = Block.place_ladder(WIDTH//2-85, HEIGHT-105-(len(left_ladders)*50), left_ladders)
        left_ladders.append(placed_block)
    if key == keys.RIGHT:
        placed_block = Block.place_ladder(WIDTH//2+85, HEIGHT-105-(len(right_ladders)*50), right_ladders)
        right_ladders.append(placed_block)

pgzrun.go()
