# game_manager.py
import pygame
import sys
from spaceship import Spaceship
from enemy import Enemy
from projectile import Projectile

class GameManager:
    player_spaceship = None  # Default value at the class level
    player_projectiles = []   # Default value at the class level
    enemy_projectiles = []    # Default value at the class level
    enemies = []             # Default value at the class level

    def __init__(self, width, height):
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("8bit Game")
        self.white = (255, 255, 255)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.last_player_shot_time = 0
        self.score = 0  # Initialize score
        self.reset_game()

    def reset_game(self):
        self.player_spaceship = Spaceship(name="Player", x=self.screen.get_width() // 2,
                                          y=self.screen.get_height() - 60, width=50, height=50)
        self.player_projectiles = []
        self.enemy_projectiles = []
        self.enemies = [Enemy(eid=1, x=60, y=60, speed=-2, shoot_rate=2000)]

    def handle_input(self):
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

    def check_player_collision(self):
        player_spaceship_hit = any(
            [self.player_spaceship.is_hit_by_enemy(projectile) for projectile in self.enemy_projectiles]
        )
        if player_spaceship_hit:
            print("Player spaceship hit!")
            self.player_spaceship.reset_hit_status()  # Reset hit status for the next frame
            self.player_spaceship.decrement_lives()  # Decrement lives when hit

    def draw_objects(self):
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
            lives_text = self.font.render(f"Lives: {self.player_spaceship.lives}", True, (0, 0, 0))
            self.screen.blit(lives_text, (10, 10))  # Adjust the position as needed

            # Draw score
            score_text = self.font.render(f"Score: {self.score}", True, (0, 0, 0))
            self.screen.blit(score_text, (120, 10))  # Adjust the position as needed
        else:
            # Player has no lives left, display "Game Over" message
            game_over_text = self.font.render("Game Over", True, (255, 0, 0))  # Use red color
            text_rect = game_over_text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))
            self.screen.blit(game_over_text, text_rect)

            # Prompt to restart the game
            restart_text = self.font.render("Press R to restart", True, (0, 0, 0))
            restart_rect = restart_text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 + 50))
            self.screen.blit(restart_text, restart_rect)

            keys = pygame.key.get_pressed()
            if keys[pygame.K_r]:
                self.reset_game()  # Restart the game if the player presses 'R'

        pygame.display.flip()
        self.clock.tick(60)

def main():
    game_manager = GameManager(width=800, height=600)

    while True:
        game_manager.handle_input()
        game_manager.update_game_state()
        game_manager.draw_objects()

if __name__ == "__main__":
    main()
