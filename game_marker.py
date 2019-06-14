import numpy as np

from line import Line
from utils import rotate_vector, lines_intersection_point, line_width, \
    lines_equal_direction, lines_parallel, straight_line_with_line_intersect


class GameMarker:
    def __init__(self, angle):
        self.angle = angle

    def _generate_marker_angle(self, car_angle):
        marker_angle = car_angle + self.angle
        if marker_angle >= 360:
            marker_angle -= 360
        return marker_angle

    def generate_marker_line(self, game_state):
        borders = game_state.board.left_borders + game_state.board.right_borders
        dir_vector = rotate_vector([1, 0], self._generate_marker_angle(game_state.car_state.angle))
        dir_line = Line(game_state.car_state.position, game_state.car_state.position + dir_vector)
        dependent_borders = filter(lambda x: not lines_parallel(dir_line, x), borders)
        intersected_borders = list(filter(lambda x: straight_line_with_line_intersect(dir_line, x), dependent_borders))
        intersection_points = [lines_intersection_point(dir_line, border) for border in intersected_borders]
        marker_lines = [Line(game_state.car_state.position, point) for point in intersection_points]
        dir_marker_lines = list(filter(lambda x: lines_equal_direction(dir_line, x), marker_lines))
        if len(dir_marker_lines) == 0:
            return Line((0, 0), (0, 0))
        return dir_marker_lines[np.argmin([line_width(line) for line in dir_marker_lines])]
