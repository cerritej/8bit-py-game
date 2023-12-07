# projectile.py
import pygame


class Projectile:
    def __init__(self, x, y, width, height, speed, length):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed
        self.length = length

    def move(self):
        self.y -= self.speed

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), (self.x, self.y, self.width, self.length))

    def update(self):
        self.move()

    def render(self, screen):
        self.draw(screen)
