import pygame
import random
import os
from collections import deque

# Initialize Pygame and Mixer
pygame.init()
pygame.mixer.init()

# Colors
WHITE = (255, 255, 255)
RED = (234, 80, 88)
BLACK = (1, 1, 1)

# Display Settings
SCREEN_HEIGHT = 720
SCREEN_WIDTH = 1200
gameWindow = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake vs Mr JOYSiM")

clock = pygame.time.Clock()

# Fonts and Paths
FONT_PATH = "hyperwave-one.ttf"
FONT_SIZE = 60
futuristic_font = pygame.font.Font(FONT_PATH, FONT_SIZE)
score_font = pygame.font.Font(FONT_PATH, 100)
regular_font = pygame.font.SysFont(None, 55)

# Images
bgimg = pygame.image.load("bg.png")
bgimg = pygame.transform.scale(bgimg, (SCREEN_WIDTH, SCREEN_HEIGHT)).convert_alpha()

overimg = pygame.image.load("over.png")
overimg = pygame.transform.scale(overimg, (SCREEN_WIDTH, SCREEN_HEIGHT)).convert_alpha()

wlcimg = pygame.image.load("wlc.png")
wlcimg = pygame.transform.scale(wlcimg, (SCREEN_WIDTH, SCREEN_HEIGHT)).convert_alpha()

# Sounds
button_click_sound = pygame.mixer.Sound("start.mp3")
hover_sound = pygame.mixer.Sound("hover.mp3")
eat_sound = pygame.mixer.Sound("eat.mp3")

# Load Music and Set Volumes (if needed)
# pygame.mixer.music.set_volume(0.5) # Optional

# Ensure highscore file exists
if not os.path.exists("highscore.txt"):
    with open("highscore.txt", "w") as f:
        f.write("0")

def load_highscore():
    with open("highscore.txt", "r") as f:
        return f.read()

def save_highscore(score):
    with open("highscore.txt", "w") as f:
        f.write(str(score))

def startMusic():
    button_click_sound.play()
    pygame.mixer.music.load("bg.mp3")
    pygame.time.delay(950)
    pygame.mixer.music.play(-1)

def checkStart(mouse_x, mouse_y):
    # Button coordinates might differ based on your image assets
    if 638 < mouse_x < 1097 and 260 < mouse_y < 392:
        startMusic()
        gameloop()

def welcomeFor():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            button_click_sound.play()
            return True

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            checkStart(mouse_x, mouse_y)

        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            startMusic()
            gameloop()
    return False

def text_screen(text, color, x, y):
    screen_text = regular_font.render(text, True, color)
    gameWindow.blit(screen_text, (x, y))

def plot_snake(surface, color, snk_list, snake_size):
    for seg_x, seg_y in snk_list:
        pygame.draw.circle(surface, color, [seg_x, seg_y], snake_size - 5)

def welcome():
    exit_game = False
    while not exit_game:
        gameWindow.blit(wlcimg, (0, 0))
        exit_game = welcomeFor()
        pygame.display.update()
        clock.tick(60)

    button_click_sound.play()
    pygame.time.delay(750)
    pygame.quit()
    exit()

def displayScore(score):
    Score_end = score_font.render(str(score), True, WHITE)
    Score_end_pos = (605, 480)
    gameWindow.blit(Score_end, Score_end_pos)

def resetMusic():
    pygame.mixer.music.load("reset.mp3")
    pygame.mixer.music.play()
    welcome()

def resetFor():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return True

        if event.type == pygame.MOUSEBUTTONDOWN:
            if checkMClickButton(pygame.mouse.get_pos(), (488, 583), (710, 658)):
                resetMusic()

        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            resetMusic()

    return False

def checkMClickButton(act_pos, min_pos, max_pos):
    x, y = act_pos
    x1, y1 = min_pos
    x2, y2 = max_pos
    return x1 < x < x2 and y1 < y < y2

def gameInputs(velocity_x, velocity_y, top_v):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return True, velocity_x, velocity_y, top_v

        if event.type == pygame.KEYDOWN:
            # Movement with constraints to prevent reversing direction directly
            if event.key == pygame.K_RIGHT and velocity_x != -top_v:
                velocity_x, velocity_y = top_v, 0
            elif event.key == pygame.K_LEFT and velocity_x != top_v:
                velocity_x, velocity_y = -top_v, 0
            elif event.key == pygame.K_UP and velocity_y != top_v:
                velocity_x, velocity_y = 0, -top_v
            elif event.key == pygame.K_DOWN and velocity_y != -top_v:
                velocity_x, velocity_y = 0, top_v
            elif event.key == pygame.K_ESCAPE:
                # Pause (if desired, currently just stops movement)
                velocity_x, velocity_y = 0, 0
    return False, velocity_x, velocity_y, top_v

def boundaryCondition(x, y):
    if x < 0 or x > SCREEN_WIDTH or y < 0 or y > SCREEN_HEIGHT:
        pygame.mixer.music.load("gover.mp3")
        pygame.mixer.music.play()
        return True
    return False

def gameloop():
    fps = 90
    score = 0
    exit_game = False
    game_over = False

    snake_x = SCREEN_WIDTH / 2
    snake_y = SCREEN_HEIGHT / 2
    snake_size = 17
    snk_length = 1

    velocity_x = 0
    velocity_y = 0
    top_v = 1

    # Food coordinates
    food_x = random.randint(SCREEN_WIDTH // 10, (3 * SCREEN_WIDTH) // 4)
    food_y = random.randint(SCREEN_HEIGHT // 10, (3 * SCREEN_HEIGHT) // 4)

    highscore = int(load_highscore())

    # Use deque for efficient removal and addition
    snk_list = deque()
    snk_positions = set()

    while not exit_game:
        if game_over:
            save_highscore(highscore)
            gameWindow.blit(overimg, (0, 0))
            displayScore(score)
            exit_game = resetFor()
        else:
            exit_game, velocity_x, velocity_y, top_v = gameInputs(velocity_x, velocity_y, top_v)
            if exit_game:
                break

            snake_x += velocity_x
            snake_y += velocity_y

            # Check boundary
            if boundaryCondition(snake_x, snake_y):
                game_over = True

            # Check if snake ate the food
            if abs(snake_x - food_x) < 15 and abs(snake_y - food_y) < 15:
                score += 10
                food_x = random.randint(SCREEN_WIDTH // 10, SCREEN_WIDTH // 2)
                food_y = random.randint(SCREEN_HEIGHT // 10, SCREEN_HEIGHT // 2)
                snk_length += 7.5
                top_v += 0.1
                if score > highscore:
                    highscore = score
                eat_sound.play()
                pygame.mixer.music.unpause()

            # Update snake's head
            head = (int(snake_x), int(snake_y))
            snk_list.append(head)
            snk_positions.add(head)

            if len(snk_list) > snk_length:
                tail = snk_list.popleft()
                snk_positions.discard(tail)

            # Check self-collision
            # Since the head is the last element, we can just check if it's duplicated
            if snk_list.count(head) > 1:
                pygame.mixer.music.load("gover.mp3")
                pygame.mixer.music.play()
                game_over = True

            gameWindow.fill(WHITE)
            gameWindow.blit(bgimg, (0, 0))

            # Draw food
            pygame.draw.circle(gameWindow, RED, [food_x, food_y], snake_size - 5)

            # Draw snake
            plot_snake(gameWindow, BLACK, snk_list, snake_size)

            # Display Score
            Score_disp = futuristic_font.render(f"Score: {score}   High Score: {highscore}", True, RED)
            gameWindow.blit(Score_disp, (5, 5))

        pygame.display.update()
        clock.tick(fps)

    button_click_sound.play()
    pygame.time.delay(500)
    pygame.quit()
    exit()

welcome()
