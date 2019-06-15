import pickle

import numpy as np

from board import Board
from game_in_progress_state import GameInProgressState
from game_move_type import GameMoveType
from individual_factory import IndividualFactory
from marker_manager import MarkerManager


class GenotypeEvaluator:

    def __init__(self, cluster_file, board_files, evaluate_move_type=False):
        with open(cluster_file, 'rb') as file_stream:
            angles = pickle.load(file_stream)
            clustering_algorithm = pickle.load(file_stream)
        self.individual_factory = IndividualFactory(clustering_algorithm, angles, MarkerManager(angles))
        self.init_game_states = [GameInProgressState(Board.from_file(x)) for x in board_files]
        self.evaluate_move_type = evaluate_move_type
        self.cached_genotypes = {}

    @staticmethod
    def _get_genotype_move_score(genotype):
        return len(list(filter(lambda x: GameMoveType(x) == GameMoveType.CENTER, genotype)))

    def _generate_genotype_score(self, genotype):
        individual = self.individual_factory.create_individual(genotype)
        score = 0.0
        for init_game_state in self.init_game_states:
            game_state = init_game_state
            while type(game_state) == GameInProgressState:
                move_type = individual.get_move(game_state)
                game_state = game_state.with_move(move_type)
            score += game_state.board_progress
        return score

    def _get_genotype_score(self, genotype):
        if tuple(genotype) not in self.cached_genotypes:
            self.cached_genotypes[tuple(genotype)] = self._generate_genotype_score(genotype)
        return self.cached_genotypes[tuple(genotype)]

    def evaluate_genotypes(self, genotypes):
        genotype_scores = np.array(list(map(self._get_genotype_score, genotypes)))
        if not self.evaluate_move_type:
            return genotype_scores
        genotype_move_scores = np.array(list(map(self._get_genotype_move_score, genotypes)))
        return genotype_scores, genotype_move_scores
