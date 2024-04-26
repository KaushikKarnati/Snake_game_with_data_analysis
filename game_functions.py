import random

import pygame
import sys
from game_config import white,black,font
from game_config import width, height, cell_size


def title_screen(screen, high_scores):
    running = True
    while running:
        screen.fill(white)
        title = font.render('Snake Game', True, black)
        screen.blit(title, (width // 2 - title.get_width() // 2, height // 3))

        # Display high scores here if needed
        # Example: loop through high_scores and blit each

        play_text = font.render('Press any key to play', True, black)
        screen.blit(play_text, (width // 2 - play_text.get_width() // 2, height // 2))

        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                running = False

def draw_block(screen, color, position, direction, is_head=False):
    """Draws a block for the snake or apple, head as a triangle if specified."""
    block = pygame.Rect(position[0], position[1], cell_size, cell_size)
    if is_head:
        # Determine points based on direction for the head to be a triangle pointing in the movement direction
        triangle_points = get_triangle_points(position, direction)
        pygame.draw.polygon(screen, color, triangle_points)
    else:
        # Draw the body as a rectangle
        pygame.draw.rect(screen, color, block)

def get_triangle_points(position, direction):
    """Calculate triangle vertices for the snake's head based on movement direction."""
    x, y = position
    if direction == (0, -cell_size):  # Moving up
        return [(x + cell_size / 2, y), (x, y + cell_size), (x + cell_size, y + cell_size)]
    elif direction == (0, cell_size):  # Moving down
        return [(x + cell_size / 2, y + cell_size), (x, y), (x + cell_size, y)]
    elif direction == (-cell_size, 0):  # Moving left
        return [(x, y + cell_size / 2), (x + cell_size, y), (x + cell_size, y + cell_size)]
    elif direction == (cell_size, 0):  # Moving right
        return [(x + cell_size, y + cell_size / 2), (x, y), (x, y + cell_size)]

def handle_key_events(event, current_direction):
    """Handles key events and changes the snake's direction without reversing."""
    key_to_direction = {
        pygame.K_UP: (0, -cell_size),
        pygame.K_DOWN: (0, cell_size),
        pygame.K_LEFT: (-cell_size, 0),
        pygame.K_RIGHT: (cell_size, 0)
    }
    new_direction = key_to_direction.get(event.key, current_direction)
    # Prevent reversing the snake
    if (new_direction[0] == -current_direction[0] and new_direction[0] != 0) or \
       (new_direction[1] == -current_direction[1] and new_direction[1] != 0):
        return current_direction
    return new_direction

def get_random_position(exclude=[]):
    """Generates a random position not including specified exclusions within the game area."""
    while True:
        x = random.randint(0, (width - cell_size) // cell_size) * cell_size
        y = random.randint(0, (height - cell_size) // cell_size) * cell_size
        position = (x, y)
        if position not in exclude:
            return position

def move_snake(snake_positions, direction, apple_position, game_data):
    """Moves the snake, checks for eating an apple, and grows if apple eaten."""
    new_head = (snake_positions[0][0] + direction[0], snake_positions[0][1] + direction[1])
    snake_positions.insert(0, new_head)
    if new_head == apple_position:
        game_data['score'] += 1
        return get_random_position(exclude=snake_positions)  # Return new apple position
    else:
        snake_positions.pop()
    return apple_position
