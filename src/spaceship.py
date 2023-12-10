import pygame


class Spaceship:
    def __init__(self, name, x, y, width, height):
        """Initializes a Spaceship object.

        Args:
            name (str): The name of the spaceship.
            x (int): The initial x-coordinate of the spaceship.
            y (int): The initial y-coordinate of the spaceship.
            width (int): The width of the spaceship.
            height (int): The height of the spaceship.
        """
        self.__name = name
        self.__x = x
        self.__y = y
        self.__width = width
        self.__height = height
        self.__lives = 5
        self.__hit_by_projectile = False  # Flag to track if the spaceship has been hit by a projectile
        self.__hit_cooldown = 1000  # Cooldown period in milliseconds
        self.__last_hit_time = 0
        self.__blink_duration = 1000  # Duration of the blinking effect in milliseconds
        self.__blink_timer = 0  # Timer to control the blinking effect
        self.__is_blinking = False  # Flag to indicate if the spaceship is currently blinking
        self.__blink_color = (255, 0, 0)  # Initial blink color is red

    @property
    def name(self):
        """Getter for the name property."""
        return self.__name

    @property
    def x(self):
        """Getter for the x property."""
        return self.__x

    @x.setter
    def x(self, x):
        """Setter for the x property."""
        self.__x = x

    @property
    def y(self):
        """Getter for the y property."""
        return self.__y

    @y.setter
    def y(self, y):
        """Setter for the y property."""
        self.__y = y

    @property
    def width(self):
        """Getter for the width property."""
        return self.__width

    @width.setter
    def width(self, width):
        """Setter for the width property."""
        self.__width = width

    @property
    def height(self):
        """Getter for the height property."""
        return self.__height

    @height.setter
    def height(self, height):
        """Setter for the height property."""
        self.__height = height

    @property
    def lives(self):
        """Getter for the lives property."""
        return self.__lives

    @lives.setter
    def lives(self, new_lives):
        """Setter for the lives property."""
        if new_lives < 0:
            raise ValueError("Lives cannot be negative.")
        self.__lives = new_lives

    def decrement_lives(self):
        """Decrements the number of lives if greater than 0."""
        if self.__lives > 0:
            self.__lives -= 1

    def increment_lives(self):
        """Increments the number of lives if greater than 0."""
        if self.__lives > 0:
            self.__lives += 1

    def move(self, dx, dy):
        """Moves the spaceship by the specified amount.

        Args:
            dx (int): The change in x-coordinate.
            dy (int): The change in y-coordinate.
        """
        # Ensure the spaceship stays within the screen boundaries in the x-direction
        new_x = self.__x + dx
        if 0 <= new_x <= (800 - self.__width):  # Max x-bounds, dependent on the screen width
            self.__x = new_x

        self.__y += dy

    def is_hit_by_enemy(self, projectile):
        """Checks if the spaceship is hit by an enemy projectile.

        Args:
            projectile (Projectile): The enemy projectile.

        Returns:
            bool: True if hit, False otherwise.
        """
        if not self.__hit_by_projectile and (self.__x < projectile.x < self.__x + self.__width) and (
                self.__y < projectile.y < self.__y + self.__height):
            current_time = pygame.time.get_ticks()
            time_since_last_hit = current_time - self.__last_hit_time

            if time_since_last_hit > self.__hit_cooldown:
                print(f"Spaceship hit by enemy projectile: {self.__x}, {self.__y}, {self.__width}, {self.__height}")
                self.__hit_by_projectile = True
                self.__last_hit_time = current_time
                self.start_blinking()  # Start the blinking effect
                return True

        return False

    def reset_hit_status(self):
        """Resets hit status for the next frame."""
        self.__hit_by_projectile = False

    def draw(self, screen):
        """Draws the spaceship on the screen.

        Args:
            screen (pygame.Surface): The surface to draw on.
        """
        current_time = pygame.time.get_ticks()

        if self.__is_blinking:
            elapsed_time = current_time - self.__blink_timer

            if elapsed_time <= self.__blink_duration:
                # Double the blink rate: switch between red and green every 250 milliseconds
                if elapsed_time % 250 < 125:  # Blink every 500 milliseconds, switch color every 250 milliseconds
                    self.__blink_color = (255, 0, 0)  # Red
                else:
                    self.__blink_color = (0, 0, 255)  # Blue

                pygame.draw.rect(screen, self.__blink_color, (self.__x, self.__y, self.__width, self.__height))
            else:
                # Stop blinking after one second
                self.__is_blinking = False
        else:
            # Draw the spaceship normally
            pygame.draw.rect(screen, (0, 128, 255), (self.__x, self.__y, self.__width, self.__height))

    def start_blinking(self):
        """Starts the blinking effect."""
        self.__is_blinking = True
        self.__blink_timer = pygame.time.get_ticks()

    def stop_blinking(self):
        """Stops the blinking effect."""
        self.__is_blinking = False

    def update_blinking(self):
        """Updates the blinking effect."""
        current_time = pygame.time.get_ticks()

        if self.__is_blinking:
            elapsed_time = current_time - self.__blink_timer

            if elapsed_time <= self.__blink_duration:
                # Blinking pattern: switch between red and green
                if elapsed_time % 500 < 250:  # Blink every 500 milliseconds, switch color every 250 milliseconds
                    self.__blink_color = (255, 0, 0)  # Red
                else:
                    self.__blink_color = (0, 255, 0)  # Green

            else:
                # Stop blinking after one second
                self.__is_blinking = False
