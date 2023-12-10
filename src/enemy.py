# enemy.py
import pygame
from projectile import Projectile

class Enemy:
    def __init__(self, eid, x, y, speed, shoot_rate):
        """
        Initializes an enemy with specified characteristics.

        Args:
            eid (int): Enemy ID.
            x (int): Initial x-coordinate.
            y (int): Initial y-coordinate.
            speed (int): Speed of the enemy.
            shoot_rate (int): Rate at which the enemy can shoot projectiles.
        """
        self.__eid = eid
        self.__x = x
        self.__y = y
        self.__width = 50
        self.__height = 50
        self.__speed = speed
        self.__shoot_rate = shoot_rate
        self.__last_shot_time = 0
        self.__is_alive = True
        self.__color = (255, 0, 0)
        self.__destroyed_time = None
        self.__direction = -1

    @property
    def eid(self):
        return self.__eid

    @eid.setter
    def eid(self, new_eid):
        self.__eid = new_eid

    @property
    def x(self):
        return self.__x

    @x.setter
    def x(self, new_x):
        self.__x = new_x

    @property
    def y(self):
        return self.__y

    @y.setter
    def y(self, new_y):
        self.__y = new_y

    @property
    def width(self):
        return self.__width

    @width.setter
    def width(self, new_width):
        self.__width = new_width

    @property
    def height(self):
        return self.__height

    @height.setter
    def height(self, new_height):
        self.__height = new_height

    @property
    def speed(self):
        return self.__speed

    @speed.setter
    def speed(self, new_speed):
        self.__speed = new_speed

    @property
    def shoot_rate(self):
        return self.__shoot_rate

    @shoot_rate.setter
    def shoot_rate(self, new_shoot_rate):
        self.__shoot_rate = new_shoot_rate

    @property
    def is_alive(self):
        return self.__is_alive

    @is_alive.setter
    def is_alive(self, new_is_alive):
        self.__is_alive = new_is_alive

    def get_color(self):
        """
        Returns the color of the enemy.

        Returns:
            Tuple: RGB color tuple.
        """
        return self.__color

    def get_destroyed_time(self):
        """
        Returns the time when the enemy was destroyed.

        Returns:
            int: Time in milliseconds.
        """
        return self.__destroyed_time

    def move(self):
        """
        Moves the enemy horizontally, handles boundary conditions, and resets position if necessary.
        """
        if self.__is_alive:
            self.__x += self.__speed * self.__direction

            if self.__x < 0 or self.__x > pygame.display.get_surface().get_width() - self.__width:
                self.__direction *= -1
                self.__x = max(0, min(self.__x, pygame.display.get_surface().get_width() - self.__width))

            self.__y = max(self.__y, 0)

            if self.__x < 0:
                self.__x = pygame.display.get_surface().get_width()
                self.__y = pygame.display.get_surface().get_height() // 4
        elif self.__destroyed_time is not None:
            current_time = pygame.time.get_ticks()
            time_since_destroyed = current_time - self.__destroyed_time
            if time_since_destroyed >= 1000:
                self.__is_alive = False

    def shoot_projectile(self):
        """
        Fires a projectile if the enemy is alive and enough time has passed since the last shot.

        Returns:
            Projectile: A new projectile if conditions are met, otherwise None.
        """
        if self.__is_alive:
            current_time = pygame.time.get_ticks()
            time_since_last_shot = current_time - self.__last_shot_time

            if time_since_last_shot > self.__shoot_rate:
                projectile = Projectile(x=self.__x + self.__width // 2 - 5,
                                        y=self.__y - 20,
                                        width=10,
                                        height=20,
                                        speed=8,
                                        length=20,
                                        direction="down")
                self.__last_shot_time = current_time
                return projectile
            else:
                return None

    def is_hit_by_player(self, projectile):
        """
        Checks if the enemy is hit by a player's projectile.

        Args:
            projectile (Projectile): The player's projectile.

        Returns:
            bool: True if hit, False otherwise.
        """
        if self.__is_alive:
            hit_condition = (self.__x < projectile.x < self.__x + self.__width) and (
                        self.__y < projectile.y < self.__y + self.__height)
            if hit_condition:
                self.__is_alive = False
                self.__color = (0, 0, 0)
                self.__destroyed_time = pygame.time.get_ticks()
            return hit_condition
        else:
            return False
