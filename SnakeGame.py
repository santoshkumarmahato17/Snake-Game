import pygame
import random

# Initialize Pygame
pygame.init()

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Screen dimensions
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480

# Block size
BLOCK_SIZE = 20

# Font
FONT = pygame.font.SysFont(None, 35)

# Clock
CLOCK = pygame.time.Clock()
FPS = 3

def draw_snake(snake_body):
    for block in snake_body:
        pygame.draw.rect(screen, GREEN, [block[0], block[1], BLOCK_SIZE, BLOCK_SIZE])

def draw_food(food_pos):
    pygame.draw.rect(screen, RED, [food_pos[0], food_pos[1], BLOCK_SIZE, BLOCK_SIZE])

def get_random_food():
    x = random.randint(0, (SCREEN_WIDTH - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
    y = random.randint(0, (SCREEN_HEIGHT - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
    return [x, y]

def message_to_screen(msg, color, y_displace=0):
    text = FONT.render(msg, True, color)
    screen.blit(text, [SCREEN_WIDTH / 2 - text.get_width() / 2, SCREEN_HEIGHT / 2 + y_displace])

def game_loop():
    game_over = False
    game_close = False

    # Initial snake position and body
    snake_body = [[SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2]]
    snake_length = 1

    # Initial direction
    direction = 'RIGHT'
    change_to = direction

    # Initial food position
    food_pos = get_random_food()

    score = 0

    while not game_over:
        while game_close:
            screen.fill(BLACK)
            message_to_screen("You Lost! Press Q-Quit or C-Play Again", RED, -50)
            message_to_screen(f"Score: {score}", WHITE, 50)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                    game_close = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        game_loop()

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and direction != 'RIGHT':
                    change_to = 'LEFT'
                elif event.key == pygame.K_RIGHT and direction != 'LEFT':
                    change_to = 'RIGHT'
                elif event.key == pygame.K_UP and direction != 'DOWN':
                    change_to = 'UP'
                elif event.key == pygame.K_DOWN and direction != 'UP':
                    change_to = 'DOWN'

        # Update direction
        direction = change_to

        # Move snake head
        if direction == 'LEFT':
            snake_body[0][0] -= BLOCK_SIZE
        elif direction == 'RIGHT':
            snake_body[0][0] += BLOCK_SIZE
        elif direction == 'UP':
            snake_body[0][1] -= BLOCK_SIZE
        elif direction == 'DOWN':
            snake_body[0][1] += BLOCK_SIZE

        # Check wall collision
        if (snake_body[0][0] >= SCREEN_WIDTH or snake_body[0][0] < 0 or
            snake_body[0][1] >= SCREEN_HEIGHT or snake_body[0][1] < 0):
            game_close = True

        # Check self collision
        for block in snake_body[1:]:
            if block == snake_body[0]:
                game_close = True

        # Check food collision
        if snake_body[0] == food_pos:
            food_pos = get_random_food()
            snake_length += 2
            score += 1

        # Add new head
        snake_body.insert(0, list(snake_body[0]))

        # Remove tail if not grown
        if len(snake_body) > snake_length:
            del snake_body[-1]

        # Draw everything
        screen.fill(BLACK)
        draw_food(food_pos)
        draw_snake(snake_body)

        # Display score
        score_text = FONT.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, [10, 10])

        pygame.display.update()

        # Control game speed
        CLOCK.tick(FPS)

    pygame.quit()
    quit()

# Set up display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Snake Game')

# Start game
game_loop()
