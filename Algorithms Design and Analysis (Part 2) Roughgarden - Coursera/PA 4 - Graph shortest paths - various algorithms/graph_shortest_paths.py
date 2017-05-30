# -*- coding: utf-8 -*-
from collections import namedtuple
from heapq import heappush, heappop

#%%
class Graph:
    Edge = namedtuple("Edge", ("src","dest","cost"))
    Neighbor = namedtuple("OutEdge", ("vertex","cost"))
    class NegativeCycleError(ValueError):
        """ Raised when the graph has a negative-cost cycle."""
    
    def __init__(self, filename=None):
        """
        Initialize a graph by reading from the specified file, or a blank graph
        if unspecified.
        """
        self._out_neighbors = list()
        self._edges         = list()
        self._vertices      = set()
        if(filename):
            self.read_from(filename)
    
    def read_from(self, filename):
        """
        Reads graph from the specified file.
        File format: First line "<number of vertices>  <number of edges>"
                     Each successive line specifies an edge as 
                     "<source vertex>  <destination vertex>  <edge cost>"
                     All vertices are referred to by integer labels.
        """
        with open(filename, "r") as FILE:
            l = FILE.readline().split()
            expected_num_vertices, expected_num_edges = map(int, l)
            self._out_neighbors = \
                [None] + [[] for i in xrange(1,expected_num_vertices+1)]
            for line in FILE:
                l = line.split()
                if len(l) == 0: continue
                src, dest, cost = map(int, l)
                self.add_edge(src, dest, cost)
            
        assert self.num_vertices() == expected_num_vertices
        assert self.num_edges() == expected_num_edges
    
    def validate(self):
        """
        Do some sanity checks on the graph-data.
        Asserts upon failure to validate.
        """
        # Assert that the vertices are labeled from 1->num_vertices.
        # This restriction can be lifted by maintaining a separate mapping from
        # natural-numbers to vertex-labels.
        assert self._vertices == set(xrange(1, self.num_vertices()+1))
        
    def add_edge(self, src, dest, cost):
        self._edges.append(Graph.Edge(src,dest,cost))
        self._vertices.add(src)
        self._vertices.add(dest)
        if src >= len(self._out_neighbors):
            self._out_neighbors += [[] for i in xrange(src+1-len(self._out_neighbors))]
        self._out_neighbors[src].append(Graph.Neighbor(dest,cost))
            
    def num_edges(self):
        return len(self._edges)
        
    def num_vertices(self):
        return len(self._vertices)
        
    def floyd_warshall_shortest_distances(self):
        distances = [None] + \
                    [[None]*(self.num_vertices()+1) for i in xrange(self.num_vertices())]
        for src,dest,cost in self._edges:
            distances[src][dest] = cost
        for v in xrange(1,self.num_vertices()+1):
            distances[v][v] = 0
        
        for v in xrange(1,self.num_vertices()+1):
            for src in xrange(1,self.num_vertices()+1):
                for dest in xrange(1,self.num_vertices()+1):
                    if distances[src][v] is None or \
                       distances[v][dest] is None:
                           continue
                    new_distance = distances[src][v]+distances[v][dest]
                    if distances[src][dest] is None or \
                       new_distance < distances[src][dest]:
                           distances[src][dest] = new_distance
        
        for v in xrange(1,self.num_vertices()+1):
            if distances[v][v] < 0:
                raise self.NegativeCycleError(\
                    "Graph has a negative-cost cycle involving vertex {}".format(v,))
                
        return distances
    
    def bellman_ford_shortest_distances_from(self, src):
        distances = [None]*(self.num_vertices()+1)
        distances[src] = 0
        
        for i in xrange(1,self.num_vertices()):
            reached_fixed_pt = True
            for u,v,cost in self._edges:
                if distances[u] is None:
                    continue
                if distances[v] is None or \
                   distances[u] + cost < distances[v]:
                    distances[v] = distances[u] + cost
                    reached_fixed_pt = False
            if reached_fixed_pt:
                # print "Breaking after {}th iteration".format(i,)
                break
        
        # Check for presence of a negative-cycle
        for u,v,cost in self._edges:
            if distances[u] is None:
                continue
            if distances[v] is None or \
               distances[u] + cost < distances[v]:
                raise self.NegativeCycleError(\
                    "Graph has a negative-cost cycle involving vertices: {} and {}".format(u,v))
        
        return distances
    
    def johnson_shortest_distances(self):
        self.validate()
        orig_num_vertices = self.num_vertices()
        
        # Add a temporary vertex
        temp_vertex = orig_num_vertices + 1
        self._vertices.add(temp_vertex)
        for v in xrange(1,orig_num_vertices+1):
            self.add_edge(temp_vertex, v, 0)
        vertex_weights = self.bellman_ford_shortest_distances_from(temp_vertex)
        # Remove the temporary vertex
        self._vertices.remove(temp_vertex)
        self._edges = [edge for edge in self._edges \
                       if edge.src != temp_vertex and edge.dest != temp_vertex]
        self._out_neighbors.pop()
        
        # Adjust edge-weights to be positive
        self._out_neighbors = \
            [None] + [[] for i in xrange(1,orig_num_vertices+1)]
        for i,(src,dest,cost) in enumerate(self._edges):
            cost += (vertex_weights[src] - vertex_weights[dest])
            self._edges[i] = Graph.Edge(src,dest,cost)
            self._out_neighbors[src].append(Graph.Neighbor(dest,cost))
        
        # Compute all pairwise distances
        distances = self.dijkstra_shortest_distances_all_pairs()
        for src in xrange(1,self.num_vertices()+1):
            for dest in xrange(1,self.num_vertices()+1):
                if distances[src][dest] is not None:
                    distances[src][dest] += (vertex_weights[dest] - vertex_weights[src])
        
        # Revert edge-weights to original
        self._out_neighbors = \
            [None] + [[] for i in xrange(1,orig_num_vertices+1)]
        for i,(src,dest,cost) in enumerate(self._edges):
            cost += (vertex_weights[dest] - vertex_weights[src])
            self._edges[i] = Graph.Edge(src,dest,cost)
            self._out_neighbors[src].append(Graph.Neighbor(dest,cost))
            
        return distances
    
    def dijkstra_shortest_distances_all_pairs(self):
        distances = [None]
        for i in xrange(1,self.num_vertices()+1):
            distances.append(self.dijkstra_shortest_distances_from(i))
        return distances
        
    def dijkstra_shortest_distances_from(self, src):
        FrontierEntry = namedtuple("FrontierEntry", ("distance","vertex"))
        frontier = []
        explored = set()
        distances = [None]*(self.num_vertices()+1)
        
        heappush(frontier, FrontierEntry(distance=0, vertex=src) )
        while frontier:
            dist, v = heappop(frontier)
            if v in explored:
                continue
            explored.add(v)
            distances[v] = dist
            for n, cost in self._out_neighbors[v]:
                if n not in explored:
                    heappush( frontier,
                              FrontierEntry(distance=dist+cost, vertex=n) )
        
        return distances
        
    def __repr__(self):
        return "Graph(|V|={}, |E|={})".format(self.num_vertices(), self.num_edges())

#%%

































