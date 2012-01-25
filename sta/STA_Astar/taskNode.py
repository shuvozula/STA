import sys
from coalitionNode import *

class taskNode:

    def __init__(self, taskName):
        self.taskName = taskName
        self.coalitionList = []
        
    def isTask(self, task):
        if (self.taskName == task):
            return True
        else:
            return False

    def addCoalition(self, coalition, bid):
        self.coalitionList.append(coalitionNode(coalition, bid))

    def getCoalitionList(self):
        return self.coalitionList