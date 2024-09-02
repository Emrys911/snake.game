import pygame
import sys
import time
import random

# Difficulty settings
difficulty = 5
# Window size
frame_size_x = 720
frame_size_y = 480

# Initialize Pygame
pygame.init()

# Check for initialization errors
check_errors = pygame.init()
if check_errors[1] > 0:
    print(f'[!] Had {check_errors[1]} errors when initializing game, exiting...')
    sys.exit(-1)
else:
    print('[+] Game successfully initialized')

# Initialize game window
pygame.display.set_caption('3D Snake Eater')
game_window = pygame.display.set_mode((frame_size_x, frame_size_y))

# Colors (R, G, B)
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)

# FPS controller
fps_controller = pygame.time.Clock()

# Game variables
block_size = 20
snake_pos = [100, 50]
snake_body = [[100, 50], [100 - block_size, 50], [100 - (2 * block_size), 50]]
food_pos = [random.randrange(1, (frame_size_x // block_size)) * block_size,
            random.randrange(1, (frame_size_y // block_size)) * block_size]
food_spawn = True
direction = 'RIGHT'
change_to = direction
score = 0

def draw_sphere(surface, color, center, radius):
    """ Draw a shaded circle to simulate a 3D sphere. """
    for i in range(radius, 0, -1):
        shading_color = tuple(max(min(int(c * (1 - 0.5 * (i / radius))), 255), 0) for c in color)
        pygame.draw.circle(surface, shading_color, center, i)

def show_score(choice, color, font, size):
    """ Display the current score on the screen. """
    score_font = pygame.font.SysFont(font, size)
    score_surface = score_font.render('Score: ' + str(score), True, color)
    score_rect = score_surface.get_rect()
    if choice == 1:
        score_rect.midtop = (frame_size_x / 10, 15)
    else:
        score_rect.midtop = (frame_size_x / 2, frame_size_y / 1.25)
    game_window.blit(score_surface, score_rect)

def game_over():
    """ Display Game Over screen and restart button. """
    my_font = pygame.font.SysFont('times new roman', 90)
    game_over_surface = my_font.render('YOU DIED', True, red)
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop = (frame_size_x / 2, frame_size_y / 4)
    game_window.fill(black)
    game_window.blit(game_over_surface, game_over_rect)
    show_score(0, red, 'times', 20)

    # Draw Restart button
    restart_font = pygame.font.SysFont('times new roman', 50)
    restart_surface = restart_font.render('Press R to Restart', True, white)
    restart_rect = restart_surface.get_rect()
    restart_rect.midtop = (frame_size_x / 2, frame_size_y / 2)
    game_window.blit(restart_surface, restart_rect)

    pygame.display.flip()

def reset_game():
    """ Reset the game variables to start a new game. """
    global snake_pos, snake_body, food_pos, food_spawn, direction, change_to, score
    snake_pos = [100, 50]
    snake_body = [[100, 50], [100 - block_size, 50], [100 - (2 * block_size), 50]]
    food_pos = [random.randrange(1, (frame_size_x // block_size)) * block_size,
                random.randrange(1, (frame_size_y // block_size)) * block_size]
    food_spawn = True
    direction = 'RIGHT'
    change_to = direction
    score = 0

# Main game loop
game_running = True
while game_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == ord('w'):
                change_to = 'UP'
            if event.key == pygame.K_DOWN or event.key == ord('s'):
                change_to = 'DOWN'
            if event.key == pygame.K_LEFT or event.key == ord('a'):
                change_to = 'LEFT'
            if event.key == pygame.K_RIGHT or event.key == ord('d'):
                change_to = 'RIGHT'
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.key == pygame.K_r:
                reset_game()
                game_running = True

    # Making sure the snake cannot move in the opposite direction instantaneously
    if change_to == 'UP' and direction != 'DOWN':
        direction = 'UP'
    if change_to == 'DOWN' and direction != 'UP':
        direction = 'DOWN'
    if change_to == 'LEFT' and direction != 'RIGHT':
        direction = 'LEFT'
    if change_to == 'RIGHT' and direction != 'LEFT':
        direction = 'RIGHT'

    # Moving the snake
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
    if snake_pos[0] == food_pos[0] and snake_pos[1] == food_pos[1]:
        score += 1
        food_spawn = False
    else:
        snake_body.pop()

    # Spawning food on the screen
    if not food_spawn:
        food_pos = [random.randrange(1, (frame_size_x // block_size)) * block_size,
                    random.randrange(1, (frame_size_y // block_size)) * block_size]
    food_spawn = True

    # GFX
    game_window.fill(black)

    # Draw the snake as 3D spheres
    for pos in snake_body:
        draw_sphere(game_window, green, (pos[0] + block_size // 2, pos[1] + block_size // 2), block_size // 2)

    # Draw the food as a 3D sphere
    draw_sphere(game_window, white, (food_pos[0] + block_size // 2, food_pos[1] + block_size // 2), block_size // 2)

    # Game Over conditions
    if snake_pos[0] < 0 or snake_pos[0] > frame_size_x - block_size or snake_pos[1] < 0 or snake_pos[1] > frame_size_y - block_size:
        game_over()
        while True:  # Wait for user input to restart or quit
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        reset_game()
                        game_running = True
                        break
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
            else:
                continue
            break

    for block in snake_body[1:]:
        if snake_pos[0] == block[0] and snake_pos[1] == block[1]:
            game_over()
            while True:  # Wait for user input to restart or quit
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_r:
                            reset_game()
                            game_running = True
                            break
                        if event.key == pygame.K_ESCAPE:
                            pygame.quit()
                            sys.exit()
                else:
                    continue
                break

    show_score(1, white, 'consolas', 20)
    pygame.display.update()
    fps_controller.tick(difficulty)
