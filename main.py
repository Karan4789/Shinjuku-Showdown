import pygame
import sys


# Initialize Pygame
pygame.init()

#Initialize Pygame mixer
pygame.mixer.init()

# Load and play background music
pygame.mixer.music.load("Assets/background_music.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)



# Screen settings
WIDTH, HEIGHT = 800, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shinjuku Showdown")
icon = pygame.image.load("Assets/punch.png")
pygame.display.set_icon(icon)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
PURPLE = (128, 0, 128)
GREEN = (0, 255, 0)

# Player settings
PLAYER_WIDTH, PLAYER_HEIGHT = 50, 70
PLAYER_SPEED = 5
BULLET_SPEED = 10
GRAVITY = 0.5
JUMP_STRENGTH = 10





# Load assets
player1_image = pygame.image.load("Assets/gojo.png")
player1_image = pygame.transform.scale(player1_image, (PLAYER_WIDTH, PLAYER_HEIGHT))
player2_image = pygame.image.load("Assets/sukuna1.png")
player2_image = pygame.transform.scale(player2_image, (PLAYER_WIDTH, PLAYER_HEIGHT))
heart_image = pygame.image.load("Assets/heart.png")
heart_image = pygame.transform.scale(heart_image, (20, 20))
background_image = pygame.image.load("Assets/background.png")
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

# Platform settings
platforms = [
    pygame.Rect(90, HEIGHT - 200, 100, 10),
    pygame.Rect(150, HEIGHT - 100, 100, 10),
    pygame.Rect(380, HEIGHT - 200, 100, 10),
    pygame.Rect(550, HEIGHT - 100, 100, 10),
    pygame.Rect(650, HEIGHT - 200, 100, 10),
]

# Player 2 bullet shape settings
BULLET_LENGTH = 20  # Length of the slanted bullet
bullet_colors = [RED, BLUE, PURPLE]
bullet_color_index = 0

game_started = False

# Define fonts for the start menu
font = pygame.font.SysFont("Arial", 50)  
button_font = pygame.font.SysFont("Arial", 30)


# Function to reset the game
def reset_game():
    global player1, player2, player1_velocity_y, player2_velocity_y, player1_lives, player2_lives, player1_bullets, player2_bullets
    player1 = pygame.Rect(50, HEIGHT - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT)
    player2 = pygame.Rect(WIDTH - 100, HEIGHT - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT)
    player1_velocity_y = 0
    player2_velocity_y = 0
    player1_lives = 5
    player2_lives = 5
    player1_bullets = []
    player2_bullets = []

# Initialize game state
reset_game()
game_over = False
clock = pygame.time.Clock()

def show_start_menu():
    global running, game_started
    start_menu = True
    while start_menu:
        screen.fill(WHITE)
        title_text = font.render("Shinjuku Showdown", True, BLACK)
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 4))
        start_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 25, 200, 50)
        pygame.draw.rect(screen, BLACK, start_button)
        button_text = button_font.render("Start", True, WHITE)
        screen.blit(button_text, (WIDTH // 2 - button_text.get_width() // 2, HEIGHT // 2 - 15))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if start_button.collidepoint(mouse_x, mouse_y):
                    start_menu = False
                    game_started = True
                    pygame.mixer.music.set_volume(1.0) 
        pygame.display.flip()

show_start_menu()  #start menu


# Main game loop
running = True
while running:
    clock.tick(60)
    screen.blit(background_image, (0, 0))

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and not game_over:
            # Player 1 and 2 shoot bullet
            if event.key == pygame.K_w:  # Player 1 shoots
                bullet = pygame.Rect(player1.x + PLAYER_WIDTH, player1.y + PLAYER_HEIGHT // 2 - 5, 10, 5)
                player1_bullets.append((bullet, bullet_colors[bullet_color_index]))
                bullet_color_index = (bullet_color_index + 1) % len(bullet_colors)
            elif event.key == pygame.K_UP:  # Player 2 shoots slanted bullets
                bullet_start = [player2.x - 10, player2.y + PLAYER_HEIGHT // 2 - 5]
                bullet_end = [bullet_start[0] - BULLET_LENGTH, bullet_start[1] + BULLET_LENGTH]
                player2_bullets.append((bullet_start, bullet_end))
            # Player 1 and 2 jump if they are on the ground or a platform
            elif event.key == pygame.K_SPACE and player1_velocity_y == 0:
                player1_velocity_y = -JUMP_STRENGTH
            elif event.key == pygame.K_RSHIFT and player2_velocity_y == 0:
                player2_velocity_y = -JUMP_STRENGTH
        elif event.type == pygame.MOUSEBUTTONDOWN and game_over:
            mouse_x, mouse_y = event.pos
            if restart_button.collidepoint(mouse_x, mouse_y):
                reset_game()
                game_over = False

    # Update player movement if game is not over
    if not game_over:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and player1.x > 0:
            player1.x -= PLAYER_SPEED
        if keys[pygame.K_d] and player1.x < WIDTH - PLAYER_WIDTH:
            player1.x += PLAYER_SPEED
        if keys[pygame.K_LEFT] and player2.x > 0:
            player2.x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT] and player2.x < WIDTH - PLAYER_WIDTH:
            player2.x += PLAYER_SPEED

        # Apply gravity
        player1_velocity_y += GRAVITY
        player1.y += player1_velocity_y
        player2_velocity_y += GRAVITY
        player2.y += player2_velocity_y

        # Collision detection for platforms
        for platform in platforms:
            if player1.colliderect(platform) and player1_velocity_y > 0:
                player1.y = platform.y - PLAYER_HEIGHT
                player1_velocity_y = 0
            if player2.colliderect(platform) and player2_velocity_y > 0:
                player2.y = platform.y - PLAYER_HEIGHT
                player2_velocity_y = 0

        # Collision with the ground
        if player1.y + PLAYER_HEIGHT >= HEIGHT:
            player1.y = HEIGHT - PLAYER_HEIGHT
            player1_velocity_y = 0
        if player2.y + PLAYER_HEIGHT >= HEIGHT:
            player2.y = HEIGHT - PLAYER_HEIGHT
            player2_velocity_y = 0

        # Update Player 1 bullets
        for bullet, color in player1_bullets[:]:
            bullet.x += BULLET_SPEED
            if bullet.colliderect(player2):
                player2_lives -= 1
                player1_bullets.remove((bullet, color))
            elif bullet.x > WIDTH:
                player1_bullets.remove((bullet, color))

        # Update Player 2 bullets
        for bullet_start, bullet_end in player2_bullets[:]:
            bullet_start[0] -= BULLET_SPEED
            bullet_end[0] -= BULLET_SPEED
            if pygame.Rect(bullet_start[0], bullet_start[1], BULLET_LENGTH, 5).colliderect(player1):
                player1_lives -= 1
                player2_bullets.remove((bullet_start, bullet_end))
            elif bullet_start[0] < 0 :
                player2_bullets.remove((bullet_start, bullet_end))

        # Check for game over
        if player1_lives <= 0 or player2_lives <= 0:
            game_over = True

    # Draw platforms
    for platform in platforms:
        pygame.draw.rect(screen, WHITE, platform)

    # Draw bullets
    for bullet, color in player1_bullets:
        pygame.draw.rect(screen, color, bullet)
    for bullet_start, bullet_end in player2_bullets:
        pygame.draw.line(screen, RED, bullet_start, bullet_end, 3)

    # Draw players
    screen.blit(player1_image, (player1.x, player1.y))
    screen.blit(player2_image, (player2.x, player2.y))

    # Draw lives
    for i in range(player1_lives):
        screen.blit(heart_image, (20 + i * 25, 20))
    for i in range(player2_lives):
        screen.blit(heart_image, (WIDTH - 160 + i * 25, 20))

    # Display game over screen
    if game_over:
        font = pygame.font.Font(None, 74)
        text = font.render("You are Defeated", True, BLACK)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - 50))
        restart_button = pygame.Rect(WIDTH // 2 - 50, HEIGHT // 2 + 20, 100, 50)
        pygame.draw.rect(screen, BLACK, restart_button)
        restart_text = pygame.font.Font(None, 36).render("Restart", True, WHITE)
        screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 30))

    pygame.display.flip()

pygame.quit()
sys.exit()
