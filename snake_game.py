from templates.game_obj import *
from ursina import Ursina, color, Light, window, camera, scene, print_on_screen, Vec3, invoke, Entity

from templates.game_obj import Snake, Apple


class Game(Ursina):
    def __init__(self):
        super().__init__()
        self.MAP_SIZE = 20  # Initialize MAP_SIZE before using it
        self.snake = Snake(self.MAP_SIZE)
        self.apple = Apple(self.MAP_SIZE, model='sphere', color=color.red)
        window.color = color.black
        window.fullscreen_size = 1920, 1000
        window.fullscreen = True
        Light(type='ambient', color=(0.5, 0.5, 0.5, 1))
        Light(type='directional', color=(0.5, 0.5, 0.5, 1), direction=(1, 1, 1))
        self.new_game()
        camera.position = (self.MAP_SIZE // 2, -20.5, -20)
        camera.rotation_x = 57

    def new_game(self):
        scene.clear()
        create_map(self.MAP_SIZE)

    def input(self, key, **kwargs):
        if key == '2':
            camera.rotation_x = 0
            camera.position = (self.MAP_SIZE // 2, self.MAP_SIZE // 2, -50)
        elif key == '3':
            camera.position = (self.MAP_SIZE // 2, -20.5, -20)
            camera.rotation_x = -57
        super().input(key)

    def check_apple_eaten(self):
        if self.snake.segment_positions[-1] == self.apple.position:
            self.snake.add_segment()
            self.apple.new_position()

    def check_game_over(self):
        snake = self.snake.segment_positions
        if 0 < snake[-1][0] < self.MAP_SIZE and 0 < snake[-1][1] < self.MAP_SIZE and len(snake) == len(set(snake)):
            return
        print_on_screen('GAME OVER', position=(-0.7, 0.1), scale=10, duration=1)
        self.snake.direction = Vec3(0, 0, 0)
        self.snake.permissions = dict.fromkeys(self.snake.permissions, 0)
        invoke(self.new_game, delay=1)

    def update(self):
        print_on_screen(f'Score: {self.snake.score}', position=(-0.85, 0.45), scale=3, duration=1 / 20)
        self.check_apple_eaten()
        self.check_game_over()
        self.snake.run()


def create_map(map_size):
    Entity(model='quad', scale=map_size, position=(map_size // 2, map_size // 2, 0), color=color.dark_grey)
    Entity(model='quad', scale=map_size, position=(map_size // 2, map_size // 2, -0.01), color=color.white)


if __name__ == "__main__":  # Corrected from "__name__"
    game = Game()
    game.run()
