import pygame
from game_manager import GameManager


def main():
    pygame.init()

    width, height = 800, 600
    game_manager = GameManager(width, height)

    while True:
        game_manager.handle_input()
        game_manager.update_game_state()
        game_manager.draw_objects()


if __name__ == "__main__":
    main()
