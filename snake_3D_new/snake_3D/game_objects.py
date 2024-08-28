from ursina import *
from random import randrange

from ursina import Entity


class Apple(Entity):
    def __init__(self, MAP_SIZE, **kwargs):
        super().__init__(**kwargs)
        self.position = None
        self.MAP_SIZE = MAP_SIZE
        self.new_position()

    def new_position(self):
        # Генерируем случайную позицию яблока на карте
        self.position = (randrange(self.MAP_SIZE) * 0.5, randrange(self.MAP_SIZE) * 0.5, -0.5)


class Snake:
    def __init__(self, map_size):
        self.MAP_SIZE = map_size
        self.segment_positions = [Vec3(randrange(self.MAP_SIZE) * 0.5, randrange(self.MAP_SIZE) * 0.5, 0)]
        self.segment_entities = []
        self.segment_length = 1
        self.directions = {'w': Vec3(0, 0.5, 0), 's': Vec3(0, -0.5, 0), 'a': Vec3(-0.5, 0, 0), 'd': Vec3(0.5, 0, 0)}
        self.direction = Vec3(0, 0, 0)
        self.permission = {'a': 1, 'd': 1, 'w': 1, 's': 1}
        self.taboo_movement = {'a': 'd', 'd': 'a', 'w': 's', 's': 'w'}
        self.speed, self.score = 12, 0
        self.frame_counter = 0

        # Создание начального сегмента змейки
        self.create_segment(self.segment_positions[0])

    def add_segment(self):
        self.segment_length += 1
        self.score += 1
        self.speed = max(self.speed - 1, 5)
        # Добавляем новый сегмент в начало списка сегментов змейки
        self.create_segment(self.segment_positions[0])

    def create_segment(self, position):
        # Создание сегмента змейки и добавление его в список сегментов
        segment = Entity(model='sphere', color=color.green, position=position)
        segment.add_script(SmoothFollow(speed=12, target=entity, offset=(0, 0, 0)))
        self.segment_entities.insert(0, segment)

    def run(self):
        self.frame_counter += 1
        if not self.frame_counter % self.speed:
            self.control()
            # Обновление позиций сегментов змейки
            new_position = self.segment_positions[-1] + self.direction
            self.segment_positions.append(new_position)
            self.segment_positions = self.segment_positions[-self.segment_length:]
            for segment, segment_position in zip(self.segment_entities, self.segment_positions):
                segment.position = segment_position

    def control(self):
        for key in 'wasd':
            if held_keys[key] and self.permission[key]:
                self.direction = self.directions[key]
                # Обновляем разрешения на движение
                self.permission = dict.fromkeys(self.permission, 1)

                self.permission[self.taboo_movement[key]] = 0
                break
