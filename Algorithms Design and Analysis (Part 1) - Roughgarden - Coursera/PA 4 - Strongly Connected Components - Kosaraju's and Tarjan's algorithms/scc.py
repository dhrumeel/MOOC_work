# -*- coding: utf-8 -*-
"""
Classes and procedures to handle simple directed-graphs.
Procedures to:
    - Perform DFS starting from a given vertex or on the entire (possibly disconnected) graph
    - Sort the vertices in a topological order
    - Find the strongly-connected-components (using either Kosaraju's algorithm
      or using Tarjan's algorithm).
"""
class Graph:
    def __init__(self, filename=None):
        """
        Initialize a graph by reading from the specified file, or a blank graph
        if unspecified.
        """
        self._out_edges = {} # dict { vertex => [outgoing-edges] }
        self.num_vertices = 0
        self.num_edges = 0
        self.vertices = set() # set of all vertices
        if(filename):
            self.read_from(filename)
    
    def read_from(self, filename):
        """
        Reads graph from the specified file.
        File format: Each line specifies a vertex followed by its "out-neighbors".
        """
        data = []
        with open(filename, "r") as FILE:
            for line in FILE:
                l = line.split()
                if len(l) == 0:
                    continue
                data.append(map(int, l))
        self.add_graph_data(data)
        
    def add_graph_data(self, data):
        for line in data:
            vertex = line[0]
            out_neighbors = line[1:]
            try:
                self._out_edges[vertex].extend(out_neighbors)
            except KeyError:
                self._out_edges[vertex] = list(out_neighbors)
                self.vertices.add(vertex)
            self.vertices.update(out_neighbors)
            self.num_edges += len(out_neighbors)
        # Add source and sink nodes to the dicts
        for v in self.vertices:
            if v not in self._out_edges: 
                self._out_edges[v] = []
        self.num_vertices = len(self.vertices)
        
    def reverse_graph(self):
        """
        Reverses the graph (i.e. reverses the direction of all edges).
        Reversed-edges are cached into self._in_edges after the first call.
        """
        if not hasattr(self, "_in_edges") or len(self._in_edges) == 0:
            inEdges = {v:[] for v in self.vertices}
            for v, edges in self._out_edges.iteritems():
                for e in edges:
                    inEdges[e].append(v)
            self._in_edges = inEdges
        self._out_edges, self._in_edges = self._in_edges, self._out_edges        

    def dfs_recursive(self, source=None, \
                            preorderCallback=None, \
                            postorderCallback=None, \
                            doneVertices=None):
        """
        Performs a recursive depth-first-search on the graph starting from the 
        vertex "source", and returns the set of vertices that were visited.
        If source is unspecified, repeatedly performs DFS from unvisited 
        starting points until every vertex in the graph is visited.
        The pre- and post-order callbacks are invoked on each visited vertex, 
        at the appropriate times.
        """
        visited = set()
        if doneVertices is None: doneVertices = set()
        
        def _dfs_inner(source):
            if source in doneVertices:
                return
            if preorderCallback: preorderCallback(source)
            visited.add(source)
            doneVertices.add(source)
            for v in self._out_edges[source]:
                _dfs_inner(v)
            if postorderCallback: postorderCallback(source)        
        
        sources = [source] if source else self.vertices
        for v in sources:
            if v not in doneVertices:
                _dfs_inner(v)
        return visited

    def dfs_iterative(self, source=None, \
                            preorderCallback=None, \
                            postorderCallback=None, \
                            doneVertices=None):
        """
        Performs a DFS without using recursion. Useful for "deep" graphs.
        Parameters and return value are similar to dfs_recursive().
        """
        sources = self.vertices if source is None else [source]
        if doneVertices is None: doneVertices = set()
        visited = set()
        for src in sources:
            if src in doneVertices: continue
            visited.add(src)
            doneVertices.add(src)
            if preorderCallback: preorderCallback(src)
            stack = [src, None] + self._out_edges[src]
            while stack:
                v = stack.pop()
                if v is not None:
                    # We just popped off a 'child' vertex v for which the
                    # parent is still on the stack.
                    if v in doneVertices: continue
                    if preorderCallback: preorderCallback(v)
                    doneVertices.add(v)
                    visited.add(v)
                    stack.extend([v, None] + self._out_edges[v])
                else:
                    # We just popped off the 'None' flag to indicate that
                    # we are done with all children of some parent vertex,
                    # which now must be at the top of the stack.
                    v = stack.pop()
                    if postorderCallback: postorderCallback(v)
        return visited

    def tarjan_SCCs_recursive(self):
        """
        Recursive implementation of Tarjan's single-pass algorithm to find the 
        SCCs of the graph.
        Returns the SCCs as a list of sets.
        """
        SCCs = []
        sccStack = []
        dfsInfo = dict()
        
        def get_SCCs_inner(v):
            sccStack.append(v)
            dfsInfo[v] = [True, len(dfsInfo), len(dfsInfo)] # [on-stack, visit-index, ancestor-index]
            for e in self._out_edges[v]:
                if e not in dfsInfo:
                    # e not yet visited
                    get_SCCs_inner(e)
                    dfsInfo[v][2] = min( dfsInfo[v][2], dfsInfo[e][2] ) # update ancestor link
                elif dfsInfo[e][0]: 
                    # e is on sccStack (v -> e is a back-edge)
                    dfsInfo[v][2] = min( dfsInfo[v][2], dfsInfo[e][1] )
            _, vIndex, vAncestor = dfsInfo[v]
            if vIndex == vAncestor:
                # v is the root node of an SCC
                SCCs.append(self._tarjan_extract_scc(v, sccStack, dfsInfo))
            return
        
        for v in self.vertices:
            if v not in dfsInfo:
                get_SCCs_inner(v)
        return SCCs
    
    def tarjan_SCCs_iterative(self):
        """
        Iterative implementation of Tarjan's single-pass algorithm to find the 
        SCCs of the graph. Useful for "deep" graphs.
        Returns the SCCs as a list of sets.
        """
        SCCs = []
        dfsStack = []
        sccStack = []
        dfsInfo = dict()
        
        for v in self.vertices:
            if v in dfsInfo: continue
            dfsStack = [(None, v)]
            while dfsStack:
                stackEntry = dfsStack.pop()
                if stackEntry is None:
                    # We just got done with all the children of a vertex
                    parent, v = dfsStack.pop()
                    if dfsInfo[v][1] == dfsInfo[v][2]:
                        # v is the root of an SCC
                        SCCs.append(self._tarjan_extract_scc(v, sccStack, dfsInfo))
                    if parent is not None:
                        dfsInfo[parent][2] = min( dfsInfo[parent][2], \
                                                  dfsInfo[v][2] )
                    continue
                parent, v = stackEntry
                if v not in dfsInfo:
                    # v hasn't been visited
                    dfsInfo[v] = [True, len(dfsInfo), len(dfsInfo)]
                    sccStack.append(v)
                    dfsStack.extend( [(parent, v), None] + \
                                     [(v, e) for e in self._out_edges[v]] )
                elif dfsInfo[v][0]:
                    # v is on the sccStack (parent -> v is a back-edge)
                    dfsInfo[parent][2] = min( dfsInfo[parent][2], dfsInfo[v][1] )

        return SCCs

    @staticmethod
    def _tarjan_extract_scc(root, sccStack, dfsInfo):
        """
        Used internally by tarjan_SCCs_recursive() and tarjan_SCCs_iterative().
        Pops off vertices from sccStack until the "root" vertex is hit.
        Returns the set of popped vertices.
        """
        scc = set()
        while(True):
            s = sccStack.pop()
            dfsInfo[s][0] = False
            scc.add(s)
            if s == root:
                break
        return scc
        
    def topological_order(self):
        """
        Returns the list of vertices of the graph, sorted in a topological-order.
        """
        topoList = []
        cb = lambda v: topoList.append(v)
        self.dfs_iterative(postorderCallback=cb)
        topoList.reverse()
        return topoList
    
    def kosaraju_SCCs(self):
        """
        Computes the strongly-connected-components of the graph using
        Kosaraju's two-pass algorithm.
        Returns the SCCs as a list of sets.
        The list of SCCs is in topological-order wrt the "metagraph" of SCC-nodes.
        """
        done = set() # set of vertices already classified into SCCs
        SCCs = []
        vertex_order = self.topological_order()
        self.reverse_graph()        
        for v in vertex_order:
            if v in done:
                continue
            scc = self.dfs_iterative(v, doneVertices=done)
            SCCs.append(scc)
        self.reverse_graph()
        return SCCs

    def __repr__(self):
        return "Graph(|V|={}, |E|={})".format(self.num_vertices, self.num_edges)

if __name__ == "__main__":
    graph = Graph("tests/graph4.txt")
    print graph.kosaraju_SCCs()
