import pygame
import time

from game_move_type import GameMoveType
from player_type import PlayerType


class GameRefresher:
    FRAME_LENGTH_SECONDS = 0.03

    def __init__(self, player_type):
        self.player_type = player_type
        self.last_frame_time = time.time()

    @staticmethod
    def _get_human_updated_game_state(game_state):
        is_left_pressed = pygame.key.get_pressed()[pygame.K_LEFT]
        is_right_pressed = pygame.key.get_pressed()[pygame.K_RIGHT]
        if is_left_pressed and not is_right_pressed:
            return game_state.with_move(GameMoveType.LEFT)
        elif not is_left_pressed and is_right_pressed:
            return game_state.with_move(GameMoveType.RIGHT)
        return game_state.with_move(GameMoveType.CENTER)

    def _get_updated_game_state(self, game_state):
        if self.player_type == PlayerType.HUMAN:
            return self._get_human_updated_game_state(game_state)
        else:
            raise Exception("Invalid playerType")

    def refresh_game_state(self, game_state):
        if time.time() - self.last_frame_time > self.FRAME_LENGTH_SECONDS:
            self.last_frame_time += self.FRAME_LENGTH_SECONDS
            return self._get_updated_game_state(game_state)
        return game_state
