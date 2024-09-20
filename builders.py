import random
from pgzero.builtins import *

_JOBS = [
    "get ladder",
    "get block",
    "place ladder",
    "place block",
    "guard",
    "final attack",
    "return block",
    "return ladder",
]

class Job:
    def __init__(self, target_x, reward):
        self.target_x = target_x
        self.reward = reward
    
    def accomplish(self):
        raise NotImplementedError()
    
class GetLadder(Job):
    pass

class GetBlock(Job):
    pass

class Item:
    def receive():
        pass

class Storehouse:
    def __init__(self, ladder_count, block_count, position_x):
        self.ladder_count = ladder_count
        self.block_count = block_count
        self.position_x = position_x
    
    def take_ladder(self):
        pass

    def take_block(self):
        pass
    
    @property
    def has_ladder(self):
        return self.ladder_count > 0
    
    @property
    def has_block(self):
        return self.block_count > 0

class Team:
    def __init__(self):
        self.active_jobs = []
    
    def start_job(self, job):
        self.active_jobs.append(job.__class__)
    
    def finish_job(self, job):
        self.active_jobs.remove(job.__class__)

    @property
    def is_getting_ladder(self):
        return GetLadder in self.active_jobs
    

class Builder:
    def __init__(self, pos, world):
        self.job = None
        self.actor = Actor('builder', pos)
        self.y_value = 100
        self.world = world
        self.determine_next_job()
    
    def update(self):
        if self.actor.x < self.job.target_x:
            self.actor.x += 1
        elif self.actor.x > self.job.target_x:
            self.actor.x -= 1
        else:
            self.finish_job()
    
    def determine_next_job(self):
        world = self.world
        if self.job and self.job.has_next:
            self.job = self.job.next()
        elif world.needs_ladder and world.storehouse.has_ladder and not world.team.is_getting_ladder:
            self.job = GetLadder(target_x=world.storehouse.position_x, reward=None)
            print(self, "getting ladder")
        elif world.needs_block and world.storehouse.has_block:
            self.job = GetBlock(target_x=world.storehouse.position_x, reward=None)
            print(self, "getting block")
        world.team.start_job(self.job)
    
    def finish_job(self):
        pass

class World:
    def __init__(self):
        self.team = Team()
        self.storehouse = Storehouse(ladder_count=4, block_count=40, position_x=0)
        self.left_ladder = None
        self.right_ladder = None
    
    @property
    def needs_ladder(self):
        return self.left_ladder is None or self.right_ladder is None
    
    needs_block = True