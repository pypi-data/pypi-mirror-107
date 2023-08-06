
class GraphOptimal1Cycle(object):
    """The class represents an optimal (not volume-optimal) 1-cycle computed from graph information.

    Examples:
        >>> import numpy as np
        >>> import homcloud.interface as hc
        >>> distance_matrix = np.a
    """

    def __init__(self, pair, path_vertices):
        self.pair = pair
        self.path_vertices = path_vertices

    def birth_time(self):
        return self.pair.birth_time()

    def death_time(self):
        return self.pair.death_time()

    def boundary_points(self):
        return self.path_vertices

    def boundary_points_symbols(self):
        return self.geometry_resolver(False).resolve_graph_path(self.path_vertices)

    def geometry_resolver(self, use_symbol):
        return self.pair.diagram.pd.geometry_resolver(use_symbol)
