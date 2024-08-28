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
DARK_GREEN = (0, 200, 0)
DARK_RED = (200, 0, 0)

# Game parameters
clock = pygame.time.Clock()
block_size = 20
snake_speed = 15

# Snake and apple initial positions and settings
snake_pos = [100, 50]
snake_body = [[100, 50], [90, 50], [80, 50]]
apple_pos = [randrange(1, (screen_width // block_size)) * block_size,
             randrange(1, (screen_height // block_size)) * block_size]
apple_spawn = True
direction = 'RIGHT'
change_to = direction


def draw_sphere(surface, color, center, radius):
    """ Draw a shaded circle to simulate a 3D sphere. """
    for i in range(radius, 0, -1):
        shading_color = tuple(max(min(int(c * (1 - 0.5 * (i / radius))), 255), 0) for c in color)
        pygame.draw.circle(surface, shading_color, center, i)


# Main game loop
while True:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != 'DOWN':
                change_to = 'UP'
            elif event.key == pygame.K_DOWN and direction != 'UP':
                change_to = 'DOWN'
            elif event.key == pygame.K_LEFT and direction != 'RIGHT':
                change_to = 'LEFT'
            elif event.key == pygame.K_RIGHT and direction != 'LEFT':
                change_to = 'RIGHT'

    # Change direction
    direction = change_to

    # Update snake position
    if direction == 'UP':
        snake_pos[1] -= block_size
    if direction == 'DOWN':
        snake_pos[1] += block_size
    if direction == 'LEFT':
        snake_pos[0] -= block_size
    if direction == 'RIGHT':
        snake_pos[0] += block_size

    # Snake body growing mechanism
    snake_body.insert(0, list(snake_pos))
    if snake_pos == apple_pos:
        apple_spawn = False
    else:
        snake_body.pop()

    if not apple_spawn:
        apple_pos = [randrange(1, (screen_width // block_size)) * block_size,
                     randrange(1, (screen_height // block_size)) * block_size]
    apple_spawn = True

    # Fill the screen with black
    screen.fill(BLACK)

    # Draw snake as 3D spheres
    for pos in snake_body:
        draw_sphere(screen, GREEN, (pos[0] + block_size // 2, pos[1] + block_size // 2), block_size // 2)

    # Draw apple as a 3D sphere
    draw_sphere(screen, RED, (apple_pos[0] + block_size // 2, apple_pos[1] + block_size // 2), block_size // 2)

    # Update display
    pygame.display.flip()

    # Check for collisions with the wall
    if snake_pos[0] < 0 or snake_pos[0] > screen_width - block_size:
        pygame.quit()
        sys.exit()
    if snake_pos[1] < 0 or snake_pos[1] > screen_height - block_size:
        pygame.quit()
        sys.exit()

    # Check for collisions with itself
    for block in snake_body[1:]:
        if snake_pos == block:
            pygame.quit()
            sys.exit()

    # Control the speed of the snake
    clock.tick(snake_speed)
