# enemy.py
import pygame
from projectile import Projectile

class Enemy:
    def __init__(self, x, y, width, height, speed, shoot_rate):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed
        self.shoot_rate = shoot_rate
        self.last_shot_time = 0
        self.is_alive = True  # New state to track whether the enemy is alive
        self.color = (255, 0, 0)  # Initial color
        self.destroyed_time = None  # Time when the enemy was destroyed

    def move(self):
        if self.is_alive:
            self.x += self.speed

            # Adjust the y-coordinate to move along the top side of the screen
            self.y = max(self.y, 0)

            # If the enemy reaches the left side, reset its position to the right
            if self.x < 0:
                self.x = pygame.display.get_surface().get_width()
                self.y = pygame.display.get_surface().get_height() // 4  # Adjust as needed
        elif self.destroyed_time is not None:
            # Check if it's been 1 second since the enemy was destroyed
            current_time = pygame.time.get_ticks()
            time_since_destroyed = current_time - self.destroyed_time
            if time_since_destroyed >= 1000:
                # If 1 second has passed, mark the enemy as no longer alive
                self.is_alive = False

    def shoot_projectile(self):
        if self.is_alive:
            current_time = pygame.time.get_ticks()
            time_since_last_shot = current_time - self.last_shot_time

            if time_since_last_shot > self.shoot_rate:
                # Create a projectile and return it
                projectile = Projectile(x=self.x + self.width // 2 - 5,
                                        y=self.y + self.height,
                                        width=10,
                                        height=20,  # Adjust the height as needed
                                        speed=8,   # Adjust the speed as needed
                                        length=20)  # Adjust the length as needed
                self.last_shot_time = current_time
                return projectile
            else:
                return None

    def is_hit(self, projectile):
        # Check if the enemy is hit by a projectile
        if self.is_alive:
            hit_condition = (self.x < projectile.x < self.x + self.width) and (self.y < projectile.y < self.y + self.height)
            if hit_condition:
                self.is_alive = False
                self.color = (0, 0, 0)  # Change color to black
                self.destroyed_time = pygame.time.get_ticks()  # Record the time when the enemy was destroyed
            return hit_condition
        else:
            return False
