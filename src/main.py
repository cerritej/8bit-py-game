import pygame
import sys
from spaceship import Spaceship
from enemy import Enemy
from projectile import Projectile

def main():
    pygame.init()

    width, height = 800, 600
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("8bit Game")
    white = (255, 255, 255)
    black = (0, 0, 0)

    player_spaceship = Spaceship(name="Player", x=width // 2, y=height - 60, width=50, height=50, lives=5)

    # Create lists to store projectiles for both player and enemy
    player_projectiles = []
    enemy_projectiles = []

    enemy = Enemy(x=60, y=60, width=50, height=50, speed=-2,
                  shoot_rate=2000)  # Adjust speed and shoot_rate as needed

    # Font for displaying text
    font = pygame.font.Font(None, 36)

    clock = pygame.time.Clock()

    # Define a variable to store the time of the last player shot
    last_player_shot_time = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player_spaceship.move(-5, 0)
        if keys[pygame.K_RIGHT]:
            player_spaceship.move(5, 0)
        if keys[pygame.K_SPACE]:
            # Player shoots a projectile
            current_time = pygame.time.get_ticks()
            time_since_last_shot = current_time - last_player_shot_time
            if time_since_last_shot > 200:  # Allow shooting every 200 milliseconds (five per second)
                new_projectile = Projectile(x=player_spaceship.x + player_spaceship.width // 2 - 5,
                                            y=player_spaceship.y,
                                            width=10,
                                            height=player_spaceship.height,
                                            speed=10,
                                            length=player_spaceship.height,
                                            direction="up")
                player_projectiles.append(new_projectile)
                last_player_shot_time = current_time

        # Enemy behavior
        enemy.move()
        new_enemy_projectile = enemy.shoot_projectile()
        if new_enemy_projectile:
            enemy_projectiles.append(new_enemy_projectile)

        # Update projectile positions
        for projectile in player_projectiles:
            projectile.move()
        for projectile in enemy_projectiles:
            projectile.move()

        # Check for collisions
        for projectile in player_projectiles:
            if enemy.is_hit(projectile):
                # Handle enemy hit
                print("Enemy hit!")

        screen.fill(white)

        # Draw the player spaceship
        pygame.draw.rect(screen, (0, 128, 255),
                         (player_spaceship.x, player_spaceship.y, player_spaceship.width, player_spaceship.height))

        # Draw the enemy with the updated color
        pygame.draw.rect(screen, enemy.get_color(), (enemy.x, enemy.y, enemy.width, enemy.height))

        # Draw projectiles
        for projectile in player_projectiles:
            pygame.draw.rect(screen, (0, 255, 0), (projectile.x, projectile.y, projectile.width, projectile.length))
        for projectile in enemy_projectiles:
            pygame.draw.rect(screen, (255, 0, 0), (projectile.x, projectile.y, projectile.width, projectile.length))

        # Draw player lives
        lives_text = font.render(f"Lives: {player_spaceship.lives}", True, black)
        screen.blit(lives_text, (10, 10))  # Adjust the position as needed

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
