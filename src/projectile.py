# projectile.py
import pygame


class Projectile:
    def __init__(self, x, y, width, height, speed, length, direction):
        """
        Initializes a projectile with specified characteristics.

        Args:
            x (int): Initial x-coordinate.
            y (int): Initial y-coordinate.
            width (int): Width of the projectile.
            height (int): Height of the projectile.
            speed (int): Speed of the projectile.
            length (int): Length of the projectile.
            direction (str): Direction of the projectile ("up" or "down").
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed
        self.length = length
        self.direction = direction

    def move(self):
        """
        Moves the projectile based on its direction and speed.
        """
        if self.direction == "up":
            self.y -= self.speed
        elif self.direction == "down":
            self.y += self.speed

    def draw(self, screen):
        """
        Draws the projectile on the given screen.

        Args:
            screen (pygame.Surface): The screen to draw the projectile on.
        """
        pygame.draw.rect(screen, (255, 0, 0), (self.x, self.y, self.width, self.length))

    def update(self):
        """
        Updates the state of the projectile by moving it.
        """
        self.move()

    def render(self, screen):
        """
        Renders the projectile by drawing it on the screen.

        Args:
            screen (pygame.Surface): The screen to render the projectile on.
        """
        self.draw(screen)
