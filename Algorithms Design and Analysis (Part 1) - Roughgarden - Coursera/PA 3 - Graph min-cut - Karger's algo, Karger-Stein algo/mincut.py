# -*- coding: utf-8 -*-
"""
Implements Karger's randomized contraction algorithm
to compute the minimum-cut of a connected graph.
"""
import random
import copy
import math

class Graph:
    def __init__(self, filename=None):
        """
        Initialize a graph by reading adjacency-list from the specified file,
        or a blank graph if unspecified.
        """
        self._edges = {} # Dict - vertex => [adjacent vertices]
        self.num_vertices = 0
        self.num_edges = 0
        if(filename):
            self.read_from(filename)
    
    def read_from(self, filename):
        """
        Reads graph as adjacency-list from the specified file.
        """
        FILE = open(filename, "r")
        for line in FILE:
            l = line.split()
            if(len(l) == 0): continue
            vertex = int(l[0])
            edges = [int(edge) for edge in l[1:] if edge != vertex]
            self._edges[vertex] = edges
            self.num_vertices += 1
            self.num_edges += len(edges)
        FILE.close()
        # num_edges needs to be halved, since each edge appears twice in the
        # adjacency-list for an undirected graph
        self.num_edges //= 2 
    
    def contract_edge(self, u, v):
        """
        Contracts the edge(s) between vertices u and v.
        Merges vertex v into u, and removes all self-loops on u.
        """
        num_edges_delta = 0 # track the change in number of edges
        u_edges = self._edges[u]
        v_edges = self._edges[v]

        # update adjacency-list for vertex u (add neighbors of v)
        new_u_edges = [e for e in u_edges if e != v] + \
                      [e for e in v_edges if e != u]
        self._edges[u] = new_u_edges
        num_edges_delta += len(new_u_edges) - len(u_edges)

        # update adjacencies of neighbors of v (to point to u)
        for w in v_edges:
            if w != u:
                w_edges = self._edges[w]
                w_edges[w_edges.index(v)] = u

        # remove vertex v
        num_edges_delta -= len(v_edges)
        del(self._edges[v])
        
        # update number of edges (num_edges_delta has double-counted the change)
        self.num_edges += (num_edges_delta // 2)
        self.num_vertices = len(self._edges)

    
    def pick_random_edge(self):
        """
        Returns a randomly selected edge from the graph as a tuple.
        """
        n = random.randrange(2 * self.num_edges)
        for v,neighbors in self._edges.iteritems():
            if n < len(neighbors):
                return (v,neighbors[n])
            else:
                n -= len(neighbors)

    def contract_random_edges(self, k=2):
        """
        Performs randomized edge contractions until there are k vertices remaining.
        """
        while(self.num_vertices > k):
            u,v = self.pick_random_edge()
            self.contract_edge(u,v)

    def karger_mincut(self, num_trials=None):
        """
        Runs Karger's randomized contraction algorithm to find the minimum-sized
        cut of the graph with a high probability.
        Graph is not modified (contractions are performed on a copy of the graph).
        num_trials => Number of times to run the algorithm before returning
                      the best solution.
                      If unspecified, defaults to binomial(N,2)*ln(N), where N is the 
                      number of vertices. This makes P(failing to find the mincut) <= (1/N)
        """
        N = self.num_vertices
        num_trials = int( num_trials or math.ceil(math.log(N)*N*(N-1)/2) )
        minCutSize = self.num_edges + 1 # upper bound on the mincut size
        for i in xrange(num_trials):
            graph = copy.deepcopy(self)
            graph.contract_random_edges(2) # contract to 2 vertices
            cutSize = len(graph.__edges.values()[0]) # cut size = degree of the super-vertex
            if (cutSize < minCutSize):
                minCutSize = cutSize
        return minCutSize
    
    def karger_stein(self):
        """
        Performs a single trial of the Karger-Stein algorithm and returns the
        size of the mincut.
        Note: Modifies the graph.
        """
        N = self.num_vertices
        if(N <= 6):
            return self.karger_mincut()
            
        # v = int(math.ceil(N/math.sqrt(2) + 1)) # number of edges to contract to
        v = int(math.ceil(N/math.sqrt(2))) # number of edges to contract to
        self.contract_random_edges(v)
        graphCopy = copy.deepcopy(self)
        a = self.karger_stein()
        b = graphCopy.karger_stein()
        return min(a,b)
    
    def karger_stein_mincut(self, num_trials=None):
        """
        Runs the improved (recursive) Karger-Stein contraction algorithm to find 
        the minimum-sized cut of the graph with a high probability.
        Graph is not modified (contractions are performed on a copy of the graph).
        num_trials => Number of times to run the algorithm before returning
                      the best solution.
                      If unspecified, defaults to log2(N)*ln(N), where N is the 
                      number of vertices. This makes P(failing to find the mincut) <= (1/N)
        """
        N = self.num_vertices
        num_trials = int( num_trials or math.ceil(math.log(N,2)*math.log(N)) )
        minCutSize = self.num_edges + 1 # upper bound on the mincut size
        for i in xrange(num_trials):
            graph = copy.deepcopy(self)
            cutSize = graph.karger_stein()
            if(cutSize < minCutSize):
                minCutSize = cutSize
        return minCutSize
    
    def __repr__(self):
#        s = "\n".join("{}: {}".format(v,l) \
#                      for (v,l) in self._edges.iteritems())
        return "Graph(|V|={}, |E|={})".format(self.num_vertices, self.num_edges)
