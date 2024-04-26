import pygame
import sys
import random
from data import save_game_data

# Initialize pygame and set up display
pygame.init()
width, height = 800, 600
cell_size = 20
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Snake Game')

# Define colors
white = (255, 255, 255)
green = (0, 255, 0)
black = (0, 0, 0)
red = (255, 0, 0)

# Initialize font
font = pygame.font.SysFont(None, 36)


def draw_block(color, position, direction, is_head=False):
    block = pygame.Rect(position[0], position[1], cell_size, cell_size)
    if is_head:
        # Determine points based on direction for the head to be a triangle pointing in the movement direction
        if direction == (0, -cell_size):  # Moving up
            triangle_points = [
                (position[0] + cell_size / 2, position[1]),  # Top center point
                (position[0], position[1] + cell_size),  # Bottom left
                (position[0] + cell_size, position[1] + cell_size)  # Bottom right
            ]
        elif direction == (0, cell_size):  # Moving down
            triangle_points = [
                (position[0] + cell_size / 2, position[1] + cell_size),  # Bottom center point
                (position[0], position[1]),  # Top left
                (position[0] + cell_size, position[1])  # Top right
            ]
        elif direction == (-cell_size, 0):  # Moving left
            triangle_points = [
                (position[0], position[1] + cell_size / 2),  # Left center point
                (position[0] + cell_size, position[1]),  # Top right
                (position[0] + cell_size, position[1] + cell_size)  # Bottom right
            ]
        elif direction == (cell_size, 0):  # Moving right
            triangle_points = [
                (position[0] + cell_size, position[1] + cell_size / 2),  # Right center point
                (position[0], position[1]),  # Top left
                (position[0], position[1] + cell_size)  # Bottom left
            ]
        pygame.draw.polygon(screen, color, triangle_points)
    else:
        # Draw the body as a rectangle
        pygame.draw.rect(screen, color, block)



def get_random_color():
    return random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)


def get_random_position(exclude=[]):
    """Generates a random position not including specified exclusions"""
    while True:
        x = random.randint(0, (width - cell_size) // cell_size) * cell_size
        y = random.randint(0, (height - cell_size) // cell_size) * cell_size
        position = (x, y)
        if position not in exclude:
            return position


def main():
    snake = [get_random_position()]
    apple = get_random_position(exclude=snake)
    direction = (0, -cell_size)  # Initial direction up
    clock = pygame.time.Clock()
    game_data = {'game_length': 0, 'score': 0, 'moves': 0, 'death_cause': ''}
    start_ticks = pygame.time.get_ticks()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                new_direction = {
                    pygame.K_UP: (0, -cell_size),
                    pygame.K_DOWN: (0, cell_size),
                    pygame.K_LEFT: (-cell_size, 0),
                    pygame.K_RIGHT: (cell_size, 0)
                }.get(event.key, direction)

                # Prevent the snake from reversing
                if new_direction != (direction[0] * -1, direction[1] * -1):
                    direction = new_direction

        new_head = (snake[0][0] + direction[0], snake[0][1] + direction[1])
        snake.insert(0, new_head)
        if new_head == apple:
            apple = get_random_position(exclude=snake)
            game_data['score'] += 1
        else:
            snake.pop()

        if new_head in snake[1:] or new_head[0] < 0 or new_head[0] >= width or new_head[1] < 0 or new_head[1] >= height:
            game_data['death_cause'] = 'collision'
            game_data['game_length'] = (pygame.time.get_ticks() - start_ticks) / 1000
            game_data['moves'] = len(snake)
            save_game_data(game_data)
            running = False

        screen.fill(white)
        draw_block(red, apple, direction)  # Apple doesn't need direction
        for i, segment in enumerate(snake):
            draw_block(green if i > 0 else black, segment, direction, is_head=(i == 0))

        # Display Score and Time
        score_text = font.render(f'Score: {game_data["score"]}', True, black)
        time_elapsed = (pygame.time.get_ticks() - start_ticks) / 1000
        time_text = font.render(f'Time: {int(time_elapsed)}s', True, black)
        screen.blit(score_text, (width - 160, 10))
        screen.blit(time_text, (width - 160, 50))

        pygame.display.update()
        clock.tick(10)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()

if __name__ == "__main__":
    main()
