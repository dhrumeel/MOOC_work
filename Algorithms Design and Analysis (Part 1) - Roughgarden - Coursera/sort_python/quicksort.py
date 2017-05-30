# -*- coding: utf-8 -*-
import random

def _median3(arr, i, j, k):
    a, b, c = arr[i], arr[j], arr[k]

    if(a > b):
        if(a > c):
            return j if (b > c) else k
        else:
            return i
    else:
        if(b > c):
            return i if (a > c) else k
        else:
            return j


def _pickPivot(arr, start, end):
    # arr[start], arr[end-1] = arr[end-1], arr[start]
    # midIdx = (end + start - 1) // 2
    # m = _median3(arr, start, midIdx, end-1)
    m = random.randrange(start, end)
    arr[start], arr[m] = arr[m], arr[start]
    return arr[start]


def _alternate_partition(arr, start, end):
    pivot = _pickPivot(arr, start, end)
    l = start+1
    for r in range(start+1, end):
        if arr[r] < pivot:
            arr[l], arr[r] = arr[r], arr[l]
            l += 1
    
    arr[start], arr[l-1] = arr[l-1], arr[start]
    
    return (l-1)


def _partition(arr, start, end):
    pivot = _pickPivot(arr, start, end)
    # The array is partitioned into 4 parts:
    # Pivot, Left-half, Unclassified, Right-half
    l = start+1 # end of Left-half
    r = end-1   # one to the left of Right-half
    
    while l <= r: 
        if arr[l] < pivot:
            l += 1
        else:
            arr[l], arr[r] = arr[r], arr[l]
            r -= 1

    arr[start], arr[r] = arr[r], arr[start]
    return r # position of the pivot


def _qsort(arr, start, end):
    length = (end - start)
    if(length <= 1): return
    
    pivotIdx = _partition(arr, start, end)
    
    _qsort(arr, start, pivotIdx)
    _qsort(arr, pivotIdx+1, end)


def quicksort(arr):
    """
    Sort list 'arr' using quicksort (in-place).
    """
    return _qsort(arr, 0, len(arr))

