import sys

class treeNode:

    def __init__(self, name, coalition, hasOnPath):
        self.name = name
        self.coalition = coalition
        self.hasOnPath = hasOnPath
        self.children = []
        #- - - - - - - - - - - - - -
        self.coalitionsOnPath = []
        self.totalRevenue = 0
        self.tasksOnPath = []
        

    
