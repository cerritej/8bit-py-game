# spaceship.py
import pygame

class Spaceship:
    def __init__(self, name, x, y, width, height):
        self.__name = name
        self.__x = x
        self.__y = y
        self.__width = width
        self.__height = height
        self.__lives = 5
        self.__hit_by_projectile = False  # Flag to track if the spaceship has been hit by a projectile

    @property
    def name(self):
        return self.__name

    @property
    def x(self):
        return self.__x

    @x.setter
    def x(self, x):
        self.__x = x

    @property
    def y(self):
        return self.__y

    @y.setter
    def y(self, y):
        self.__y = y

    @property
    def width(self):
        return self.__width

    @width.setter
    def width(self, width):
        self.__width = width

    @property
    def height(self):
        return self.__height

    @height.setter
    def height(self, height):
        self.__height = height

    @property
    def lives(self):
        return self.__lives

    @lives.setter
    def lives(self, new_lives):
        if new_lives < 0:
            raise ValueError("Lives cannot be negative.")
        self.__lives = new_lives

    def decrement_lives(self):
        if self.__lives > 0:
            self.__lives -= 1

    def increment_lives(self):
        if self.__lives > 0:
            self.__lives += 1

    def move(self, dx, dy):
        # Ensure the spaceship stays within the screen boundaries in the x-direction
        new_x = self.__x + dx
        if 0 <= new_x <= (800 - self.__width):  # Max x-bounds, dependent on the screen width
            self.__x = new_x

        self.__y += dy

    def is_hit_by_enemy(self, projectile):
        if not self.__hit_by_projectile and (self.__x < projectile.x < self.__x + self.__width) and (
                self.__y < projectile.y < self.__y + self.__height):
            print(f"Spaceship hit by enemy projectile: {self.__x}, {self.__y}, {self.__width}, {self.__height}")
            self.__hit_by_projectile = True  # Set the flag to True to indicate the spaceship has been hit
            return True
        return False

    def reset_hit_status(self):
        # Reset hit status for the next frame
        self.__hit_by_projectile = False

