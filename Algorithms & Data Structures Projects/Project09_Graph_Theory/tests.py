import unittest, string, math, random
from xml.dom import minidom

from solution import Graph, Vertex


class GraphTests(unittest.TestCase):
    """
    Begin Vertex Tests
    """

    def test_deg(self):

        # (1) test a-->b and a-->c
        vertex = Vertex('a')
        vertex.adj['b'] = 1
        self.assertEqual(vertex.deg(), 1)
        vertex.adj['c'] = 3
        assert vertex.deg() == 2

        # (2) test a-->letter for all letters in alphabet
        vertex = Vertex('a')
        for i, char in enumerate(string.ascii_lowercase):
            self.assertEqual(vertex.deg(), i)
            vertex.adj[char] = i

    def test_get_outgoing_edges(self):

        # (1) test a-->b and a-->c
        vertex = Vertex('a')
        solution = {('b', 1), ('c', 2)}
        vertex.adj['b'] = 1
        vertex.adj['c'] = 2
        subject = vertex.get_outgoing_edges()
        self.assertEqual(subject, solution)

        # (2) test empty case
        vertex = Vertex('a')
        solution = set()
        subject = vertex.get_outgoing_edges()
        self.assertEqual(subject, solution)

        # (3) test a-->letter for all letters in alphabet
        for i, char in enumerate(string.ascii_lowercase):
            vertex.adj[char] = i
            solution.add((char, i))
        subject = vertex.get_outgoing_edges()
        self.assertEqual(subject, solution)

    def test_distances(self):

        # (1) test pythagorean triple
        vertex_a = Vertex('a')
        vertex_b = Vertex('b', 3, 4)

        subject = vertex_a.euclidean_dist(vertex_b)
        self.assertEqual(subject, 5)
        subject = vertex_b.euclidean_dist(vertex_a)
        self.assertEqual(subject, 5)
        subject = vertex_a.taxicab_dist(vertex_b)
        self.assertEqual(subject, 7)
        subject = vertex_b.taxicab_dist(vertex_a)
        self.assertEqual(subject, 7)

        # (2) test linear difference
        vertex_a = Vertex('a')
        vertex_b = Vertex('b', 0, 10)

        subject = vertex_a.euclidean_dist(vertex_b)
        self.assertEqual(subject, 10)
        subject = vertex_b.euclidean_dist(vertex_a)
        self.assertEqual(subject, 10)
        subject = vertex_a.taxicab_dist(vertex_b)
        self.assertEqual(subject, 10)
        subject = vertex_b.taxicab_dist(vertex_a)
        self.assertEqual(subject, 10)

        # (3) test zero distance
        vertex_a = Vertex('a')
        vertex_b = Vertex('b')

        subject = vertex_a.euclidean_dist(vertex_b)
        self.assertEqual(subject, 0)
        subject = vertex_b.euclidean_dist(vertex_a)
        self.assertEqual(subject, 0)
        subject = vertex_a.taxicab_dist(vertex_b)
        self.assertEqual(subject, 0)
        subject = vertex_b.taxicab_dist(vertex_a)
        self.assertEqual(subject, 0)

        # (4) test floating point distance
        vertex_a = Vertex('a')
        vertex_b = Vertex('b', 5, 5)

        subject = vertex_a.euclidean_dist(vertex_b)
        self.assertAlmostEqual(subject, 5 * math.sqrt(2))
        subject = vertex_b.euclidean_dist(vertex_a)
        self.assertAlmostEqual(subject, 5 * math.sqrt(2))
        subject = vertex_a.taxicab_dist(vertex_b)
        self.assertEqual(subject, 10)
        subject = vertex_b.taxicab_dist(vertex_a)
        self.assertEqual(subject, 10)

        # (5) test taxicab absolute values in right spot
        vertex_a = Vertex('a', 3, 1)
        vertex_b = Vertex('b', 2, 5)
        subject = vertex_a.euclidean_dist(vertex_b)
        self.assertAlmostEqual(subject, math.sqrt(17))
        subject = vertex_b.euclidean_dist(vertex_a)
        self.assertAlmostEqual(subject, math.sqrt(17))
        subject = vertex_a.taxicab_dist(vertex_b)
        self.assertEqual(subject, 5)
        subject = vertex_b.taxicab_dist(vertex_a)
        self.assertEqual(subject, 5)

    """
    End Vertex Tests
    """

    """
    Begin Graph Tests
    """

    def test_unvisit_vertices(self):

        graph = Graph()

        # (1) visit all vertices then reset
        graph.vertices['a'] = Vertex('a')
        graph.vertices['b'] = Vertex('b')

        for vertex in graph.vertices.values():
            vertex.visited = True
        graph.unvisit_vertices()
        for vertex in graph.vertices.values():
            self.assertFalse(vertex.visited)

    def test_get_vertex_by_id(self):

        graph = Graph()

        # (1) test basic vertex object
        vertex_a = Vertex('a')
        graph.vertices['a'] = vertex_a
        subject = graph.get_vertex_by_id('a')
        self.assertEqual(subject, vertex_a)

        # (2) test empty case
        subject = graph.get_vertex_by_id('b')
        self.assertIsNone(subject)

        # (3) test case with adjacencies
        vertex_b = Vertex('b')
        for i, char in enumerate(string.ascii_lowercase):
            vertex_b.adj[char] = i
        graph.vertices['b'] = vertex_b
        subject = graph.get_vertex_by_id('b')
        self.assertEqual(subject, vertex_b)

    def test_get_all_vertices(self):

        graph = Graph()
        solution = set()

        # (1) test empty graph
        subject = graph.get_all_vertices()
        self.assertEqual(subject, solution)

        # (2) test single vertex
        vertex = Vertex('$')
        graph.vertices['$'] = vertex
        solution.add(vertex)
        subject = graph.get_all_vertices()
        self.assertEqual(subject, solution)

        # (3) test multiple vertices
        graph = Graph()
        solution = set()
        for i, char in enumerate(string.ascii_lowercase):
            vertex = Vertex(char)
            graph.vertices[char] = vertex
            solution.add(vertex)
        subject = graph.get_all_vertices()
        self.assertEqual(subject, solution)

    def test_get_edge_by_ids(self):

        graph = Graph()

        # (1) neither end vertex exists
        subject = graph.get_edge_by_ids('a', 'b')
        self.assertIsNone(subject)

        # (2) one end vertex exists
        graph.vertices['a'] = Vertex('a')
        subject = graph.get_edge_by_ids('a', 'b')
        self.assertIsNone(subject)

        # (3) both end vertices exist, but no edge
        graph.vertices['a'] = Vertex('a')
        graph.vertices['b'] = Vertex('b')
        subject = graph.get_edge_by_ids('a', 'b')
        self.assertIsNone(subject)

        # (4) a -> b exists but b -> a does not
        graph.vertices.get('a').adj['b'] = 331
        subject = graph.get_edge_by_ids('a', 'b')
        self.assertEqual(subject, ('a', 'b', 331))
        subject = graph.get_edge_by_ids('b', 'a')
        self.assertIsNone(subject)

        # (5) connect all vertices to center vertex and return all edges
        graph.vertices['$'] = Vertex('$')
        for i, char in enumerate(string.ascii_lowercase):
            graph.vertices[char] = Vertex(char)
            graph.vertices.get('$').adj[char] = i
        for i, char in enumerate(string.ascii_lowercase):
            subject = graph.get_edge_by_ids('$', char)
            self.assertEqual(subject, ('$', char, i))

    def test_get_all_edges(self):

        graph = Graph()

        # (1) test empty graph
        subject = graph.get_all_edges()
        self.assertEqual(subject, set())

        # (2) test graph with vertices but no edges
        graph.vertices['a'] = Vertex('a')
        graph.vertices['b'] = Vertex('b')
        subject = graph.get_all_edges()
        self.assertEqual(subject, set())

        # (3) test graph with one edge
        graph.vertices.get('a').adj['b'] = 331
        subject = graph.get_all_edges()
        self.assertEqual(subject, {('a', 'b', 331)})

        # (4) test graph with two edges
        graph = Graph()
        graph.vertices['a'] = Vertex('a')
        graph.vertices['b'] = Vertex('b')
        graph.vertices.get('a').adj['b'] = 331
        graph.vertices.get('b').adj['a'] = 1855
        subject = graph.get_all_edges()
        solution = {('a', 'b', 331), ('b', 'a', 1855)}
        self.assertEqual(subject, solution)

        # (5) test entire alphabet graph
        graph = Graph()
        solution = set()
        for i, char in enumerate(string.ascii_lowercase):
            graph.vertices[char] = Vertex(char)
            for j, jar in enumerate(string.ascii_lowercase):
                if i != j:
                    graph.vertices.get(char).adj[jar] = 26 * i + j
                    solution.add((char, jar, 26 * i + j))

        subject = graph.get_all_edges()
        self.assertEqual(subject, solution)

    def test_build_path(self):

        # (1) test on single edge
        graph = Graph()
        graph.add_to_graph('a', 'b', 331)
        subject = graph.build_path({'b': 'a'}, 'a', 'b')
        self.assertEqual(subject, (['a', 'b'], 331))

        # (2) test on two edges
        graph = Graph()
        graph.add_to_graph('a', 'b', 331)
        graph.add_to_graph('b', 'c', 100)
        subject = graph.build_path({'b': 'a', 'c': 'b'}, 'a', 'c')
        self.assertEqual(subject, (['a', 'b', 'c'], 431))

        # (3) test that the right weights are being selected
        graph = Graph()
        graph.add_to_graph('a', 'b', 331)
        graph.add_to_graph('b', 'c', 100)
        graph.add_to_graph('a', 'c', 999)
        subject = graph.build_path({'c': 'a'}, 'a', 'c')
        self.assertEqual(subject, (['a', 'c'], 999))

        # (4) test on a lot of edges
        graph = Graph(csvf='test_csvs/bfs/7.csv')
        subject = graph.build_path({'midleft': 'bottomleft', 'topleft': 'midleft', 'topright': 'topleft'}, 'bottomleft', 'topright')
        self.assertEqual(subject, (['bottomleft', 'midleft', 'topleft', 'topright'], 3))

    def test_bfs(self):

        graph = Graph()

        # (1) test on empty graph
        subject = graph.bfs('a', 'b')
        self.assertEqual(subject, ([], 0))

        # (2) test on graph missing begin or dest
        graph.add_to_graph('a')
        subject = graph.bfs('a', 'b')
        self.assertEqual(subject, ([], 0))
        subject = graph.bfs('b', 'a')
        self.assertEqual(subject, ([], 0))

        # (3) test on graph with both vertices but no path
        graph.add_to_graph('b')
        subject = graph.bfs('a', 'b')
        self.assertEqual(subject, ([], 0))

        # (4) test on single edge
        graph = Graph()
        graph.add_to_graph('a', 'b', 331)
        subject = graph.bfs('a', 'b')
        self.assertEqual(subject, (['a', 'b'], 331))

        # (5) test on two edges
        graph = Graph()
        graph.add_to_graph('a', 'b', 331)
        graph.add_to_graph('b', 'c', 100)
        subject = graph.bfs('a', 'c')
        self.assertEqual(subject, (['a', 'b', 'c'], 431))

        # (6) test on edge triangle and ensure one-edge path is taken
        # (bfs guarantees fewest-edge path, not least-weighted path)
        graph = Graph()
        graph.add_to_graph('a', 'b', 331)
        graph.add_to_graph('b', 'c', 100)
        graph.add_to_graph('a', 'c', 999)
        subject = graph.bfs('a', 'c')
        self.assertEqual(subject, (['a', 'c'], 999))

        # (7) test on grid figure-8 and ensure fewest-edge path is taken
        graph = Graph(csvf='test_csvs/bfs/7.csv')

        subject = graph.bfs('bottomleft', 'topleft')
        self.assertEqual(subject, (['bottomleft', 'midleft', 'topleft'], 2))

        graph.unvisit_vertices()  # mark all unvisited
        subject = graph.bfs('bottomright', 'topright')
        self.assertEqual(subject, (['bottomright', 'midright', 'topright'], 2))

        graph.unvisit_vertices()  # mark all unvisited
        subject = graph.bfs('bottomleft', 'topright')
        self.assertIn(subject[0], [['bottomleft', 'midleft', 'topleft', 'topright'],
                                   ['bottomleft', 'midleft', 'midright', 'topright'],
                                   ['bottomleft', 'bottomright', 'midright', 'topright']])
        self.assertEqual(subject[1], 3)

        # (8) test on example graph from Onsay's slides, starting from vertex A
        # see bfs_graph.png
        graph = Graph(csvf='test_csvs/bfs/8.csv')

        subject = graph.bfs('a', 'd')
        self.assertEqual(subject, (['a', 'b', 'd'], 4))

        graph.unvisit_vertices()  # mark all unvisited
        subject = graph.bfs('a', 'f')
        self.assertEqual(subject, (['a', 'c', 'f'], 4))

        graph.unvisit_vertices()  # mark all unvisited
        subject = graph.bfs('a', 'h')
        self.assertEqual(subject, (['a', 'e', 'h'], 4))

        graph.unvisit_vertices()  # mark all unvisited
        subject = graph.bfs('a', 'g')
        self.assertEqual(subject, (['a', 'e', 'g'], 4))

        graph.unvisit_vertices()  # mark all unvisited
        subject = graph.bfs('a', 'i')
        self.assertIn(subject[0], [['a', 'e', 'h', 'i'], ['a', 'e', 'g', 'i']])
        self.assertEqual(subject[1], 6)

        # (9) test path which does not exist
        graph.unvisit_vertices()  # mark all unvisited
        graph.add_to_graph('z')
        subject = graph.bfs('a', 'z')
        self.assertEqual(subject, ([], 0))

    def test_dfs(self):

        graph = Graph()

        # (1) test on empty graph
        subject = graph.dfs('a', 'b')
        self.assertEqual(subject, ([], 0))

        # (2) test on graph missing begin or dest
        graph.add_to_graph('a')
        subject = graph.dfs('a', 'b')
        self.assertEqual(subject, ([], 0))
        subject = graph.dfs('b', 'a')
        self.assertEqual(subject, ([], 0))

        # (3) test on graph with both vertices but no path
        graph.add_to_graph('b')
        subject = graph.dfs('a', 'b')
        self.assertEqual(subject, ([], 0))

        # (4) test on single edge
        graph = Graph()
        graph.add_to_graph('a', 'b', 331)
        subject = graph.dfs('a', 'b')
        self.assertEqual(subject, (['a', 'b'], 331))

        # (5) test on two edges
        graph = Graph()
        graph.add_to_graph('a', 'b', 331)
        graph.add_to_graph('b', 'c', 100)
        subject = graph.dfs('a', 'c')
        self.assertEqual(subject, (['a', 'b', 'c'], 431))

        # (6) test on linear chain with backtracking distractors
        # see linear_graph.png
        graph = Graph(csvf='test_csvs/dfs/6.csv')

        subject = graph.dfs('a', 'e')
        self.assertEqual(subject, (['a', 'b', 'c', 'd', 'e'], 4))

        graph.unvisit_vertices()  # mark all unvisited
        subject = graph.dfs('e', 'a')
        self.assertEqual(subject, (['e', 'd', 'c', 'b', 'a'], 8))

        # (7) test on linear chain with cycle
        # see cyclic_graph.png
        graph = Graph(csvf='test_csvs/dfs/7.csv')

        subject = graph.dfs('a', 'd')
        self.assertIn(subject, [(['a', 'b', 'm', 'c', 'd'], 24),
                                (['a', 'b', 'n', 'c', 'd'], 28)])

        graph.unvisit_vertices()  # mark all unvisited
        subject = graph.dfs('d', 'a')
        self.assertIn(subject, [(['d', 'c', 'm', 'b', 'a'], 240),
                                (['d', 'c', 'n', 'b', 'a'], 280)])

        # (8) test path which does not exist on graph
        graph.unvisit_vertices()
        graph.add_to_graph('z')
        subject = graph.dfs('a', 'z')
        self.assertEqual(subject, ([], 0))

    def test_topological_sort(self):

        graph = Graph()

        # (1) test on empty graph
        subject = graph.topological_sort()
        self.assertEqual(subject, [])

        # (2) test on lone vertex graph
        graph.add_to_graph('a')
        subject = graph.topological_sort()
        self.assertEqual(subject, ['a'])

        # (3) test on single edge graph
        graph = Graph()
        graph.add_to_graph('a', 'b')
        subject = graph.topological_sort()
        self.assertEqual(subject, ['a', 'b'])

        # (4) test on two edges
        graph = Graph()
        graph.add_to_graph('a', 'b')
        graph.add_to_graph('b', 'c')
        subject = graph.topological_sort()
        self.assertEqual(subject, ['a', 'b', 'c'])

        # (5) test on transitive graph with three edges
        graph = Graph()
        graph.add_to_graph('a', 'b')
        graph.add_to_graph('b', 'c')
        graph.add_to_graph('a', 'c')
        subject = graph.topological_sort()
        self.assertEqual(subject, ['a', 'b', 'c'])

        # define helper function to check validity of topological_sort result
        def check_if_topologically_sorted(g, topo):
            edges = g.get_all_edges()
            return all(topo.index(edge[0]) < topo.index(edge[1]) for edge in edges)

        # (6) test on two edges -- multiple correct answers from here on out
        graph = Graph()
        graph.add_to_graph('a', 'b')
        graph.add_to_graph('a', 'c')
        subject = graph.topological_sort()
        self.assertTrue(check_if_topologically_sorted(graph, subject))

        # (7) test on small DAG
        graph = Graph()
        graph.add_to_graph('A', 'B')
        graph.add_to_graph('A', 'F')
        graph.add_to_graph('B', 'C')
        graph.add_to_graph('D', 'A')
        graph.add_to_graph('D', 'C')
        graph.add_to_graph('E', 'C')
        graph.add_to_graph('F', 'E')
        subject = graph.topological_sort()
        self.assertTrue(check_if_topologically_sorted(graph, subject))

        # (8) test on medium DAG
        graph = Graph(csvf='test_csvs/topo/1.csv')
        subject = graph.topological_sort()
        self.assertTrue(check_if_topologically_sorted(graph, subject))

        # (9) test on large DAG
        graph = Graph(csvf='test_csvs/topo/2.csv')
        subject = graph.topological_sort()
        self.assertTrue(check_if_topologically_sorted(graph, subject))

        # (10) test on very large DAG with many edges
        graph = Graph(csvf='test_csvs/topo/3.csv')
        subject = graph.topological_sort()
        self.assertTrue(check_if_topologically_sorted(graph, subject))

        # DAGs generated by adapting https://github.com/Willtl/online-printing-shop/blob/master/generator/instance_generator.py

    def test_graph_comprehensive(self):
        # (1) test on example graph from Onsay's slides, starting from vertex A
        # see bfs_graph.png
        graph = Graph(csvf='test_csvs/bfs/8.csv')

        subject = graph.bfs('a', 'd')
        self.assertEqual(subject, (['a', 'b', 'd'], 4))

        graph.unvisit_vertices()  # mark all unvisited
        subject = graph.bfs('a', 'f')
        self.assertEqual(subject, (['a', 'c', 'f'], 4))

        graph.unvisit_vertices()  # mark all unvisited
        subject = graph.bfs('a', 'h')
        self.assertEqual(subject, (['a', 'e', 'h'], 4))

        graph.unvisit_vertices()  # mark all unvisited
        subject = graph.bfs('a', 'g')
        self.assertEqual(subject, (['a', 'e', 'g'], 4))

        graph.unvisit_vertices()  # mark all unvisited
        subject = graph.bfs('a', 'i')
        self.assertIn(subject[0], [['a', 'e', 'h', 'i'], ['a', 'e', 'g', 'i']])
        self.assertEqual(subject[1], 6)

        # (2) test path which does not exist
        graph.unvisit_vertices()  # mark all unvisited
        graph.add_to_graph('z')
        subject = graph.bfs('a', 'z')
        self.assertEqual(subject, ([], 0))

        # (3) test on linear chain with backtracking distractors
        # see linear_graph.png
        graph = Graph(csvf='test_csvs/dfs/6.csv')

        subject = graph.dfs('a', 'e')
        self.assertEqual(subject, (['a', 'b', 'c', 'd', 'e'], 4))

        graph.unvisit_vertices()  # mark all unvisited
        subject = graph.dfs('e', 'a')
        self.assertEqual(subject, (['e', 'd', 'c', 'b', 'a'], 8))

        # (4) test on linear chain with cycle
        # see cyclic_graph.png
        graph = Graph(csvf='test_csvs/dfs/7.csv')

        subject = graph.dfs('a', 'd')
        self.assertIn(subject, [(['a', 'b', 'm', 'c', 'd'], 24),
                                (['a', 'b', 'n', 'c', 'd'], 28)])

        graph.unvisit_vertices()  # mark all unvisited
        subject = graph.dfs('d', 'a')
        self.assertIn(subject, [(['d', 'c', 'm', 'b', 'a'], 240),
                                (['d', 'c', 'n', 'b', 'a'], 280)])

        # (5) test path which does not exist on graph
        graph.unvisit_vertices()
        graph.add_to_graph('z')
        subject = graph.dfs('a', 'z')
        self.assertEqual(subject, ([], 0))

        # construct random matrix
        random.seed(331)
        vertices = [s for s in string.ascii_lowercase]
        matrix = [[None] + vertices]
        probability = 0.1  # probability that two vertices are connected
        for i in range(1, len(matrix[0])):
            row = [matrix[0][i]]
            for j in range(1, len(matrix[0])):
                weight = (random.randint(1, 10))  # choose a random weight between 1 and 9
                connect = (random.random() < probability)  # connect if random draw in (0,1) < probability
                if i == j or not connect:  # such that p=0 never connects and p=1 always connects
                    weight = None  # do not connect vertex to self, either
                row.append(weight)
            matrix.append(row)

        # (6) test matrix2graph and graph2matrix
        graph = Graph()
        [graph.add_to_graph(letter) for letter in string.ascii_lowercase]  # prespecify order of vertices in dict
        graph.matrix2graph(matrix)
        subject = graph.graph2matrix()
        self.assertEqual(subject, matrix)

        # (7) test get_all_vertices by comparing certain invariants (ordering is not guaranteed under set)
        subject = graph.get_all_vertices()

        subject_ids = set([vertex.id for vertex in subject])
        solution_ids = set([letter for letter in string.ascii_lowercase])
        self.assertEqual(subject_ids, solution_ids)

        subject_degrees = {}
        for vertex in subject:
            degree = vertex.deg()
            if degree in subject_degrees:
                subject_degrees[degree] += 1
            else:
                subject_degrees[degree] = 1
        solution_degrees = {2: 8, 3: 7, 6: 1, 1: 5, 4: 3, 5: 1, 0: 1}
        self.assertEqual(subject_degrees, solution_degrees)

        # (8) test get_all_edges
        subject = graph.get_all_edges()
        solution = {('a', 's', 9), ('a', 't', 8), ('a', 'z', 6), ('b', 'l', 4), ('b', 'v', 9), ('c', 'k', 10),
                    ('c', 'u', 7), ('d', 'e', 1), ('d', 'i', 10), ('e', 'o', 5), ('e', 'q', 4), ('e', 'v', 8),
                    ('f', 'j', 6), ('g', 'h', 7), ('g', 'o', 4), ('g', 'r', 10), ('h', 'd', 4), ('h', 'k', 3),
                    ('h', 'l', 10), ('j', 'b', 5), ('j', 'o', 7), ('j', 'q', 7), ('j', 'r', 3), ('j', 'w', 6),
                    ('j', 'y', 2), ('k', 'z', 3), ('l', 'g', 7), ('l', 'h', 9), ('l', 'i', 10), ('l', 'w', 6),
                    ('m', 'a', 2), ('m', 'f', 10), ('m', 'j', 3), ('n', 't', 6), ('o', 'd', 5), ('o', 'l', 9),
                    ('p', 'q', 1), ('q', 'o', 4), ('q', 'z', 7), ('r', 'c', 4), ('s', 'i', 7), ('s', 'j', 8),
                    ('s', 'k', 8), ('s', 'w', 10), ('t', 'd', 1), ('t', 'g', 2), ('t', 'q', 7), ('t', 'u', 9),
                    ('u', 'g', 8), ('u', 'y', 3), ('v', 'i', 8), ('v', 'x', 5), ('w', 'c', 3), ('w', 'd', 2),
                    ('x', 'h', 7), ('x', 'j', 4), ('x', 'u', 3), ('y', 'e', 7), ('y', 'l', 4), ('y', 'n', 3),
                    ('z', 'j', 1), ('z', 'n', 4), ('z', 'q', 7), ('z', 's', 4), ('z', 'y', 5)}
        self.assertEqual(subject, solution)

        # define helper function to check validity of bfs/dfs result
        def is_valid_path(graph, search_result):
            path, dist = search_result
            length = 0
            for i in range(len(path) - 1):
                begin, end = path[i], path[i + 1]
                edge = graph.get_edge_by_ids(begin, end)
                if edge is None:
                    return False  # path contains some edge not in the graph
                length += edge[2]
            return length == dist  # path consists of valid edges: return whether length matches

        # (9) check bfs/dfs on all pairs of vertices in graph
        for begin in vertices:
            for end in vertices:
                if begin != end:
                    # (9.1) test bfs
                    subject = graph.bfs(begin, end)
                    self.assertTrue(is_valid_path(graph, subject))
                    if subject[0]:
                        self.assertTrue(subject[0][0] == begin and subject[0][-1] == end)
                    graph.unvisit_vertices()

                    # (9.2) test dfs
                    subject = graph.dfs(begin, end)
                    self.assertTrue(is_valid_path(graph, subject))
                    if subject[0]:
                        self.assertTrue(subject[0][0] == begin and subject[0][-1] == end)
                    graph.unvisit_vertices()

    def test_boss_order_validity(self):

        graph = Graph()

        # (1) test on empty graph
        self.assertTrue(graph.boss_order_validity())

        # (2) 2 vertices, one edge
        graph.add_to_graph('Margit', 'Godrick')
        graph.unvisit_vertices()
        self.assertTrue(graph.boss_order_validity())

        # (3) 3 vertices in a linked list
        graph.add_to_graph('Godrick', 'Renalla')
        graph.unvisit_vertices()
        self.assertTrue(graph.boss_order_validity())

        # (4) 3 vertices, not possible to win
        graph.add_to_graph('Renalla', 'Margit')
        graph.unvisit_vertices()
        self.assertFalse(graph.boss_order_validity())

        # (5) one vertex, not possible to beat the game
        graph = Graph()
        graph.add_to_graph('Godfrey', 'Godfrey')
        self.assertFalse(graph.boss_order_validity())

        # (6) two vertices, not possible to beat the game
        graph = Graph()
        graph.add_to_graph('Morgott', 'Fire Giant')
        graph.add_to_graph('Fire Giant', 'Morgott')
        self.assertFalse(graph.boss_order_validity())

        # (7a) many vertices, possible to beat the game
        graph = Graph()
        graph.add_to_graph('Margit', 'Godrick')
        graph.add_to_graph('Godrick', 'Renalla')
        graph.add_to_graph('Margit', 'Renalla')
        graph.add_to_graph('Morgott', 'Margit')
        graph.add_to_graph('Godskin Duo', 'Margit')
        graph.add_to_graph('Morgott', 'Godskin Duo')
        graph.add_to_graph('Godfrey', 'Morgott')
        graph.add_to_graph('Godfrey', 'Godskin Duo')
        self.assertTrue(graph.boss_order_validity())

        # (7b) many vertices, not possible to beat the game
        graph = Graph()
        graph.add_to_graph('Margit', 'Godrick')
        graph.add_to_graph('Godrick', 'Renalla')
        graph.add_to_graph('Margit', 'Renalla')
        graph.add_to_graph('Morgott', 'Margit')
        graph.add_to_graph('Godskin Duo', 'Margit')
        graph.add_to_graph('Morgott', 'Godskin Duo')
        graph.add_to_graph('Godfrey', 'Morgott')
        graph.add_to_graph('Godfrey', 'Godskin Duo')
        graph.add_to_graph('Renalla', 'Godfrey')
        self.assertFalse(graph.boss_order_validity())

        # (8) big linked list
        graph = Graph()
        colors = ['Margit', 'Maliketh', 'Fire Giant', 'Renalla', 'Godrick', 'Sir Gideon Ofnir', 'Hoarah Loux',
                  'Morgott',
                  'Godskin Duo', 'Radagon', 'Elden Beast', 'Malenia', 'Starscourge Radahn', 'Mohg']
        for i, id in enumerate(colors):
            if i + 1 < len(colors):
                graph.add_to_graph(id, colors[i + 1])
        self.assertTrue(graph.boss_order_validity())

        # (9) circular linked list
        graph.add_to_graph('Mohg', 'Margit')
        graph.unvisit_vertices()
        self.assertFalse(graph.boss_order_validity())

        # (10a) Miyazaki had the "brilliant" idea of potentially giving every enemy (even tortoises) in the game other enemies
        # that must be defeated first, forming this big graph with enemies labeled by id as numbers, can beat the game
        graph = Graph(csvf='test_csvs/application/1.csv')
        self.assertTrue(graph.boss_order_validity())

        # (10b) big graph, cannot beat the game anymore :(
        graph.add_to_graph('724', '688')
        graph.unvisit_vertices()
        self.assertFalse(graph.boss_order_validity())

    def test_feedback_xml_validity(self):

        path = "feedback.xml"
        xml_doc = minidom.parse(path)
        response = {}
        tags = ["netid", "feedback", "difficulty", "time", "citations", "type", "number"]

        # Assert that we can access all tags
        for tag in tags:
            raw = xml_doc.getElementsByTagName(tag)[0].firstChild.nodeValue
            lines = [s.strip() for s in raw.split("\n")]  # If multiple lines, strip each line
            clean = " ".join(lines).strip()  # Rejoin lines with spaces and strip leading space
            self.assertNotEqual("REPLACE", clean)  # Make sure entry was edited
            response[tag] = clean  # Save each entry

        # Assert that difficulty is a float between 0-10
        difficulty_float = float(response["difficulty"])
        self.assertGreaterEqual(difficulty_float, 0.0)
        self.assertLessEqual(difficulty_float, 10.0)

        # Assert that hours is a float between 0-100 (hopefully it didn't take 100 hours!)
        time_float = float(response["time"])
        self.assertGreaterEqual(time_float, 0.0)
        self.assertLessEqual(time_float, 100.0)

        # Assert assignment type and number was not changed
        self.assertEqual("Project", response["type"])
        self.assertEqual("9", response["number"])

    """
    End Graph Tests
    """


if __name__ == '__main__':
    unittest.main()
