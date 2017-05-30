# -*- coding: utf-8 -*-
import collections
from heapq import heappush, heappop

class Graph:
    Edge = collections.namedtuple("Edge", ("dest", "weight"))
    FrontierEntry = collections.namedtuple("FrontierEntry", ("distance", "vertex"))
    
    def __init__(self, filename=None):
        """
        Initialize a graph by reading from the specified file, or a blank graph
        if unspecified.
        """
        self._out_edges = {}
        self.vertices = set()
        self.num_vertices = 0
        self.num_edges = 0
        if(filename):
            self.read_from(filename)
    
    def read_from(self, filename):
        """
        Reads graph from the specified file.
        File format: Each line specifies a vertex followed by its out-edges.
                     Each edge is "v,w" where v is the destination vertex and
                     w is the weight of the edge.
        """
        FILE = open(filename, "r")
        for line in FILE:
            tokens = line.split()
            if len(tokens) == 0: continue
            src = int( tokens[0] )
            for edge in tokens[1:]:
                d,w = edge.split(",")
                d,w = int(d), int(w)
                self.vertices.add(d)
                try:
                    self._out_edges[src].append(Graph.Edge(dest=d, weight=w))
                except KeyError:
                    self._out_edges[src] = [Graph.Edge(dest=d, weight=w)]
                    self.vertices.add(src)
                self.num_edges += 1
        FILE.close()
        for v in self.vertices:
            if v not in self._out_edges: self._out_edges[v] = []
        self.num_vertices = len(self.vertices)

    def dijkstra(self, src):
        """
        Runs Dijkstra's algorithm to find the shortest distance from src to all
        vertices reachable from it.
        Returns the result as a dictionary (vertex => distance)
        """
        frontier = [] # heap data-structure to track the best potential edges to explore
        explored = set()
        distances = {}
        # start with vertex src, distance=0
        heappush(frontier, Graph.FrontierEntry(vertex=src, distance=0))
        while(frontier):
            dist, v = heappop(frontier)
            if v in explored: continue
            distances[v] = dist
            explored.add(v)
            for dest, weight in self._out_edges[v]:
                if dest not in explored:
                    heappush( frontier, \
                              Graph.FrontierEntry(vertex=dest, distance=dist+weight) )
        return distances
        