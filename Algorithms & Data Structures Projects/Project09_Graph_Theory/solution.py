"""
CSE 331 SS22 (Onsay)
Graph Project Part 1
"""

import math
import queue
import time
import csv
from typing import TypeVar, Tuple, List, Set, Dict, Any

import numpy as np

T = TypeVar('T')
Matrix = TypeVar('Matrix')  # Adjacency Matrix
Vertex = TypeVar('Vertex')  # Vertex Class Instance
Graph = TypeVar('Graph')  # Graph Class Instance


class Vertex:
    """
    Class representing a Vertex object within a Graph.
    """

    __slots__ = ['id', 'adj', 'visited', 'x', 'y']

    def __init__(self, id_init: str, x: float = 0, y: float = 0) -> None:
        """
        DO NOT MODIFY
        Initializes a Vertex.
        :param id_init: [str] A unique string identifier used for hashing the vertex.
        :param x: [float] The x coordinate of this vertex (used in a_star).
        :param y: [float] The y coordinate of this vertex (used in a_star).
        :return: None.
        """
        self.id = id_init
        self.adj = {}  # dictionary {id : weight} of outgoing edges
        self.visited = False  # boolean flag used in search algorithms
        self.x, self.y = x, y  # coordinates for use in metric computations

    def __eq__(self, other: Vertex) -> bool:
        """
        DO NOT MODIFY.
        Equality operator for Graph Vertex class.
        :param other: [Vertex] vertex to compare.
        :return: [bool] True if vertices are equal, else False.
        """
        if self.id != other.id:
            return False
        if self.visited != other.visited:
            print(f"Vertex '{self.id}' not equal")
            print(f"Vertex visited flags not equal: self.visited={self.visited},"
                  f" other.visited={other.visited}")
            return False
        if self.x != other.x:
            print(f"Vertex '{self.id}' not equal")
            print(f"Vertex x coords not equal: self.x={self.x}, other.x={other.x}")
            return False
        if self.y != other.y:
            print(f"Vertex '{self.id}' not equal")
            print(f"Vertex y coords not equal: self.y={self.y}, other.y={other.y}")
            return False
        if set(self.adj.items()) != set(other.adj.items()):
            diff = set(self.adj.items()).symmetric_difference(set(other.adj.items()))
            print(f"Vertex '{self.id}' not equal")
            print(f"Vertex adj dictionaries not equal:"
                  f" symmetric diff of adjacency (k,v) pairs = {str(diff)}")
            return False
        return True

    def __repr__(self) -> str:
        """
        DO NOT MODIFY
        Constructs string representation of Vertex object.
        :return: [str] string representation of Vertex object.
        """
        lst = [f"<id: '{k}', weight: {v}>" for k, v in self.adj.items()]
        return f"<id: '{self.id}'" + ", Adjacencies: " + "".join(lst) + ">"

    __str__ = __repr__

    def __hash__(self) -> int:
        """
        DO NOT MODIFY
        Hashes Vertex into a set. Used in unit tests.
        :return: [int] Hash value of Vertex.
        """
        return hash(self.id)

    # ============== Modify Vertex Methods Below ==============#

    def deg(self) -> int:
        """
        This function returns the number of outgoing edges from vertex
        :return: Integer representing degree of given edge
        """
        return len(self.adj)

    def get_outgoing_edges(self) -> Dict[Any, Any]:
        """
        Returns all the outgoing edges with the values
        :return: set of tuples with the edges
        """
        if self.deg == 0:
            return set()
        edges = []
        for i in self.adj.items():
            edges.append(i)
        return set(edges)

    def euclidean_dist(self, other: Vertex) -> float:
        """
        This function returns the euclidean distance between the given vertex and the
        other vertex
        :param other: This is the other vertex we want the distance too
        :return: Float representing the distance
        """
        return ((other.x - self.x) ** 2 + (other.y - self.y) ** 2) ** (1 / 2)

    def taxicab_dist(self, other: Vertex) -> float:
        """
        This function returns the taxicabdistance between the given vertex and the
        other vertex
        :param other: This is the other vertex we want the distance too
        :return: Float representing the distance
        """
        return abs(self.x - other.x) + abs(self.y - other.y)


class Graph:
    """
    Class implementing the Graph ADT using an Adjacency Map structure.
    """

    __slots__ = ['size', 'vertices', 'plot_show', 'plot_delay']

    def __init__(self, plt_show: bool = False, matrix: Matrix = None, csvf: str = "") -> None:
        """
        DO NOT MODIFY
        Instantiates a Graph class instance.
        :param plt_show: [bool] If true, render plot when plot() is called; else, ignore plot().
        :param matrix: [Matrix] Optional matrix parameter used for fast construction.
        :param csvf: [str] Optional filepath to a csv containing a matrix.
        :return: None.
        """
        matrix = matrix if matrix else np.loadtxt(csvf, delimiter=',', dtype=str).tolist() \
            if csvf else None
        self.size = 0
        self.vertices = {}

        self.plot_show = plt_show
        self.plot_delay = 0.2

        if matrix is not None:
            for i in range(1, len(matrix)):
                for j in range(1, len(matrix)):
                    if matrix[i][j] == "None" or matrix[i][j] == "":
                        matrix[i][j] = None
                    else:
                        matrix[i][j] = float(matrix[i][j])
            self.matrix2graph(matrix)

    def __eq__(self, other: Graph) -> bool:
        """
        DO NOT MODIFY
        Overloads equality operator for Graph class.
        :param other: [Graph] Another graph to compare.
        :return: [bool] True if graphs are equal, else False.
        """
        if self.size != other.size or len(self.vertices) != len(other.vertices):
            print(f"Graph size not equal: self.size={self.size}, other.size={other.size}")
            return False
        for vertex_id, vertex in self.vertices.items():
            other_vertex = other.get_vertex_by_id(vertex_id)
            if other_vertex is None:
                print(f"Vertices not equal: '{vertex_id}' not in other graph")
                return False

            adj_set = set(vertex.adj.items())
            other_adj_set = set(other_vertex.adj.items())

            if not adj_set == other_adj_set:
                print(f"Vertices not equal: adjacencies of '{vertex_id}' not equal")
                print(f"Adjacency symmetric difference = "
                      f"{str(adj_set.symmetric_difference(other_adj_set))}")
                return False
        return True

    def __repr__(self) -> str:
        """
        DO NOT MODIFY
        Constructs string representation of graph.
        :return: [str] String representation of graph.
        """
        return "Size: " + str(self.size) + ", Vertices: " + str(list(self.vertices.items()))

    __str__ = __repr__

    def plot(self) -> None:
        """
        DO NOT MODIFY
        Creates a plot a visual representation of the graph using matplotlib.
        :return: None.
        """
        if self.plot_show:
            import matplotlib.cm as cm
            import matplotlib.patches as patches
            import matplotlib.pyplot as plt

            # if no x, y coords are specified, place vertices on the unit circle
            for i, vertex in enumerate(self.get_all_vertices()):
                if vertex.x == 0 and vertex.y == 0:
                    vertex.x = math.cos(i * 2 * math.pi / self.size)
                    vertex.y = math.sin(i * 2 * math.pi / self.size)

            # show edges
            num_edges = len(self.get_all_edges())
            max_weight = max([edge[2] for edge in self.get_all_edges()]) if num_edges > 0 else 0
            colormap = cm.get_cmap('cool')
            for i, edge in enumerate(self.get_all_edges()):
                origin = self.get_vertex_by_id(edge[0])
                destination = self.get_vertex_by_id(edge[1])
                weight = edge[2]

                # plot edge
                arrow = patches.FancyArrowPatch((origin.x, origin.y),
                                                (destination.x, destination.y),
                                                connectionstyle="arc3,rad=.2",
                                                color=colormap(weight / max_weight),
                                                zorder=0,
                                                **dict(arrowstyle="Simple,tail_width=0.5,"
                                                                  "head_width=8,head_length=8"))
                plt.gca().add_patch(arrow)

                # label edge
                plt.text(x=(origin.x + destination.x) / 2 - (origin.x - destination.x) / 10,
                         y=(origin.y + destination.y) / 2 - (origin.y - destination.y) / 10,
                         s=weight, color=colormap(weight / max_weight))

            # show vertices
            x = np.array([vertex.x for vertex in self.get_all_vertices()])
            y = np.array([vertex.y for vertex in self.get_all_vertices()])
            labels = np.array([vertex.id for vertex in self.get_all_vertices()])
            colors = np.array(
                ['yellow' if vertex.visited else 'black' for vertex in self.get_all_vertices()])
            plt.scatter(x, y, s=40, c=colors, zorder=1)

            # plot labels
            for j, _ in enumerate(x):
                plt.text(x[j] - 0.03 * max(x), y[j] - 0.03 * max(y), labels[j])

            # show plot
            plt.show()
            # delay execution to enable animation
            time.sleep(self.plot_delay)

    def add_to_graph(self, begin_id: str, end_id: str = None, weight: float = 1) -> None:
        """
        Adds to graph: creates start vertex if necessary,
        an edge if specified,
        and a destination vertex if necessary to create said edge
        If edge already exists, update the weight.
        :param begin_id: [str] unique string id of starting vertex
        :param end_id: [str] unique string id of ending vertex
        :param weight: [float] weight associated with edge from start -> dest
        :return: None
        """
        if self.vertices.get(begin_id) is None:
            self.vertices[begin_id] = Vertex(begin_id)
            self.size += 1
        if end_id is not None:
            if self.vertices.get(end_id) is None:
                self.vertices[end_id] = Vertex(end_id)
                self.size += 1
            self.vertices.get(begin_id).adj[end_id] = weight

    def matrix2graph(self, matrix: Matrix) -> None:
        """
        Given an adjacency matrix, construct a graph
        matrix[i][j] will be the weight of an edge between the vertex_ids
        stored at matrix[i][0] and matrix[0][j]
        Add all vertices referenced in the adjacency matrix, but only add an
        edge if matrix[i][j] is not None
        Guaranteed that matrix will be square
        If matrix is nonempty, matrix[0][0] will be None
        :param matrix: [Matrix] an n x n square matrix (list of lists) representing Graph
        :return: None
        """
        for i in range(1, len(matrix)):  # add all vertices to begin with
            self.add_to_graph(matrix[i][0])
        for i in range(1, len(matrix)):  # go back through and add all edges
            for j in range(1, len(matrix)):
                if matrix[i][j] is not None:
                    self.add_to_graph(matrix[i][0], matrix[j][0], matrix[i][j])

    def graph2matrix(self) -> Matrix:
        """
        Given a graph, creates an adjacency matrix of the type described in construct_from_matrix.
        :return: [Matrix] representing graph.
        """
        matrix = [[None] + list(self.vertices)]
        for v_id, outgoing in self.vertices.items():
            matrix.append([v_id] + [outgoing.adj.get(v) for v in self.vertices])
        return matrix if self.size else None

    def graph2csv(self, filepath: str) -> None:
        """
        Given a (non-empty) graph, creates a csv file containing data necessary to reconstruct.
        :param filepath: [str] location to save CSV.
        :return: None.
        """
        if self.size == 0:
            return

        with open(filepath, 'w+') as graph_csv:
            csv.writer(graph_csv, delimiter=',').writerows(self.graph2matrix())

    # ============== Modify Graph Methods Below ==============#

    def unvisit_vertices(self) -> None:
        """
        Resets all the visited flags to None
        :return: None
        """
        for i in self.vertices:
            self.vertices[i].visited = False

    def get_vertex_by_id(self, v_id: str) -> Vertex:
        """
        Returns the vertex if the id is in the graph otherwise returns None
        :param v_id: The id that is being searched for
        :Return: Returns Vertex if found, Otherwise None
        """
        if v_id in self.vertices:
            return self.vertices[v_id]
        else:
            return None

    def get_all_vertices(self) -> Set[Vertex]:
        """
        Returns a set of all Vertex Objects in the graph
        """

        vertex = []
        for i in self.vertices.items():
            vertex.append(i[1])
        return set(vertex)

    def get_edge_by_ids(self, begin_id: str, end_id: str) -> Tuple[str, str, float]:
        """
        This function will return the edge connecting the vertex from begin_id to end_id
        :param begin_id: This represents the first edge
        :param end_id: This represents the second edge
        :return: None if either edge is not in the graph. If both exist returns connecting edge
        """
        try:
            return begin_id, end_id, self.vertices[begin_id].adj[end_id]
        except KeyError:
            return None

    def get_all_edges(self) -> Set[Tuple[str, str, float]]:
        """
        This function returns set of tuples representing all the edges within graph
        :return: Set of tuples
        """
        l1 = []
        for i in self.vertices:
            for j in self.vertices[i].adj:
                l1.append((i, j, self.vertices[i].adj[j]))

        return set(l1)

    def build_path(self, back_edges: Dict[str, str], begin_id: str, end_id: str)-> Tuple[List[str], float]:
        """
        Takes a dictionary of back-edges and remakes the path from the starting id to the ending id
        :param back_edges: Dictionary of back edges
        :param begin_id: Starting Vertex id
        :param end_id: Ending Vertex id
        :Return: Tuple that contains a list mapping out the path, and a float for distance
        """

        path = []
        distance = 0
        curr = self.get_vertex_by_id(end_id)

        while True:
            path = [curr.id] + path
            if curr.id == begin_id:
                break
            try:
                distance += self.vertices[back_edges[curr.id]].adj[end_id]
            except KeyError:
                return [], 0
            end_id = back_edges[curr.id]
            curr = self.get_vertex_by_id(end_id)

        return path, distance

    def bfs(self, begin_id: str, end_id: str) -> Tuple[List[str], float]:
        """
        Breadth First search algorithm searches based off of distance
        :param begin_id: The node to start traversal at
        :param end_id:
        :return: Tuple of list and float. The list representing the nodes visited
        and float distance.
        """
        # Starting Case
        if self.get_edge_by_ids(begin_id, end_id) is None:
            if len(self.vertices) >= 2:
                pass
            else:
                return [], 0

        level = [begin_id]
        discovered = []
        distance = 0
        back_edges = {}
        while len(level) > 0:
            curr = level.pop(0)
            discovered.append(curr)

            for i in self.vertices[curr].adj:  # checking adjacent
                if not self.vertices[i].visited:
                    back_edges[i] = curr
                    level.append(i)
                    discovered.append(i)
                    self.vertices[i].visited = True

        return self.build_path(back_edges, begin_id, end_id)

    def dfs(self, begin_id: str, end_id: str) -> Tuple[List[str], float]:
        """
        Depth First Search Algorithm searches by depth
        :param begin_id: This parameter represents starting vertex
        :param end_id:  This parameter represents ending vertex
        :return: Returns list of visited notes and weight
        """
        if self.get_edge_by_ids(begin_id, end_id) is None:
            if len(self.vertices) > 2:
                pass
            else:
                return [], 0

        def dfs_inner(current_id: str, end_id: str, path: List[str] = []) -> Tuple[List[str], float]:
            """
            Inner recursive function. Returns list and float
            :param current_id: of the vertex
            :param end_id:
            :param path: list representing of all vertices in between the two
            :return: Tuple of a list and float
            """
            distance_ = 0
            if current_id not in path:
                if len(path) > 0 and path[len(path)-1] == end_id:
                    return path, distance_
                path.append(current_id)
                self.vertices[current_id].visited = True
                for i in self.vertices[current_id].adj:
                    if end_id in self.vertices[current_id].adj:
                        path.append(end_id)
                        self.vertices[end_id].visited = True
                        return path, self.vertices[current_id].adj[end_id]
                    elif not self.vertices[i].visited:
                        if len(self.vertices[i].adj) == 0 and i != end_id:
                            self.vertices[i].visited = True
                            continue

                        self.vertices[i].visited = True
                        temp, distance_ = dfs_inner(i, end_id, path)
                        if temp is None and distance_ == 0:
                            path = []
                            distance_ = 0
                            return path, distance_
                        distance_ += self.vertices[current_id].adj[i]
                        if path[len(path) - 1] == end_id:
                            break
                        else:
                            break


            return path, distance_

        path, distance = dfs_inner(begin_id, end_id)
        if end_id in path:
            return path, distance
        else:
            return [], 0

    def topological_sort(self) -> List[str]:
        """
        This function will sort the graph topologically
        :return: list of the vertices visited
        """
        if len(self.vertices) == 0:
            return [], 0
        result = []

        def topological_sort_inner(current_id: str) -> None:
            """
            This function sorts the current vertex
            """
            for j in self.vertices[current_id].adj:
                if not self.vertices[i].visited:
                    topological_sort_inner(i)

        for i in self.vertices:
            if not self.vertices[i].visited:
                topological_sort_inner(i)

    def boss_order_validity(self) -> bool:
        """
        Determine if the game is beatable by the graph order
        """
        pass
