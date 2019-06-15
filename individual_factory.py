from individual import Individual


class IndividualFactory:

    def __init__(self, clustering_algorithm, angles, marker_manager):
        self.clustering_algorithm = clustering_algorithm
        self.angles = angles
        self.marker_manager = marker_manager

    def create_individual(self, genotype):
        return Individual(self.clustering_algorithm, self.angles, self.marker_manager, genotype)
