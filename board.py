from line import Line
from car_state import CarState
from utils import line_width


class Board:

    @staticmethod
    def _format_border_lines(lines):
        points = list(map(lambda line: [int(x) for x in line.split(" ")], lines))
        border_lines = []
        for i in range(1, len(points)):
            border_lines.append(Line(points[i - 1], points[i]))
        return border_lines

    @staticmethod
    def from_file(file_path):
        with open(file_path, 'r') as file_stream:
            lines = file_stream.readlines()
            left_borders = Board._format_border_lines(lines[slice(lines.index('\n'))])
            lines = lines[slice(lines.index('\n') + 1, None)]
            right_borders = Board._format_border_lines(lines[slice(lines.index('\n'))])
            lines = lines[slice(lines.index('\n') + 1, None)]
            car_state_args = list(map(lambda x: int(x), lines[0].split(" ")))
            init_car_state = CarState((car_state_args[0], car_state_args[1]), car_state_args[2])
            end_points = tuple(map(lambda x: int(x), lines[1].split(" ")))
            end_position = Line((end_points[0], end_points[1]), (end_points[2], end_points[3]))
            return Board(left_borders, right_borders, init_car_state, end_position)

    def __init__(self, left_borders, right_borders, init_car_state, end_position):
        self.left_borders = left_borders
        self.left_border_distances = list(map(line_width, left_borders))
        self.right_borders = right_borders
        self.init_car_state = init_car_state
        self.end_position = end_position
