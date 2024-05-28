import pygame
import time
import random

# PYGAME INITIALISATION (?)
pygame.init()

# FONT INITIALISATION
pygame.font.init()

WIDTH, HEIGHT = 1600, 900
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Asteroid Evaders")

# GAME ICON
icon = pygame.image.load("./assets/SpaceSmall-2.png").convert()
pygame.display.set_icon(icon)

# TITLE WIN - GLOBAL
game_state = "start_menu"


# Define Background Image
BG = pygame.transform.scale(
    pygame.image.load("./assets/Background-Image.jpg"), (WIDTH, HEIGHT)
)

# Define Player ATTRIBUTES
PLAYER_HP = 5
PLAYER_WIDTH = 40
PLAYER_HEIGHT = 60
PLAYER_VEL = 5

# Define Projectile ATTRIBUTES
STAR_WIDTH = 30
STAR_HEIGHT = 20
STAR_VEL = 1

# FONT
FONT = pygame.font.SysFont("Verdana", 26)


# Start Menu Draw Function
def draw_start_menu():
    WIN.fill((0, 0, 0))
    font = pygame.font.SysFont("arial", 40)
    title = font.render("My Game", True, (255, 255, 255))
    start_button = font.render("Start", True, (255, 255, 255))
    WIN.blit(
        title,
        (
            WIDTH / 2 - title.get_width() / 2,
            HEIGHT / 2 - title.get_height() / 2,
        ),
    )
    WIN.blit(
        start_button,
        (
            WIDTH / 2 - start_button.get_width() / 2,
            HEIGHT / 2 + start_button.get_height() / 2,
        ),
    )
    pygame.display.update()


# Draw Function
def draw(player: pygame.Rect, elapsed_time: float, astroids: list, hp) -> None:
    # Draw Background Image
    WIN.blit(BG, (0, 0))

    # Draw Player
    pygame.draw.rect(WIN, "purple", player)  # CAN: string color OR RGB-color code

    # Elapsed Time
    time_text = FONT.render(f"Time: {round(elapsed_time, 1)}s", 1, "white")
    WIN.blit(time_text, (10, 10))

    # Elapsed Time
    time_text = FONT.render(f"Lives Left: {hp}/5", 1, "white")
    WIN.blit(time_text, (10, 40))

    # Draw astroids
    for astroid in astroids:
        pygame.draw.rect(WIN, "white", astroid)

    pygame.display.update()


# Main
def main() -> None:
    run = True

    # Player
    player = pygame.Rect(
        WIDTH / 2, HEIGHT - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT
    )  # PLAYER will appear @ Bottom-Centre of WIN W/ HGHT of 60 && WDTH of 40

    # CLOCK
    clock = pygame.time.Clock()

    # Start Time
    start_time = time.time()
    elapsed_time = 0

    # Projectile Initialisation
    star_add_increment = 2000
    star_count = 0
    astroids = []

    # Hit Check
    hp = PLAYER_HP

    # Main Game Loop
    while run:
        # Clock Ticking + astroid Generating
        star_count += clock.tick(60)  # 60 FPS
        elapsed_time = time.time() - start_time

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        # Movement
        keys = pygame.key.get_pressed()
        # LEFT MOVEMENT
        if keys[pygame.K_a] and player.x - PLAYER_VEL >= 0:
            player.x -= PLAYER_VEL
        # RIGHT MOVEMENT
        if keys[pygame.K_d] and player.x + PLAYER_VEL + player.width <= WIDTH:
            player.x += PLAYER_VEL
        # UP MOVEMENT
        if keys[pygame.K_w] and player.y - PLAYER_VEL >= 0:
            player.y -= PLAYER_VEL  # Verticle Speed = 1/2 Horizontal Speed
        # DOWN MOVEMENT
        if keys[pygame.K_s] and player.y + PLAYER_VEL + player.height <= HEIGHT:
            player.y += PLAYER_VEL  # Verticle Speed = 1/2 Horizontal Speed

        # Generate astroids
        if star_count > star_add_increment:
            for _ in range(2):
                star_x = random.randint(0, WIDTH - STAR_WIDTH)
                astroid = pygame.Rect(star_x, -STAR_HEIGHT, STAR_WIDTH, STAR_HEIGHT)
                astroids.append(astroid)

            star_add_increment = max(200, star_add_increment - 50)
            star_count = 0

        # PROJECTILE MOVEMENT
        for astroid in astroids[:]:
            astroid.y += STAR_VEL
            if astroid.y > HEIGHT:
                astroids.remove(astroid)
            elif astroid.y + astroid.height >= player.y and astroid.colliderect(player):
                astroids.remove(astroid)
                hp -= 1
                break

        if hp <= 0:
            lost_text = FONT.render("You Lost!", 1, "white")
            WIN.blit(
                lost_text,
                (
                    WIDTH / 2 - lost_text.get_width() / 2,
                    HEIGHT / 2 - lost_text.get_height() / 2,
                ),
            )
            pygame.display.update()
            pygame.time.delay(7000)
            break

        # Draw Elements
        draw(player, elapsed_time, astroids, hp)
    pygame.quit()


if __name__ == "__main__":
    main()
