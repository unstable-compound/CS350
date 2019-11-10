from sys import argv, exit
from heap import Heap



class AdjVertex:
    '''
    Vertex of an adjacency list.
    Holds its label and a list of adjacent vertices in neighbors
    Each adjacent vertex is stored with (label, edge weight)
    '''

    def __init__(self, label):
        self.label = label
        self.neighbors = []

    def add_edge(self, label, weight):
        self.neighbors.append((label, weight))





class GraphEL:
    '''
    Edge list representation of a graph
    The edges argument is a list of tuples (v1, v2, weight)
    Vertices are not explicitly maintained, only contained with the edge list
    '''
    def __init__(self, nvertices, edges):
        self.edges = edges
        self.nvertices = nvertices

    def convert_to_adj(self):
        return GraphAdj(self.nvertices, self.edges)

    def __repr__(self):
        return '\n'.join(map(str, self.edges))

    def A_star(self, start_city, end_city):
        # Set of nodes already evaluated
        visited_items = {}

        # set of known nodes which have yet to be evaluated:
        known_items = {start_city}

        came_from = {
            "": "",
        }
















def read_from_file(fname):
    '''
    Creates an edge list representation of a graph from a text file in the format
    <v1>, <v2>, <weight>
    Assumed to be an undirected graph so we add two edges for each line to represent
    v1 --> v2 and v2 --> v1
    '''
    edges = []
    with open(fname, 'r') as f:
        vertices = set()
        for line in f:
            # Splits the string into a list "x, y, 3" --> ['x', ' y', ' 3']
            v1, v2, weight = line.split(',')
            # Strips white space from the front and back of strings
            v1 = v1.strip()
            v2 = v2.strip()
            # convert weight into numeric value
            weight = float(weight)
            # append two tuples as the graph is undirected
            edges.append((v1, v2, weight))
            edges.append((v2, v1, weight))
            if v1 not in vertices:
                vertices.add(v1)
            if v2 not in vertices:
                vertices.add(v2)
    return GraphEL(len(vertices), edges)