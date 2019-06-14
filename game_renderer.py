import pygame

from game_lost_state import GameLostState
from game_marker import GameMarker
from game_won_state import GameWonState
from utils import rotate_vector


class GameRenderer:

    def __init__(self, screen):
        self.screen = screen
        self.text_font = pygame.font.SysFont("comicsansms", 10)
        self.end_game_font = pygame.font.SysFont("comicsansms", 60)

    def _render_game_won(self):
        text = self.end_game_font.render("Game won!", True, (0, 255, 0))
        self.screen.blit(text, (140, 220))

    def _render_game_lost(self):
        text = self.end_game_font.render("Game over!", True, (255, 0, 0))
        self.screen.blit(text, (140, 220))

    def _render_lines(self, lines, color):
        for line in lines:
            pygame.draw.line(self.screen, color, line.start_position, line.end_position, 2)

    def _render_player(self, car_state):
        p1 = car_state.position + rotate_vector((20, 0), car_state.angle)
        p2 = car_state.position + rotate_vector((-10, -10), car_state.angle)
        p3 = car_state.position + rotate_vector((-10, 10), car_state.angle)
        triangle_points = [p1, p2, p3]
        pygame.draw.polygon(self.screen, (0, 0, 255), triangle_points, 0)

    def _render_board_progress(self, board_progress):
        text = self.text_font.render("Board progress: {}".format(board_progress), True, (135, 31, 120))
        self.screen.blit(text, (5, 5))

    def _generate_marker_lines(self, marker_lines):
        if not pygame.key.get_pressed()[pygame.K_m]:
            return
        self._render_lines(marker_lines, (255, 165, 0))

    def render_game(self, game_state, marker_manager):
        self.screen.fill((255, 255, 255))
        self._render_board_progress(game_state.board_progress)
        if type(game_state) == GameWonState:
            self._render_game_won()
        elif type(game_state) == GameLostState:
            self._render_game_lost()
        else:
            self._render_lines(game_state.board.left_borders + game_state.board.right_borders, (255, 0, 0))
            self._render_lines([game_state.board.end_position], (0, 255, 0))
            self._render_player(game_state.car_state)
            self._generate_marker_lines(marker_manager.generate_marker_lines(game_state).values())

