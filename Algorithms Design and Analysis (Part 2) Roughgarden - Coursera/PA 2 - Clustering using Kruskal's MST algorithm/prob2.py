# -*- coding: utf-8 -*-

import sys
import os
sys.path.append(os.path.abspath("../../unionfind"))
from unionfind import UnionFind
from collections import defaultdict
import itertools

 #%%
def readFile(filename):
    labels = []
    with open(filename, "r") as FILE:
        num_labels, num_bits = (int(x) for x in FILE.readline().split())
        for line in FILE:
            s = "".join(line.split())
            if len(s) > 0:
                assert( len(s) == num_bits )
                labels.append( int(s, 2) )
        
        assert( len(labels) == num_labels )
    return (num_bits, labels)
    
#%%
def countOnes(n):
    count = 0
    while(n):
        n &= (n-1)
        count += 1
    return count

#%%
def hammingDistance(a, b):
    return countOnes(a ^ b)

#%%
def prob2_new(filename):
    num_bits, labels = readFile(filename)
    
    labels = set(labels)
    uf = UnionFind(labels)
    
    print "After clustering labels with dist=0: {} clusters exist.".format(uf.num_disjoint_sets,)
    
    # For each label, look for potential labels at dist=1
    flip_masks = [(1<<s) for s in xrange(num_bits)]
    for label in labels:
        for flip_mask in flip_masks:
            potential_nbor = (label ^ flip_mask)
            if potential_nbor in labels:
                uf.union(label, potential_nbor)
                
    print "After clustering labels with dist=1: {} clusters exist.".format(uf.num_disjoint_sets,)
    
    # For each label, look for potential labels at dist=2
    flip_masks = [ (1 << t[0] | 1 << t[1]) for t in \
                      itertools.combinations(range(num_bits), 2) ]
    for label in labels:
        for flip_mask in flip_masks:
            potential_nbor = (label ^ flip_mask)
            if potential_nbor in labels:
                uf.union(label, potential_nbor)
                
    print "After clustering labels with dist=2: {} clusters exist.".format(uf.num_disjoint_sets,)
    
    return uf.num_disjoint_sets

#%%
def prob2(filename):
    num_bits, labels = readFile(filename)
    
    labels = set(labels)
    uf = UnionFind(labels)
    
    print "After clustering labels with dist=0: {} clusters exist.".format(uf.num_disjoint_sets,)
    
    # Group labels by number-of-ones
    group_for_ones = defaultdict(list)
    for label in labels:
        group_for_ones[countOnes(label)].append(label)
    
    for idx,a in enumerate(labels):
        num_ones = countOnes(a)
        for b in itertools.chain(*[iter(group_for_ones[i]) \
                                     for i in xrange(num_ones-1, num_ones+2)]):
            if uf.find_root(a) != uf.find_root(b) and \
               hammingDistance(a, b) <= 1:
                   uf.union(a, b)
        if idx == 1000:
            return uf.num_disjoint_sets

    print "After clustering labels with dist=1: {} clusters exist.".format(uf.num_disjoint_sets,)    
    
    for idx,a in enumerate(labels):
        num_ones = countOnes(a)
        print "Finding neighbors at dist=2 for label with {} ones".format(num_ones,)
        for b in itertools.chain(*[iter(group_for_ones[i]) \
                                     for i in xrange(num_ones-2, num_ones+3)]):
            if uf.find_root(a) != uf.find_root(b) and \
               hammingDistance(a, b) <= 2:
                   uf.union(a, b)
    
    print "After clustering labels with dist=2: {} clusters exist.".format(uf.num_disjoint_sets,)
    
    return uf.num_disjoint_sets
    
    