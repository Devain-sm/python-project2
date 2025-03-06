import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the game window
width, height = 1600, 900
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Water Gun Game")

# Colors
BLUE = (0, 120, 255)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Game variables
player_x = 400  # Starting position of water gun
player_speed = 5
water_drops = []  # Stores positions of water projectiles
targets = []  # Stores positions of targets
score = 0

# Clock to control game speed
clock = pygame.time.Clock()

# Main game loop
running = True
while running:
    screen.fill(WHITE)  # Clear screen
    
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Shoot water with SPACE key
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                water_drops.append([player_x + 15, 550])  # Add new water drop

    # Move player with LEFT/RIGHT arrows
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < 760:
        player_x += player_speed

    # Update water drops (move upward)
    for drop in water_drops:
        drop[1] -= 7  # Move upward
        pygame.draw.circle(screen, BLUE, (drop[0], drop[1]), 5)
        # Remove drops that go off-screen
        if drop[1] < 0:
            water_drops.remove(drop)

    # Spawn targets randomly
    if random.random() < 0.02:  # 2% chance per frame
        targets.append([random.randint(50, 750), 0])

    # Update targets (move downward)
    for target in targets:
        target[1] += 3  # Move downward
        pygame.draw.circle(screen, RED, (int(target[0]), int(target[1])), 20)
        # Remove targets that reach bottom
        if target[1] > 600:
            targets.remove(target)

    # Collision detection
    for drop in water_drops:
        for target in targets:
            # Check distance between water drop and target
            dx = drop[0] - target[0]
            dy = drop[1] - target[1]
            if (dx*dx + dy*dy) < 625:  # 25^2 (collision radius)
                targets.remove(target)
                water_drops.remove(drop)
                score += 10

    # Draw player (water gun)
    pygame.draw.rect(screen, BLUE, (player_x, 550, 30, 40))  # Gun base
    pygame.draw.circle(screen, BLUE, (player_x + 15, 540), 10)  # Gun nozzle

    # Display score
    font = pygame.font.SysFont(None, 36)
    text = font.render(f"Score: {score}", True, BLUE)
    screen.blit(text, (10, 10))

    pygame.display.update()
    clock.tick(120)  # 30 FPS

pygame.quit()