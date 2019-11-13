from sys import argv, exit
import os


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


p_infinity = float('Inf')


def get_current(known_items, fScore):  # known_items is a set
    lowest = p_infinity
    retval = str()
    for item in known_items:
        if fScore[item] < lowest:
            lowest = fScore[item]
            retval = item
    return retval


def reconstruct_path(came_from, current):
    total_path = list()
    total_path.append(current)
    while current in came_from:
        current = came_from[current]
        total_path.append(current)
    return total_path


class GraphEL:
    '''
    Edge list representation of a graph
    The edges argument is a list of tuples (v1, v2, weight)
    Vertices are not explicitly maintained, only contained with the edge list
    '''

    def __init__(self, nvertices, edges):
        self.edges = edges  # The edges argument is a list of tuples (v1, v2, weight)
        self.nvertices = nvertices

    def __repr__(self):
        return '\n'.join(map(str, self.edges))

    def list_of_vertices(self):
        # build set of vertices
        vertices = set()
        ret_list = list()
        for e in self.edges:
            v1 = e[0]
            v2 = e[1]
            if v1 not in vertices:
                vertices.add(v1)
                ret_list.append(v1)
            if v2 not in vertices:
                vertices.add(v2)
                ret_list.append(v2)
        return ret_list

    def find_neighbors(self, current):
        neighbors = list()
        for e in self.edges:
            if current == e[0]:
                neighbors.append(e[1])
        return neighbors

    def dist_between(self, v1, v2):
        dist = p_infinity
        for e in self.edges:
            if v1 == e[0] and v2 == e[1]:
                dist = e[2]
        return dist

    def a_star(self, start_vertex, end_vertex):
        # Set of nodes already evaluated
        visited_items = set()  # closedSet
        def_map_val = p_infinity
        # set of known nodes which have yet to be evaluated:
        known_items = set()  # openSet
        known_items.add(start_vertex)

        came_from = dict()

        # list of vertices
        vertices = self.list_of_vertices()

        # initialize this map where each vertex has a cost associated with it
        # specifically the cost of getting from start to the key vertex.
        # it should have a default value of infinity for each vertex.
        gScore = dict()
        for v in vertices:
            gScore[v] = p_infinity
        # The cost of going from start to start is 0
        gScore[start_vertex] = 0

        # for each node the total cost of getting from start to the goal by passing by that node.
        # That value is partly known and partly heuristic.
        # Represented by map with default value of infinity
        fScore = dict()
        for v in vertices:
            fScore[v] = p_infinity

        # For the first node, (start), that value is completely heuristic
        fScore[start_vertex] = heuristic_estimate(start_vertex, end_vertex)

        while len(known_items) != 0:
            current = get_current(known_items, fScore)
            if current == end_vertex:
                return reconstruct_path(came_from, current)
            known_items.remove(current)  # openSet
            visited_items.add(current)  # closedSet

            # grab neighbors
            neighbors = self.find_neighbors(current)
            for n in neighbors:
                if n in visited_items:
                    continue
                elif n not in known_items:  # dicover new node
                    known_items.add(n)

                tentative_Gscore = gScore[current] + self.dist_between(current, n)
                if tentative_Gscore >= gScore[n]:
                    continue  # not a better path

                # this path is best till now so record it
                came_from[n] = current
                gScore[n] = tentative_Gscore
                fScore[n] = gScore[n] + heuristic_estimate(n, end_vertex)

        # if past while loop then
        s = "failure"
        retval = list()
        retval.append(s)
        return retval


def heuristic_estimate(start_city, end_city):
    key = (start_city, end_city)
    lookup = build_heuristic_dict()
    rule = lookup[key]
    return rule


def build_heuristic_dict():
    rule_lookup = dict()
    file_name = "euclidian.txt"
    file = open(file_name, "r")
    for line in file:
        line_items = line.split()
        s = line_items[0]
        e = line_items[1]
        rule = float(line_items[2])
        key = (s, e)
        value = rule
        rule_lookup[key] = value
    file.close()
    return rule_lookup


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
            v1 = v1.lstrip('(')
            v2 = v2.strip()
            weight = weight.strip()
            weight = weight.strip(")\n")
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


def usage():
    print("> python3 graph.py [start_city] [end_city]")
    exit(0)


if __name__ == '__main__':
    if len(argv) < 3:
        usage()
    filename = "routes.txt"
    start = argv[1]
    end = argv[2]
    route_graph = read_from_file(filename)
    path = route_graph.a_star(start, end)
    path.reverse()

    n = len(path)
    print(path[0])
    for i in range(1, n):
        print(" -> " + path[i])


