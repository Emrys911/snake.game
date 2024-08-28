import pygame
import sys
from random import randrange

# Initialize Pygame
pygame.init()

# Screen settings
screen_width = 640
screen_height = 480
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Snake Game")

# Colors
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Game parameters
clock = pygame.time.Clock()
block_size = 20
map_size = 20
speed = 12


class Apple(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((block_size, block_size))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.new_position()

    def new_position(self):
        self.rect.x = randrange(0, (screen_width // block_size)) * block_size
        self.rect.y = randrange(0, (screen_height // block_size)) * block_size


class Snake:
    def __init__(self):
        self.body = [[100, 50]]
        self.direction = pygame.Vector2(1, 0)  # Start moving to the right
        self.directions = {
            'UP': pygame.Vector2(0, -1),
            'DOWN': pygame.Vector2(0, 1),
            'LEFT': pygame.Vector2(-1, 0),
            'RIGHT': pygame.Vector2(1, 0)
        }
        self.permission = {'UP': 1, 'DOWN': 1, 'LEFT': 1, 'RIGHT': 1}
        self.taboo_movement = {'UP': 'DOWN', 'DOWN': 'UP', 'LEFT': 'RIGHT', 'RIGHT': 'LEFT'}
        self.grow_snake = False
        self.speed = speed

    def move(self):
        head_x, head_y = self.body[0]
        new_head = [head_x + self.direction.x * block_size, head_y + self.direction.y * block_size]
        self.body.insert(0, new_head)

        if not self.grow_snake:
            self.body.pop()
        else:
            self.grow_snake = False

    def change_direction(self, new_direction):
        if new_direction != self.taboo_movement.get(self.current_direction()):
            self.direction = self.directions[new_direction]

    def current_direction(self):
        for dir_key, vector in self.directions.items():
            if vector == self.direction:
                return dir_key
        return 'RIGHT'  # Default

    def grow(self):
        self.grow_snake = True

    def draw(self, screen):
        for segment in self.body:
            pygame.draw.rect(screen, GREEN, pygame.Rect(segment[0], segment[1], block_size, block_size))

    def check_collision(self):
        head = self.body[0]
        # Check collision with walls
        if head[0] < 0 or head[0] >= screen_width or head[1] < 0 or head[1] >= screen_height:
            return True

        # Check collision with itself
        if head in self.body[1:]:
            return True

        return False


# Game Initialization
snake = Snake()
apple = Apple()


# Main game loop
def run_game():
    global apple

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    snake.change_direction('UP')
                elif event.key == pygame.K_DOWN:
                    snake.change_direction('DOWN')
                elif event.key == pygame.K_LEFT:
                    snake.change_direction('LEFT')
                elif event.key == pygame.K_RIGHT:
                    snake.change_direction('RIGHT')

        # Move the snake
        snake.move()

        # Check if snake eats the apple
        if snake.body[0] == [apple.rect.x, apple.rect.y]:
            snake.grow()
            apple.new_position()

        # Check for collisions
        if snake.check_collision():
            pygame.quit()
            sys.exit()

        # Fill screen
        screen.fill(BLACK)

        # Draw apple
        screen.blit(apple.image, apple.rect)

        # Draw snake
        snake.draw(screen)

        # Update display
        pygame.display.flip()

        # Control the speed
        clock.tick(snake.speed)


if __name__ == "__main__":
    run_game()
