# -*- coding: utf-8 -*-
import os
import sys
sys.path.append(os.path.abspath("../../unionfind"))
from unionfind import UnionFind
from collections import namedtuple
from heapq import heappush, heappop, heapify

#%%
class Graph:
    # Tuple to store edge-information for the graph.
    Edge = namedtuple("Edge", ("cost", "vertex1", "vertex2"))
    # Tuple to store adjacency-information for vertices in the graph.
    OutEdge = namedtuple("OutEdge", ("vertex","cost"))
    
    def __init__(self, filename=None):
        """
        Intialize an undirected graph by reading from the specified file, or a 
        blank graph if unspecified.
        """
        self._out_edges = dict()
        self._vertices  = set()
        self._edges     = list()
        if(filename):
            self.read_from(filename)
    
    def num_edges(self):
        return len(self._edges)
    
    def num_vertices(self):
        return len(self._vertices)
        
    def read_from(self, filename):
        """
        Reads graph from the specified file.
        File format: First line "<number of vertices>  <number of edges>"
                     Each successive line specifies an edge as 
                     "<vertex 1>  <vertex 2>  <edge cost>"
                     All vertices are referred to by integer labels.
        """
        with open(filename, "r") as FILE:
            l = FILE.readline().split()
            expected_num_vertices, expected_num_edges = map(int, l)
            for line in FILE:
                l = line.split()
                if len(l) == 0: continue
                v, w, cost = map(int, l)
                self.add_edge(cost, v, w)
        
        assert self.num_vertices() == expected_num_vertices
        assert self.num_edges() == expected_num_edges
    
    def add_edge(self, cost, v, w):
        """
        Add an edge to the graph between vertices v and w, with the specified cost.
        Also add the vertices v and w to the graph, if not already present.
        """
        self._edges.append(Graph.Edge(cost, v, w))
        # Add edge to adjacency-list for vertex v
        try:
            self._out_edges[v].append(Graph.OutEdge(w, cost))
        except KeyError:
            self._out_edges[v] = [Graph.OutEdge(w, cost)]
            self._vertices.add(v)
        # Add edge to adjacency-list for vertex w
        try:
            self._out_edges[w].append(Graph.OutEdge(v, cost))
        except KeyError:
            self._out_edges[w] = [Graph.OutEdge(v, cost)]
            self._vertices.add(w)
    
    def add_vertex(self, v):
        """
        Add a vertex to the graph.
        """
        self._vertices.add(v)
        self._out_edges[v] = []
    
    def compute_total_cost(self):
        """
        Return the sum of the costs of the edges in the graph.
        """
        cost = 0
        for edges in self._out_edges.itervalues():
            for edge in edges:
                cost += edge.cost
        return cost/2
    
    def kruskal_mst(self):
        """
        Run Kruskal's algorithm to fine the minimum-cost spanning tree of the graph.
        Returns a tuple with the cost of the MST and a Graph object for the MST.
        """
        mst = Graph()
        total_cost = 0 # total cost of the MST
        # Initialize a union-find universe representing the spanning forest 
        # with all vertices separate.
        forest_uf = UnionFind()
        map(lambda v: forest_uf.add_singleton(v), self._vertices)
        # Add edges to the MST in increasing order of edge-cost
        edges = sorted(self._edges, key=lambda e: e.cost)
        for (cost, vertex1, vertex2) in edges:
            # Have we spanned all vertices?
            if mst.num_vertices() == self.num_vertices():
                break
            # Does the current edge introduce a cycle?
            if forest_uf.find_root(vertex1) == forest_uf.find_root(vertex2):
                continue
            mst.add_edge(cost, vertex1, vertex2)
            total_cost += cost
            forest_uf.union(vertex1, vertex2)
        
        return total_cost, mst
    
    def prim_mst(self):
        """
        Run Prim's algorithm to fine the minimum-cost spanning tree of the graph.
        Returns a tuple with the cost of the MST and a Graph object for the MST.
        """
        total_cost = 0
        mst = Graph()
        v = next(iter(self._vertices))
        mst.add_vertex(v)
        spanned = set([v])
        # Initialize the min-heap for tracking the cheapest edges to span
        span_frontier = map( lambda e: Graph.Edge(e.cost, v, e.vertex), \
                             self._out_edges[v] )
        heapify(span_frontier)
        while len(spanned) != self.num_vertices():
            cost, v, w = heappop(span_frontier)
            if w in spanned: continue
            total_cost += cost
            mst.add_edge(cost, v, w)
            spanned.add(w)
            for out_edge in self._out_edges[w]:
                heappush( span_frontier, \
                          Graph.Edge(out_edge.cost, w, out_edge.vertex) )
        
        return total_cost, mst
    
    def __repr__(self):
        return "Graph(|V|={}, |E|={})".format(self.num_vertices(), self.num_edges())
