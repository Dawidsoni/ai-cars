import pickle

from game_marker import GameMarker
from utils import line_width


class MarkerManager:
    def __init__(self, angles, save_path=None):
        self.markers = {angle: GameMarker(angle) for angle in angles}
        self.game_state_marker_lines = {}
        self.save_path = save_path

    def _save_marker_lines(self, marker_lines):
        marker_widths = {x: line_width(marker_lines[x]) for x in marker_lines.keys()}
        with open(self.save_path, 'a+b') as file_stream:
            pickle.dump(marker_widths, file_stream)

    def generate_marker_lines(self, game_state):
        if game_state in self.game_state_marker_lines:
            return self.game_state_marker_lines[game_state]
        marker_lines = {x: self.markers[x].generate_marker_line(game_state) for x in self.markers.keys()}
        if self.save_path is not None:
            self._save_marker_lines(marker_lines)
        self.game_state_marker_lines[game_state] = marker_lines
        return marker_lines
