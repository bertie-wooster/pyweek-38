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
        return self.reward
    
    has_next = False

    def next(self, world):
        raise NotImplementedError()

    def __str__(self):
        return self.__class__.__name__
    
class GetLadder(Job):
    has_next = True

    def next(self, world: 'World'):
        current_x = self.target_x
        ladder_x = world.find_ladder(current_x, exists = False)
        return PlaceLadder(target_x=ladder_x, reward=None)

class GetBlock(Job):
    has_next = True

    def next(self, world: 'World'):
        current_x = self.target_x
        ladder_x = world.find_ladder(current_x, exists = True)
        return PlaceBlock(target_x=ladder_x, reward=None)

class PlaceLadder(Job):
    pass

class PlaceBlock(Job):
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
        self.item = None
        self.determine_next_job()
    
    def __str__(self):
        return "Builder(has {}, job {})".format(self.item, self.job)
    
    def update(self):
        if self.actor.x < self.job.target_x:
            self.actor.x += 5
        elif self.actor.x > self.job.target_x:
            self.actor.x -= 5
        else:
            self.finish_job()
    
    def determine_next_job(self):
        world = self.world
        nearest_storehouse, other_storehouse = world.find_storehouses(self.actor.x)
        if self.job and self.job.has_next:
            self.job = self.job.next(world)
        elif world.needs_ladder and (nearest_storehouse.has_ladder or other_storehouse.has_ladder) and not world.team.is_getting_ladder:
            self.job = GetLadder(target_x=nearest_storehouse.position_x if nearest_storehouse.has_ladder else other_storehouse.position_x, reward="ladder")
            print(self)
        elif world.needs_block and (nearest_storehouse.has_block or other_storehouse.has_block):
            self.job = GetBlock(target_x=nearest_storehouse.position_x if nearest_storehouse.has_block else other_storehouse.position_x, reward=None)
            print(self)
        if self.job:
            world.team.start_job(self.job)
    
    def finish_job(self):
        self.item = self.job.accomplish()
        self.determine_next_job()

class World:
    def __init__(self):
        self.team = Team()
        self.left_storehouse = Storehouse(ladder_count=0, block_count=40, position_x=0)
        self.right_storehouse = Storehouse(ladder_count=4, block_count=40, position_x=800)
        self.left_ladder = None
        self.left_ladder_x = 300
        self.right_ladder = None
        self.right_ladder_x = 500
    
    def find_storehouses(self, position_x):
        left_dist = abs(self.left_storehouse.position_x - position_x)
        right_dist = abs(self.right_storehouse.position_x - position_x)
        if left_dist < right_dist:
            return self.left_storehouse, self.right_storehouse
        return self.right_storehouse, self.left_storehouse
    
    def find_ladder(self, position_x, exists=True):
        if exists and not self.right_ladder:
            return self.left_ladder_x
        elif not self.right_ladder:
            return self.right_ladder_x
        # Both ladders are eligible.
        left_dist = abs(self.left_ladder_x - position_x)
        right_dist = abs(self.right_ladder_x - position_x)
        if left_dist < right_dist:
            return self.left_ladder_x
        else:
            return self.right_ladder_x
    
    @property
    def needs_ladder(self):
        return self.left_ladder is None or self.right_ladder is None
    
    needs_block = True