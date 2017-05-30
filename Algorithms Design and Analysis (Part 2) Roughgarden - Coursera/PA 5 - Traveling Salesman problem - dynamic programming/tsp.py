# -*- coding: utf-8 -*-
import math
import numpy as np
import itertools as it

#%%
def binomial(n,k):
    if n < k:
        return 0
    elif k == 0:
        return 1
    elif k > n/2:
        return binomial(n,n-k)
    else:
        res = 1    
        for div in xrange(1,k+1):
            res *= n
            res /= div
            n -= 1
        return res

#%%
def read_points_from(filename):
    points = []
    with open(filename, "r") as FILE:
        expected_num_points = int( FILE.readline().strip() )
        for line in FILE:
            tokens = line.split()
            if len(tokens) == 0:
                continue
            x,y = map(float, tokens)
            points.append((x,y))
    
    assert len(points) == expected_num_points
    return points

#%%
def index_for_subset(subset, skip_element=None):
    res = 0
    if skip_element is None:
        elements = iter(subset)
    else:
        elements = (e for e in subset if e != skip_element)
    for i,n in enumerate(elements, start=1):
        res += binomial(n-1,i)
    return res

def euclidean_distance(a,b):
    return math.sqrt( (a[0]-b[0])**2 + (a[1]-b[1])**2 )

def extract_optimal_path(distances, opt_table):
    assert(len(opt_table[-1]) == 1)
    n = len(opt_table[-1][0]) + 1
    assert(len(opt_table) == n)
    
    opt_length, pred = \
        min( it.starmap( lambda v,s: (s[0]+distances[v][0], v), \
                         it.izip(xrange(1,n+1), opt_table[-1][0]) ) )
    
    path = [0]
    subset = tuple(xrange(1,n))
    while(pred != 0):
        path.append(pred)
        row = index_for_subset(subset)
        col = subset.index(pred)
        s = len(subset)
        subset = tuple(x for x in subset if x != pred)
        pred = opt_table[s][row][col][1]
    path.append(0)
    
    return opt_length,list(reversed(path))

def held_karp(pts):
    n = len(pts)
    distances = \
        [ [euclidean_distance(pts[i],pts[j]) for j in xrange(n)] for i in xrange(n) ]
    for i in xrange(n):
        distances[i][i] = 0
    
    opt_table = [None for i in xrange(n)]
    # For subset_size=1
    opt_table[1] = [ [(distances[0][i],0)] for i in xrange(1,n) ]
    
    for subset_size in xrange(2,n):
        num_subsets = binomial(n-1, subset_size)
        curr_opt_sol = np.empty((num_subsets, subset_size), dtype=np.object)
        prev_opt_sol = opt_table[subset_size-1]
        
        for subset in it.combinations(xrange(1,n), subset_size):
            row = index_for_subset(subset)
            for col,end_pt in enumerate(subset):
                # Get smaller subset (by excluding the current end-pt being considered)
                intermediate_pts = (pt for pt in subset if pt != end_pt)
                # Build list of candidate-solutions to current subproblem
                # ie. Best TSP length through the intermediate-pts, ending at 'end_pt'
                intermediate_solutions = \
                    prev_opt_sol[index_for_subset(subset,skip_element=end_pt)]
                candidate_solutions = \
                    it.starmap(lambda v,sol: (sol[0] + distances[v][end_pt], v), \
                               it.izip(intermediate_pts, intermediate_solutions))
                curr_opt_sol[row][col] = min(candidate_solutions)
        
        opt_table[subset_size] = curr_opt_sol
    
    # We have an optimal 1-way tour through all vertices, 
    # now complete the tour and return total length.
    return extract_optimal_path(distances, opt_table)

#%%
def plot_points(ax, points, m):
    x,y = zip(*points)
    ax.plot(x,y,m)

def compute_path_length(path):
    return sum( it.starmap(euclidean_distance, it.izip(path, path[1:])) )
    
#%%
import sys
from numbers import Number
from collections import Set, Mapping, deque

try: # Python 2
    zero_depth_bases = (basestring, Number, xrange, bytearray)
    iteritems = 'iteritems'
except NameError: # Python 3
    zero_depth_bases = (str, bytes, Number, range, bytearray)
    iteritems = 'items'
    
def getsize_recursive(obj_0):
    """Recursively iterate to sum size of object & members."""
    def inner(obj, _seen_ids = set()):
        obj_id = id(obj)
        if obj_id in _seen_ids:
            return 0
        _seen_ids.add(obj_id)
        size = sys.getsizeof(obj)
        if isinstance(obj, zero_depth_bases):
            pass # bypass remaining control flow and return
        elif isinstance(obj, (tuple, list, Set, deque, np.ndarray)):
            size += sum(inner(i) for i in obj)
        elif isinstance(obj, Mapping) or hasattr(obj, iteritems):
            size += sum(inner(k) + inner(v) for k, v in getattr(obj, iteritems)())
        # Check for custom object instances - may subclass above too
        if hasattr(obj, '__dict__'):
            size += inner(vars(obj))
        if hasattr(obj, '__slots__'): # can have __slots__ with __dict__
            size += sum(inner(getattr(obj, s)) for s in obj.__slots__ if hasattr(obj, s))
        return size
    return inner(obj_0)
    
def estimate_size(N):
    sols = np.empty(N+1, dtype=object)
    for s in xrange(1,N):
        num_subsets = binomial(N-1,s)
        sols[s] = np.empty((num_subsets,s), dtype=object)
        for i in xrange(num_subsets):
            for j in xrange(s):
                sols[s][i][j] = (np.random.random()*1000, j)

    return sols

#%%






















