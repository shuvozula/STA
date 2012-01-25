import sys

class coalitionNode:

    def __init__(self, coalition, bid):
        self.coalition = coalition
        self.bid = bid
        
    def getCoalition(self):
        return self.coalition

    def getBid(self):
        return self.bid
