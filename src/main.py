# main.py
import pygame
import sys
from spaceship import Spaceship
from projectile import Projectile


def main():
    pygame.init()

    width, height = 800, 600
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("8bit Game")
    white = (255, 255, 255)

    player_spaceship = Spaceship(name="Player", x=width // 2, y=height - 60, width=50, height=50)

    # Create a list to store projectiles
    projectiles = []

    clock = pygame.time.Clock()

    # Define a variable to store the time of the last shot
    last_shot_time = 0

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

        # Limit the rate of shooting to at most twice per second
        current_time = pygame.time.get_ticks()
        time_since_last_shot = current_time - last_shot_time
        if keys[
            pygame.K_SPACE] and time_since_last_shot > 200:  # Allow shooting every 200 milliseconds (five per second)
            new_projectile = Projectile(x=player_spaceship.x + player_spaceship.width // 2 - 5,
                                        y=player_spaceship.y,
                                        width=10,
                                        height=player_spaceship.height,
                                        speed=10,
                                        length=player_spaceship.height)
            projectiles.append(new_projectile)
            last_shot_time = current_time

        screen.fill(white)

        # Draw the player spaceship
        pygame.draw.rect(screen, (0, 128, 255),
                         (player_spaceship.x, player_spaceship.y, player_spaceship.width, player_spaceship.height))

        # Update and draw projectiles
        for projectile in projectiles:
            projectile.update()
            projectile.render(screen)

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
