# game_manager.py
import pygame
import sys
from spaceship import Spaceship
from enemy import Enemy
from projectile import Projectile
import random

class GameManager:
    # Class-level variables to track game state
    player_spaceship = None  # Default value at the class level
    player_projectiles = []  # Default value at the class level
    enemy_projectiles = []  # Default value at the class level
    enemies = []  # Default value at the class level

    def __init__(self, width, height):
        """
        Initializes the game manager with the specified width and height.

        Args:
            width (int): Width of the game window.
            height (int): Height of the game window.
        """
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("8bit Game")
        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
        self.red = (255, 0, 0)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.last_player_shot_time = 0
        self.score = 0  # Initialize score
        self.reset_game()

    def reset_game(self):
        """
        Resets the game state to the initial configuration.
        """
        self.player_spaceship = Spaceship(name="Player", x=self.screen.get_width() // 2,
                                          y=self.screen.get_height() - 60, width=50, height=50)
        self.player_projectiles = []
        self.enemy_projectiles = []
        self.enemies = [Enemy(eid=1, x=60, y=60, speed=-2, shoot_rate=2000)]
        self.score = 0  # Reset score to 0 on restart

    def handle_input(self):
        """
        Handles user input events, such as key presses and window close.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.player_spaceship.move(-5, 0)
        if keys[pygame.K_RIGHT]:
            self.player_spaceship.move(5, 0)
        if keys[pygame.K_SPACE]:
            self.shoot_projectile()

    def shoot_projectile(self):
        """
        Fires a projectile from the player's spaceship if the cooldown time has passed.
        """
        current_time = pygame.time.get_ticks()
        time_since_last_shot = current_time - self.last_player_shot_time
        if time_since_last_shot > 200:
            new_projectile = Projectile(x=self.player_spaceship.x + self.player_spaceship.width // 2 - 5,
                                        y=self.player_spaceship.y,
                                        width=10,
                                        height=self.player_spaceship.height,
                                        speed=10,
                                        length=self.player_spaceship.height,
                                        direction="up")
            self.player_projectiles.append(new_projectile)
            self.last_player_shot_time = current_time

    def update_game_state(self):
        """
        Updates the game state, including moving objects, handling collisions, and updating scores.
        """
        for enemy in self.enemies:
            enemy.move()
            new_enemy_projectile = enemy.shoot_projectile()
            if new_enemy_projectile:
                self.enemy_projectiles.append(new_enemy_projectile)

        # Update projectile positions
        for projectile in self.player_projectiles + self.enemy_projectiles:
            projectile.move()

        # Check for collisions and remove enemies immediately
        self.check_enemy_collisions()

        # Check for collisions with player spaceship
        self.check_player_collision()

        # Update blinking status of the player spaceship
        self.player_spaceship.update_blinking()

    def check_enemy_collisions(self):
        """
        Checks for collisions between player projectiles and enemies, updating scores and spawning new enemies.
        """
        enemies_to_remove = []
        for projectile in self.player_projectiles:
            for enemy in self.enemies:
                if enemy.is_hit_by_player(projectile):
                    # Handle enemy hit
                    print(f"Enemy {enemy.eid} hit!")
                    enemies_to_remove.append(enemy)
                    self.score += 10  # Increase the score when an enemy is hit

        for enemy in enemies_to_remove:
            self.enemies.remove(enemy)

            # If the enemy with ID 1 is hit, spawn two new enemies
            if enemy.eid == 1:
                self.enemies.extend([Enemy(eid=2, x=100, y=100, speed=-2, shoot_rate=2000),
                                     Enemy(eid=3, x=700, y=100, speed=-2, shoot_rate=2000)])
            elif enemy.eid == 2 or enemy.eid == 3:
                # If enemies with ID 2 and 3 are both destroyed, spawn a new enemy with ID 4
                if all(e.eid not in [2, 3] for e in self.enemies):
                    self.enemies.append(Enemy(eid=4, x=50, y=50, speed=-6, shoot_rate=750))
            elif enemy.eid == 4:
                # If enemy with ID 4 is destroyed, spawn three new enemies with ID 5, 6, and 7
                self.enemies.extend([Enemy(eid=5, x=100, y=100, speed=-2, shoot_rate=2000),
                                     Enemy(eid=6, x=400, y=100, speed=-2, shoot_rate=2000),
                                     Enemy(eid=7, x=700, y=100, speed=-2, shoot_rate=2000)])
            elif enemy.eid == 5 or enemy.eid == 6 or enemy.eid == 7:
                # If enemies with ID 5, 6, and 7 are all destroyed, spawn two new enemies with ID 8 and 9
                if all(e.eid not in [5, 6, 7] for e in self.enemies):
                    self.enemies.extend([Enemy(eid=8, x=100, y=100, speed=-4, shoot_rate=750),
                                         Enemy(eid=9, x=700, y=100, speed=-4, shoot_rate=750)])
            elif enemy.eid == 8 or enemy.eid == 9:
                # If enemies with ID 8 and 9 are both destroyed, spawn three new enemies with ID 10, 11, and 12
                if all(e.eid not in [8, 9] for e in self.enemies):
                    self.enemies.extend([Enemy(eid=10, x=100, y=100, speed=-6, shoot_rate=1000),
                                         Enemy(eid=11, x=400, y=100, speed=-4, shoot_rate=750),
                                         Enemy(eid=12, x=700, y=100, speed=-2, shoot_rate=500)])

        # Check if all enemies are destroyed, then trigger randomization for the next group
        if not self.enemies:
            # Determine whether to use random values for the next group
            if all(e.eid >= 12 for e in enemies_to_remove):
                # Randomize characteristics for the next group
                next_group_size = random.randint(1, 4)
                next_group_start_id = max(e.eid for e in enemies_to_remove) + 1

                next_group = [
                    Enemy(
                        eid=i,
                        x=random.randint(100, 700),
                        y=random.randint(50, 150),
                        speed=random.uniform(-3, -6),
                        shoot_rate=random.randint(500, 1000),
                    )
                    for i in range(next_group_start_id, next_group_start_id + next_group_size)
                ]

                self.enemies.extend(next_group)

    def check_player_collision(self):
        """
        Checks for collisions between enemy projectiles and the player's spaceship, updating lives and hit status.
        """
        player_spaceship_hit = any(
            [self.player_spaceship.is_hit_by_enemy(projectile) for projectile in self.enemy_projectiles]
        )
        if player_spaceship_hit:
            print("Player spaceship hit!")
            self.player_spaceship.reset_hit_status()  # Reset hit status for the next frame
            self.player_spaceship.decrement_lives()  # Decrement lives when hit

    def draw_objects(self):
        """
        Draws game objects on the screen, including the player's spaceship, enemies, projectiles, lives, and score.
        """
        self.screen.fill(self.white)

        if self.player_spaceship.lives > 0:
            # Draw the player spaceship
            self.player_spaceship.draw(self.screen)

            # Draw the enemies with the updated color
            for enemy in self.enemies:
                pygame.draw.rect(self.screen, enemy.get_color(), (enemy.x, enemy.y, enemy.width, enemy.height))

            # Draw projectiles
            for projectile in self.player_projectiles:
                pygame.draw.rect(self.screen, (0, 255, 0),
                                 (projectile.x, projectile.y, projectile.width, projectile.length))
            for projectile in self.enemy_projectiles:
                pygame.draw.rect(self.screen, (255, 0, 0),
                                 (projectile.x, projectile.y, projectile.width, projectile.length))

            # Draw player lives
            lives_text = self.font.render(f"Lives: {self.player_spaceship.lives}", True, self.black)
            self.screen.blit(lives_text, (10, 10))  # Adjust the position as needed

            # Draw score
            score_text = self.font.render(f"Score: {self.score}", True, self.black)
            self.screen.blit(score_text, (120, 10))  # Adjust the position as needed
        else:
            # Player has no lives left, display "Game Over" message
            game_over_text = self.font.render("Game Over", True, self.red)
            text_rect = game_over_text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))
            self.screen.blit(game_over_text, text_rect)

            # Display the final score in black
            final_score_text = self.font.render(f"Final Score: {self.score}", True, self.black)
            final_score_rect = final_score_text.get_rect(
                center=(self.screen.get_width() // 2, self.screen.get_height() // 2 + 30))
            self.screen.blit(final_score_text, final_score_rect)

            # Prompt to restart the game
            restart_text = self.font.render("Press R to restart", True, self.black)
            restart_rect = restart_text.get_rect(
                center=(self.screen.get_width() // 2, self.screen.get_height() // 2 + 70))
            self.screen.blit(restart_text, restart_rect)

            keys = pygame.key.get_pressed()
            if keys[pygame.K_r]:
                self.reset_game()  # Restart the game if the player presses 'R'

        pygame.display.flip()
        self.clock.tick(60)
