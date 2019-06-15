import pygame

from game_move_type import GameMoveType


class HumanPlayer:
    def __init__(self, left_key=pygame.K_LEFT, right_key=pygame.K_RIGHT):
        self.left_key = left_key
        self.right_key = right_key

    def get_move(self, _game_state):
        is_left_pressed = pygame.key.get_pressed()[self.left_key]
        is_right_pressed = pygame.key.get_pressed()[self.right_key]
        if is_left_pressed and not is_right_pressed:
            return GameMoveType.LEFT
        elif not is_left_pressed and is_right_pressed:
            return GameMoveType.RIGHT
        return GameMoveType.CENTER
