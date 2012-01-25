import sys

class treeNode:

    def __init__(self, name, coalition, robotsOnPath):
        self.name = name
        self.totalRevenue = 0
        self.parent = None
        self.children = []
        self.blocked = True
        self.heuristicVal = 0.0
        self.futureNodes = None
        self.winnerOnPath = False
        #- - - - - - - - - - - - - -
        self.coalition = coalition
        self.coalitionsOnPath = []
        self.robotsOnPath = robotsOnPath
        #- - - - - - - - - - - - - -
        self.memberOfTask = None
        self.tasksOnPath = [] # stores the list of tasks excluding task-levels taken up by dummy nodes
        self.allTasksOnPath = [] # stores the list of all the tasks that are used up on the current path 
        
        
        
        
        
