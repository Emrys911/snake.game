from ursina import *
from random import randrange

from ursina import Vec3, Entity
from ursina import Entity


class Apple(Entity):
    def __init__(self, MAP_SIZE, **kwargs):
        super().__init__(**kwargs)
        self.MAP_SIZE = MAP_SIZE
        self.new_position()


def new_position(self):
    self.position = (randrange(self.MAP_SIZE) * 0.5, randrange(self.MAP_SIZE) * 0.5, -0.5)


class Snake:
    def __init__(self, map_size):
        self.segment_positions = None
        self.directions = None
        self.MAP_SIZE = map_size
        self.segment_length = 1
        self.position_length = self.segment_length = 1
        self.segment_position = [Vec3(randrange(self.MAP_SIZE * 0.5), randrange(map_size * 0.5, -1))]
        self.segment_entities = []
        self.create_segment(self.segment_positions[0])
        self.direction = Vec3(0, 0, 0)
        self.permission = {'a': 1, 'd': 1, 'w': 1, 's': 1}
        self.taboo_movement = {'a': 'd', 'd': 'a', 'w': 's', 's': 'w'}
        self.speed, self.score = 12, 0
        self.frame_counter = 0

    def add_segment(self):
        self.segment_length += 1
        self.position_length += 1
        self.score += 1
        self.speed = max(self.speed - 1, 5)
        self.create_segment(self.segment_positions[0])

    def create_segment(self, position):
        entity = Entity(position=position)
        Entity(model='sphere', color=color.green, position=position).add_script(
            SmoothFollow(speed=12, target=entity, offset=(0, 0, 0)))
        self.segment_entities.insert(0, entity)

    def run(self):
        self.frame_counter += 1
        if not self.frame_counter % self.speed:
            self.control()
            self.segment_position.append(self.segment_position[-1] + self.direction)
            self.segment_positions = self.segment_position[-self.segment_length:]
            for segment, segment_position in zip(self.segment_entities, self.segment_positions):
                segment_position

    def control(self):
        for key in 'wasd':
            if held_keys[key] and self.permission[key]:
                self.direction = self.directions[key]
                self.permission = dict.fromkeys(self.permission, 1)
                self.permission[self.taboo_movement[key]] = 0
                break
