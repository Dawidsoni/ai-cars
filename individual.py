from game_move_type import GameMoveType
from utils import line_width


class Individual:

    def __init__(self, clustering_algorithm, angles, marker_manager, genotype):
        self.clustering_algorithm = clustering_algorithm
        self.angles = angles
        self.marker_manager = marker_manager
        self.genotype = genotype

    def get_move(self, game_state):
        marker_lines = self.marker_manager.generate_marker_lines(game_state)
        marker_widths = {x: line_width(marker_lines[x]) for x in marker_lines.keys()}
        feature_input = list(map(lambda x: marker_widths[x], self.angles))
        predicted_cluster = self.clustering_algorithm.predict([feature_input])[0]
        return GameMoveType(self.genotype[predicted_cluster])
