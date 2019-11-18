from sys import argv, exit
import math

import argparse


class TreeNode:
    def __init__(self, val):
        self.val = val
        self.parent = None

    def attach(self, parent):
        self.parent = parent

    def __repr__(self):
        if self.parent is None:
            p = "None"
        else:
            p = str(self.parent.val)
        return "{} -> {}".format(str(self.val), p)


class UnionFind:
    def __init__(self):
        self.refs = {}
        self.trees = []

    def makeset(self, x):
        # Keys must be unique
        if x in self.refs:
            raise KeyError
        self.refs[x] = len(self.trees)
        self.trees.append(TreeNode(x))

    def find(self, x):
        current = self.trees[self.refs[x]]
        while current.parent is not None:
            current = current.parent
        return current.val

    def union(self, x, y):
        parent_x = self.trees[self.refs[self.find(x)]]
        parent_y = self.trees[self.refs[self.find(y)]]
        parent_x.attach(parent_y)

    def __repr__(self):
        return ', '.join(map(str, self.trees))


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


class GraphAdj:
    def __init__(self, nvertices, edges):
        '''
        Creates an adjacency matrix from an edge list
        Uses a dictionary to hold each vertex.
        Key, value ==> label : AdjVertex object
        '''
        self.nvertices = nvertices
        self.vertices = {}
        for v1, v2, cost in edges:
            if v1 not in self.vertices.keys():
                self.vertices[v1] = AdjVertex(v1)
            self.vertices[v1].add_edge(v2, cost)

    def __repr__(self):
        ''' Representation of graph when used in print() statement '''
        ret = []
        for vertex in self.vertices:
            ret.append(vertex + ' [' + \
                       ', '.join(map(str, self.vertices[vertex].neighbors)) \
                       + ']')
        return '\n'.join(ret)


def is_acyclic(union_find, edge):
    if union_find.find(edge[0]) is union_find.find(edge[1]):
        return False
    else:
        return True


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

    #  The edges argument is a list of tuples (v1, v2, weight)
    def sort_edges(self):
        self.edges.sort(key=lambda x: x[2])

    def list_of_vertices(self):
        # build set of vertices
        vertices = list()
        for e in self.edges:
            v1 = e[0]
            v2 = e[1]
            if v1 not in vertices:
                vertices.append(v1)
            if v2 not in vertices:
                vertices.append(v2)
        return vertices

    def fill_union_find(self, union_find):
        vertices = self.list_of_vertices()
        for v in vertices:
            union_find.makeset(v)
        return union_find

    def __repr__(self):
        return '\n'.join(map(str, self.edges))

    #   Input: A weighted, connected graph G = <V,E>
    #   Output: M, the set of edges composing a minimum spanning tree of G.
    def kruskals(self):
        self.sort_edges();
        min_span_tree_set = set()
        union_find = UnionFind()
        union_find = self.fill_union_find(union_find)

        num_processed_edges = 0
        while len(min_span_tree_set) < self.nvertices - 1:
            edge = self.edges[num_processed_edges]
            v = edge[0]
            u = edge[1]

            if is_acyclic(union_find, edge):
                min_span_tree_set.add(edge)
                union_find.union(v, u)
            num_processed_edges += 1
        return min_span_tree_set


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


if __name__ == '__main__':
    # Parsing command line options
    parser = argparse.ArgumentParser()
    parser.add_argument('-e', '--edgelist', action='store_true',
                        default=True, help='Use edge list representation')
    parser.add_argument('-a', '--adjlist', action='store_true',
                        default=False, help='Use adjacency list representation')
    parser.add_argument('-f', '--file', action='store', help='file to read graph from')
    args = parser.parse_args()

    # Create graph in desired form
    graph = read_from_file(args.file)

    graph.sort_edges()
    min_span_tree = graph.kruskals()
    print("The edges involved in the minimum spanning tree are as follows: ")
    t_weight = 0.0
    for edge in min_span_tree:
        print(edge)
        t_weight += edge[2]
    print("The total weight of the tree is: " + str(t_weight))

