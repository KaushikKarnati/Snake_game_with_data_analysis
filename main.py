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
purple = (128, 0, 128)
black = (0, 0, 0)
red = (255, 0, 0)
grey = (128, 128, 128)  # Color for obstacles

# Initialize font
font = pygame.font.SysFont(None, 36)

def draw_block(color, position):
    block = pygame.Rect(position[0], position[1], cell_size, cell_size)
    pygame.draw.rect(screen, color, block)

def get_random_color():
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

def get_random_position(exclude=[]):
    position = (random.randint(0, width // cell_size - 1) * cell_size, random.randint(0, height // cell_size - 1) * cell_size)
    while position in exclude:
        position = (random.randint(0, width // cell_size - 1) * cell_size, random.randint(0, height // cell_size - 1) * cell_size)
    return position

def create_obstacles(num_obstacles, exclude=[]):
    obstacles = []
    while len(obstacles) < num_obstacles:
        new_obstacle = get_random_position(exclude)
        if new_obstacle not in obstacles:
            obstacles.append(new_obstacle)
    return obstacles

def main():
    snake = [(width // 2, height // 2)]
    apple = get_random_position()
    obstacles = create_obstacles(10, exclude=[apple] + snake)
    direction = (0, -cell_size)
    clock = pygame.time.Clock()
    game_data = {'game_length': 0, 'score': 0, 'moves': 0, 'death_cause': ''}
    segment_colors = [purple] + [get_random_color() for _ in range(len(snake) - 1)]
    start_ticks = pygame.time.get_ticks()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != (0, cell_size):
                    direction = (0, -cell_size)
                elif event.key == pygame.K_DOWN and direction != (0, -cell_size):
                    direction = (0, cell_size)
                elif event.key == pygame.K_LEFT and direction != (cell_size, 0):
                    direction = (-cell_size, 0)
                elif event.key == pygame.K_RIGHT and direction != (-cell_size, 0):
                    direction = (cell_size, 0)

        new_head = (snake[0][0] + direction[0], snake[0][1] + direction[1])
        snake.insert(0, new_head)
        segment_colors.insert(1, get_random_color())
        if snake[0] == apple:
            apple = get_random_position(exclude=snake + obstacles)
            game_data['score'] += 1
        else:
            snake.pop()
            segment_colors.pop()

        # Check for collision with obstacles
        if snake[0] in obstacles:
            game_data['death_cause'] = 'hit obstacle'
            save_game_data(game_data)
            running = False

        if snake[0][0] < 0 or snake[0][0] >= width or snake[0][1] < 0 or snake[0][1] >= height or snake[0] in snake[1:]:
            game_data['death_cause'] = 'wall collision' if snake[0][0] < 0 or snake[0][0] >= width or snake[0][1] < 0 or snake[0][1] >= height else 'self collision'
            game_data['game_length'] = (pygame.time.get_ticks() - start_ticks) / 1000
            game_data['moves'] = len(snake)
            save_game_data(game_data)
            running = False

        screen.fill(white)
        draw_block(red, apple)
        for obstacle in obstacles:
            draw_block(grey, obstacle)
        for i, segment in enumerate(snake):
            draw_block(segment_colors[i], segment)

        # Display Score and Time in black
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
