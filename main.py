import pygame
import sys
from game_functions import draw_block, get_random_position, title_screen, move_snake, handle_key_events
from game_config import width, height, white, red, green, black, cell_size, font
from data import save_game_data
from high_scores import load_high_scores, save_high_scores

def main():
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Snake Game')

    # Load or initialize high scores
    high_scores = load_high_scores()

    # Display the title screen and wait for the user to start the game
    title_screen(screen, high_scores)

    # Game initialization
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
                direction = handle_key_events(event, direction)

        # Game logic
        move_snake(snake, direction, apple, game_data)

        # Check game over condition
        if snake[0] in snake[1:] or not (0 <= snake[0][0] < width and 0 <= snake[0][1] < height):
            game_data['death_cause'] = 'collision'
            game_data['game_length'] = (pygame.time.get_ticks() - start_ticks) / 1000
            game_data['moves'] = len(snake)
            save_game_data(game_data)
            running = False
            high_scores.append({'score': game_data['score'], 'name': 'Player'})  # Assume 'Player' or get from input
            save_high_scores(high_scores)

        # Drawing
        screen.fill(white)
        draw_block(screen, red, apple, direction)  # Draw the apple
        for i, segment in enumerate(snake):
            draw_block(screen, green if i > 0 else black, segment, direction, is_head=(i == 0))

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
