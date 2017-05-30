# -*- coding: utf-8 -*-

"""
Functions to sort a list using mergesort, and count number of inversions.
"""

def _countAndMerge(left, right, _cmp):
    merged = []
    (lLength, rLength) = (len(left), len(right))
    (lIdx, rIdx) = (0, 0)
    count = 0

    while True:
        if(lIdx == lLength): 
            merged.extend(right[rIdx:])
            break
        if(rIdx == rLength): 
            merged.extend(left[lIdx:])
            break

        if ( _cmp(left[lIdx], right[rIdx]) <= 0 ):
            merged.append(left[lIdx])
            lIdx += 1
        else:
            merged.append(right[rIdx])
            rIdx += 1
            count += (lLength - lIdx)

    return(count, merged)


def countInversionsAndSort(inputlist, _cmp=cmp):
    """
    Given an input list, return a tuple (inversion-count, sortedList)
    """
    inputLength = len(inputlist)
    if(inputLength <= 1): return (0, inputlist)

    mid = inputLength // 2

    (lInversions, lSorted) = \
        countInversionsAndSort(inputlist[:mid], _cmp)
    (rInversions, rSorted) = \
        countInversionsAndSort(inputlist[mid:], _cmp)
    (splitInversions, fullSorted) = \
        _countAndMerge(lSorted, rSorted, _cmp)

    return (splitInversions + lInversions + rInversions, fullSorted)

