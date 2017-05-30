# -*- coding: utf-8 -*-
import mergesort
import quicksort

def readListFromFile(file):
    """
    Read and return a list of integers from the specified file.
    Integers should be separated by whitespace in the file.
    """
    with open(file, "r") as FILE:
        return map(int, FILE.read().split())

class CountCompares:
    count = 0
    
    @classmethod
    def reset(cls):
        cls.count = 0
    
    def __init__(self, value):
        self.value = value
    
    def __lt__(self, other):
        CountCompares.count += 1
        return self.value < other
    
    def __gt__(self, other):
        CountCompares.count += 1
        return self.value > other
    
    def __le__(self, other):
        CountCompares.count += 1
        return self.value <= other
    
    def __ge__(self, other):
        CountCompares.count += 1
        return self.value >= other
    
    def __eq__(self, other):
        CountCompares.count += 1
        return self.value == other
    
    def __ne__(self, other):
        CountCompares.count += 1
        return self.value != other
    
    def __str__(self):
        return str(self.value)
    
    def __repr__(self):
        return self.__str__()


