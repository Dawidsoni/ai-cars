import pygame
import sys

from board import Board
from game_refresher import GameRefresher
from game_renderer import GameRenderer
from game_in_progress_state import GameInProgressState
from marker_manager import MarkerManager
from player_type import PlayerType


def get_program_arguments():
    args = list(sys.argv)
    if len(args) < 3:
        raise Exception("Too few program arguments")
    markers_save_path = args[3] if len(args) >= 4 else None
    return args[1], PlayerType(int(args[2])), markers_save_path


def start_game(board_path, player_type, markers_save_path):
    game_state = GameInProgressState(Board.from_file(board_path))
    marker_manager = MarkerManager([0, 20, 340, 90, 270], markers_save_path)
    pygame.init()
    pygame.display.set_caption('AI cars')
    screen = pygame.display.set_mode((600, 600))
    game_renderer = GameRenderer(screen)
    game_refresher = GameRefresher(player_type)
    while True:
        events = list(pygame.event.get())
        if any([event.type == pygame.QUIT for event in events]):
            pygame.quit()
            sys.exit()
        game_state = game_refresher.refresh_game_state(game_state)
        game_renderer.render_game(game_state, marker_manager)
        pygame.display.update()


if __name__ == '__main__':
    start_game(*get_program_arguments())