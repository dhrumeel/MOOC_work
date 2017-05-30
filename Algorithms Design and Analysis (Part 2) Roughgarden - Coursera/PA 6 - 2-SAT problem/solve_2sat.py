# -*- coding: utf-8 -*-
import os
import sys
sys.path.append(os.path.abspath("../../scc"))
from scc import Graph

#%%
def read_clauses_from(filename):
    clauses = []
    variables = set()
    with open(filename, "r") as FILE:
        expected_num_clauses = int(FILE.readline())
        for line in FILE:
            tokens = line.split()
            if len(tokens) == 0:
                continue
            a,b = map(int,tokens)
            if a == 0 or b == 0:
                raise ValueError("Variable labels should be non-zero.")
            variables.add(abs(a))
            variables.add(abs(b))
            clauses.append((a,b))
            
    assert expected_num_clauses == len(clauses)
    return variables, clauses
        
#%%
def generate_implication_graph(variables, clauses):
    graph = Graph()
    graph_edges = []
    for a,b in clauses:
        graph_edges.append((-a,b))
        graph_edges.append((-b,a))
    graph.add_graph_data(graph_edges)
    
    return graph
    
#%%
def solve_2sat(variables, clauses):
    graph = generate_implication_graph(variables, clauses)
    assignment = dict()
    sccs = graph.kosaraju_SCCs()
    for scc in reversed(sccs):
        for literal in scc:
            if -literal in scc:
                print "UNSAT"
                return None
            if abs(literal) in assignment:
                continue
            if literal > 0:
                assignment[literal] = True
            else:
                assignment[-literal] = False
    
    print "SAT"
    
    return assignment
    
#%%

        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        