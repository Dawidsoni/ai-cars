import numpy as np

from car_state import CarState
from game_lost_state import GameLostState
from game_move_type import GameMoveType
from game_won_state import GameWonState
from line import Line
from utils import rotate_vector, lines_intersect, point_from_line_square_distance, point_to_line_projection, line_width


class GameInProgressState:
    MOVE_STEP_SIZE = 2.5
    ANGLE_STEP_SIZE = 3

    def __init__(self, board, prev_car_state=None, car_state=None):
        self.board = board
        self.prev_car_state = prev_car_state if prev_car_state is not None else self.board.init_car_state
        self.car_state = car_state if car_state is not None else self.board.init_car_state
        self.board_progress = self._get_board_progress()

    def _get_board_progress(self):
        distances = [point_from_line_square_distance(self.car_state.position, x) for x in self.board.left_borders]
        current_line_index = np.argmin(distances)
        current_line = self.board.left_borders[current_line_index]
        previous_lines_distances = self.board.left_border_distances[slice(current_line_index)]
        current_line_distance = np.linalg.norm((point_to_line_projection(self.car_state.position, current_line)))
        return int(sum(previous_lines_distances) + current_line_distance)

    def _win_line_crossed(self):
        position_line = Line(self.prev_car_state.position, self.car_state.position)
        return lines_intersect(self.board.end_position, position_line)

    def _border_line_crossed(self):
        position_line = Line(self.prev_car_state.position, self.car_state.position)
        borders = self.board.left_borders + self.board.right_borders
        return any([lines_intersect(border, position_line) for border in borders])

    def _with_move_center(self):
        move_vector = self.MOVE_STEP_SIZE * rotate_vector([1, 0], self.car_state.angle)
        updated_car_state = CarState(self.car_state.position + move_vector, self.car_state.angle)
        return GameInProgressState(self.board, self.car_state, updated_car_state)

    def _with_move_left(self):
        angle = self.car_state.angle - self.ANGLE_STEP_SIZE
        if angle < 0:
            angle += 360
        move_vector = self.MOVE_STEP_SIZE * rotate_vector([1, 0], angle)
        updated_car_state = CarState(self.car_state.position + move_vector, angle)
        return GameInProgressState(self.board, self.car_state, updated_car_state)

    def _with_move_right(self):
        angle = self.car_state.angle + self.ANGLE_STEP_SIZE
        if angle >= 360:
            angle -= 360
        move_vector = self.MOVE_STEP_SIZE * rotate_vector([1, 0], angle)
        updated_car_state = CarState(self.car_state.position + move_vector, angle)
        return GameInProgressState(self.board, self.car_state, updated_car_state)

    def with_move(self, game_move_type):
        if self._win_line_crossed():
            return GameWonState(self.board, self.car_state, self.board_progress)
        elif self._border_line_crossed():
            return GameLostState(self.board, self.car_state, self.board_progress)
        elif game_move_type == GameMoveType.CENTER:
            return self._with_move_center()
        elif game_move_type == GameMoveType.LEFT:
            return self._with_move_left()
        elif game_move_type == GameMoveType.RIGHT:
            return self._with_move_right()
