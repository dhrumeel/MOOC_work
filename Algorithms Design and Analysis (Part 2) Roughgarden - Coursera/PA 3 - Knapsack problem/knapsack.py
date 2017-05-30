# -*- coding: utf-8 -*-

from collections import namedtuple

Item = namedtuple("Item", ("value", "weight"))
TableEntry = namedtuple("TableEntry", ("value","pick"))

#%%
def read_from(filename):
    items = []
    with open(filename, "r") as FILE:
        knapsack_size, num_items = [int(x) for x in FILE.readline().split()]
        for line in FILE:
            l = line.split()
            if len(l) == 0:
                continue
            val, wt = [int(x) for x in l]
            items.append(Item(value=val, weight=wt))

        assert(len(items) == num_items)
        return knapsack_size, items

#%%
def knapsack_optimal_value(capacity, items):
    i_val, i_wt = items[0]
    optimal_values = [0] * i_wt + [i_val] * (capacity+1-i_wt)
    
    for (i_val, i_wt) in items[1:]:
        for cap in xrange(capacity, i_wt-1, -1):
            optimal_values[cap] = max( (i_val + optimal_values[cap-i_wt]), \
                                       optimal_values[cap] )
    
    return optimal_values[capacity]
    
#%%
def knapsack_recursive(capacity, items):
    cache = [dict() for i in xrange(len(items))]

    def opt_value(cap, i):
        if cap <= 0 or i < 0:
            return 0
        try:
            return cache[i][cap]
        except KeyError:
            i_val, i_wt = items[i]
            result = opt_value(cap, i-1)
            if i_wt <= cap:
                result = max( i_val + opt_value(cap-i_wt, i-1), \
                              result )
            cache[i][cap] = result
            return result
        
    result = opt_value(capacity, len(items)-1)
    print "Cache size is ", sum([len(d) for d in cache])
    
    return result
    
#%%
def extract_solution(capacity, items, optimal_table):
    selected_items = []
    item_idx = len(items)-1
    while capacity > 0 and item_idx >= 0:
        sol = optimal_table[item_idx][capacity]
        if sol.pick == True:
            selected_items.append(items[item_idx])
            capacity = capacity - items[item_idx].weight
        item_idx = item_idx-1
    
    return selected_items
    
def knapsack_solve(capacity, items):
    num_items = len(items)
    # Table of optimal solutions to smaller subproblems
    # Each table entry [i][j] is a tuple (V, P) where:
    # V is the optimal value that can be packed into a knapsack with
    # capacity j, using only the items 0->i
    # P is True if item i should be selected to achieve the optimal 
    # value V for subproblem [i][j]
    opt_table = [[None]*(capacity+1) for i in xrange(num_items)]
    
    # Base-cases: Item 0
    i_val, i_wt = items[0]
    opt_table[0] = [TableEntry(value=0, pick=False)]*i_wt + \
                   [TableEntry(value=i_val, pick=True)]*(capacity+1-i_wt)
    
    # Fill the table
    for i in xrange(1,num_items):
        i_val, i_wt = items[i]

        # If knapsack-capacity < weight, don't pick item i
        for c in xrange(i_wt):
            opt_table[i][c] = TableEntry(value=opt_table[i-1][c].value, \
                                         pick=False)
        
        for c in xrange(i_wt, capacity+1):
            # optimal value achievable if item i is selected
            value_select = i_val + opt_table[i-1][c-i_wt].value
            # optimal value achievable if item i is dropped
            value_drop = opt_table[i-1][c].value
            if value_drop > value_select:
                opt_table[i][c] = TableEntry(value=value_drop, pick=False)
            else:
                opt_table[i][c] = TableEntry(value=value_select, pick=True)
    
    return opt_table[num_items-1][capacity].value, \
           extract_solution(capacity, items, opt_table)
    
#%%
def knapsack_greedy(capacity, items):
    sort_key = lambda item: float(item.value)/item.weight
    selected_items = []
    total_value = 0
    for item in sorted(items, key=sort_key, reverse=True):
        if capacity - item.weight < 0:
            continue
        selected_items.append(item)
        capacity -= item.weight
        total_value += item.value
    
    return total_value, selected_items



#%%



































            