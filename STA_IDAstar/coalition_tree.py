
__author__ = 'Spondon Saha'

import time
import sys
from treeNode import treeNode
from coalitionnode import CoalitionNode


class CoalitionTree:
    """Contains the core logic for the STA IDA* algorithm."""

    def __init__(self, coalitionsByTasksList, screenDump):
        """Constructor.

        Arguments:
            coalitionsByTasksList: A list of taskNode"""
        self.coalitionsByTasksList = coalitionsByTasksList
        self.root = treeNode("root", [], []) # name, coalition, onPath
        self.root.blocked = False
        self.orderOfTasks = []
        self.bestRevenue = 0
        self.bestPartition = None
        self.chosenTasks = []
        
        # A-star variables
        self.nodeHeuristics = [] # used for collecting all the heuristics for each node for a particular task level
        self.leaves = [] # used for collecting all the leaf nodes
        self.winnerNode = None
        
        # f-limit for use in the IDA-star algorithm 
        self.fLimit = 0.0 # we are trying to maximize our revenue, hence the f-limit starts at zero
        
        # declarations below used for statistical data collection
        self.nodecount = 0
        self.dummyNodeCount = 0
        self.regularNodeCount = 0
        self.dummyTime = 0.0
        self.regularTime = 0.0
        
        # enable/disable print
        self.screenDump = screenDump

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
       
    def printit(self, msg):
        if self.screenDump == True:
            print msg

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    
    def hasMember(self, c1, c2):

        for elem in c2:
            if (c1.count(elem) > 0):
                return True

        return False
    
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    def displayWinner(self):

        self.printit("")
        self.printit("WINNING COALITIONS AND TASKS")
        self.printit("")
        self.printit("Winning coalitions --> " + str(self.winnerNode.coalitionsOnPath))
        self.printit("Respective tasks   --> " + str(self.winnerNode.tasksOnPath))
        self.printit("Revenue fetched    --> " + str(self.winnerNode.totalRevenue))

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    def constructTree(self):

        # START BUILDING THE TREE
        self.printit("-------------------------------------------------------------")
        self.printit("<<<<<<<<<<<<<<<< CONSTRUCTING COALITION TREE >>>>>>>>>>>>>>>>")
        self.printit("-------------------------------------------------------------")

        #taskList = self.getOrderOfTasks()
        #lastTask = self.coalitionsByTasksList[len(self.coalitionsByTasksList) - 1].taskName
        solutionFound = False
        winners = []
        taskList = []
        g = 0
        
        while not solutionFound:
            
            self.printit("     -- Going Depth First --> " + str(self.root.name))
            winners, selectedTasks, new_f = self.DFS_Contour(self.root, self.coalitionsByTasksList, winners, taskList, 0) # (root, F, winners, task-list, g)
            self.printit("     -- Coming out of Depth First...")
            if winners:
                solutionFound = True
            else:
                self.printit("     -- Updating fLimit = " + str(self.fLimit))
                self.fLimit = new_f # update the flimit to the next highest revenue value
        
        self.printit("-------------------------------------------------------------")
        self.printit("<<<<<<<<<<< CONSTRUCTING COALITION TREE COMPLETED >>>>>>>>>>>")
        self.printit("-------------------------------------------------------------")
        
        self.printit("")
        self.printit("WINNING COALITIONS AND TASKS")
        self.printit("")
        self.printit("Winning coalitions --> " + str(winners))
        self.printit("Respective tasks   --> " + str(selectedTasks))
        self.printit("Revenue fetched    --> " + str(new_f))
        self.printit("Visited States     --> " + str(self.nodecount))
        
        output = []
        output.append(str(winners))
        output.append(str(selectedTasks))
        output.append(str(new_f))
        output.append(self.nodecount)
        
        return output

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    def DFS_Contour(self, node, CBTList, winners, taskList, g):
        
        self.printit("------------------------------------------------------")
        self.printit("    -- Estimating heuristic for node '" + str(node.name) + "'")
        hF = self.estimateHeuristic(node.coalitionsOnPath, node.allTasksOnPath, 0)
        self.printit("    -- Heuristic for node '" + str(node.name) + "' is '" + str(hF) + "'")
        
        self.printit("    <** f-limit = " + str(self.fLimit) + ", (g + hF) = " + str((g + hF)) + " **>")
        
        # pruning
        if (g + hF) < self.fLimit:
            self.printit("    (g + hF) is < f-limit....pruning.....")
            return [], [], (g + hF)
        else:
            self.printit("    (g + hF) is >= f-limit....go deeper.....")
        
        # check if there are any more tasks to handle, then get eligible children
        if CBTList:
            children = self.getEligibleChildren(CBTList[0].getCoalitionList(), node.robotsOnPath) # gets the list of children that are not repeated on the current path
        else:
            self.printit("    End of a path reached. f-Limit = " + str(self.fLimit))
            self.printit("    End of a path reached. Winners = " + str(winners) + " and g = '" + str(g) + "'")
            self.printit("    -- updating f-limit from '" + str(self.fLimit) + "' to '" + str(g) + "'")
            self.fLimit = g # revert to branch and bound once the first leaf is reached
            return winners, taskList, g
        
       # if there are any eligible children for the current path, then add dummy node and prepare for DFS
        if children or (not children and (len(CBTList) > 1)):            
            taskName = CBTList[0].taskName
            if (len(CBTList) > 1): # add a dummy node if the children do not belong to the last task
                self.printit("    -- Adding Dummy node to the list of children...")
                dummy = coalitionNode([], 0)
                children.append(dummy) # add the dummy node
            self.printit("    Children to be added to '" + str(node.name) + "' are " + str(map(lambda(x): x.getCoalition(), children)))
        else: # end of path reached
            self.printit("    End of a path reached. f-Limit = " + str(self.fLimit))
            self.printit("    End of a path reached. Winners = " + str(winners) + " and g = '" + str(g) + "'")
            self.printit("    -- updating f-limit from '" + str(self.fLimit) + "' to '" + str(g) + "'")
            self.fLimit = g # revert to branch and bound once the first leaf is reached
            return winners, taskList, g
        
        # initialize recursion parameters
        maxRevenue = 0
        bestWinners = []
        listOfTasks = []
        next_f = 0
        
        # for each child in children, recursively inspect using heuristics to see if the path is feasible as per f-limit
        for child in children:
            self.printit("        - - - - - - - - - - - - - - - - - - - - - - ")
            self.printit("        -- Adding child node: " + str(child.getCoalition()) + " to coalition " + str(node.name))
            
            self.nodecount += 1
            self.printit("        -- VISITING NEW STATE " + str(child.getCoalition()))
            childNode = self.addChild(node, child, taskName) # add a child node and return it's instance
            solution, tasks, new_f = self.DFS_Contour(childNode, CBTList[1:], winners + [child.getCoalition()] , taskList + [taskName], g + int(child.getBid())) # recursively inspect the current child
            
            self.printit("        -- returning from DFS contour to node " + str(node.name) + "....")
            
            if solution and (new_f > maxRevenue):
                self.printit("        ** updating maxRevenue from '" + str(maxRevenue) + "' to '" + str(new_f) + "'")
                self.printit("        ** updating bestWinners from '" + str(bestWinners) + "' to '" + str(solution) + "'")
                maxRevenue = new_f
                bestWinners = solution
                listOfTasks = tasks
            else:
                self.printit("        ** NO NEED TO UPDATE: solution = '" + str(solution) + "', maxRevenue = '" + str(maxRevenue) + "', new_f = '" + str(new_f) + "'")
                
            self.printit("        $$ updating next_f from '" + str(next_f) + "' to '" + str(new_f) + "'")
            next_f = max(next_f, new_f)
            
        if bestWinners:
            return bestWinners, listOfTasks, maxRevenue
        else:
            return [], [], next_f
            
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
     
    def getEligibleChildren(self, currentChildren, robotsOnPath):
        
        eligibleCoalitions = []
        
        for child in currentChildren:
            if not self.hasMember(robotsOnPath, child.getCoalition()):
                eligibleCoalitions.append(child)
                
        return eligibleCoalitions
    
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    
    def addChild(self, parentNode, child, taskName):
        
        # fetch the child coalition and bid value from the coalitionNode object
        coalition = child.getCoalition()
        bidValue = child.getBid()
        
        if coalition: # its a regular coalition with a positive bid value
            childNode = treeNode(str(coalition), coalition, parentNode.robotsOnPath + coalition) # name, coalition, robotsOnPath
            childNode.parent = parentNode
            childNode.coalitionsOnPath = parentNode.coalitionsOnPath[:] # deep copy the entire list
            childNode.coalitionsOnPath.append(coalition) # --> extra operation than DUMMY
            childNode.totalRevenue = int(parentNode.totalRevenue) + int(bidValue)
            childNode.tasksOnPath = parentNode.tasksOnPath[:] # deep copy the entire list
            childNode.tasksOnPath.append(taskName) # --> extra operation than DUMMY
            childNode.memberOfTask = taskName
            childNode.allTasksOnPath = parentNode.allTasksOnPath[:]
            childNode.allTasksOnPath.append(taskName)
            #parentNode.children.append(childNode) # add the child node as a child of the parent node
            return childNode
        else: # its a dummy node with an empty coalition set and a zero bid value
            dummyNode = treeNode("dummy", [], parentNode.robotsOnPath)
            dummyNode.parent = parentNode
            dummyNode.coalitionsOnPath = parentNode.coalitionsOnPath[:]
            dummyNode.totalRevenue = parentNode.totalRevenue
            dummyNode.tasksOnPath = parentNode.tasksOnPath
            dummyNode.memberOfTask = taskName
            dummyNode.allTasksOnPath = parentNode.allTasksOnPath[:]
            dummyNode.allTasksOnPath.append(taskName)
            return dummyNode
    
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    def estimateHeuristic(self, coalitionsOnPath, allTasksOnPath, totalRevenue):
    #===============================================================================
    # hF = sum of greatest contribution from coalitions of each task, that are not
    #      overlapping with the rest of the coalitions already in the path
    #===============================================================================
        g = float(totalRevenue)
        #hF = 0.0
        
        heurCBTList = []
        
        # populate 'heurCBTList' with all elements from 'self.coalitionsByTasksList' that are
        # not in 'allTasksOnPath'
        # Explanation: Get all taskNodes that have not been covered so far
        for taskNode in self.coalitionsByTasksList:
            if (self.hasMember(taskNode.taskName.split(' '), allTasksOnPath) == False):
                heurCBTList.append(taskNode)
        
        # build list of robots that are in heurCBTList
        robotsAheadInPath = []
        cNodesAheadInPath = []
        for tNode in heurCBTList:
            listOfCoalitions = tNode.getCoalitionList()
            for cNode in listOfCoalitions:
                robotsAheadInPath += cNode.getCoalition() # adds the elements of the list instead of the list-object
                cNodesAheadInPath.append(cNode) # adds it as a list-object to cNodesAheadInPath
        
        # remove duplicates: bench-marked the fastest, look --> http://www.peterbe.com/plog/uniqifiers-benchmark
        robotsAheadInPath = {}.fromkeys(robotsAheadInPath).keys() 
        
        # now iterate by each robot and pick all coalitions
        hF = 0.0
        for robot in robotsAheadInPath:
            MaxHolder = []
            for cNode in cNodesAheadInPath:
                coalition = cNode.getCoalition()
                # if the robot is a member of the current coalition, then proceed
                if (self.hasMember(coalition, [robot])):
                    # check if the coalition has any robots that are previously in the path 
                    onPath = False
                    for c in coalitionsOnPath: 
                        if (self.hasMember(coalition, c)):
                            onPath = True
                            break
                    # if not, then collect its heuristic
                    if not onPath: 
                        heuristic = float(cNode.getBid()) / len(cNode.getCoalition()) # sandholm's heuristic 3.1, equation (23)
                        MaxHolder.append(heuristic)
            
            if len(MaxHolder) > 0:
                hF += max(MaxHolder)
            
        # collect the heuristics for each node belonging to each task
##        self.nodeHeuristics.append(g + hF)
##        self.leaves.append(node)
        
        return (g + hF)
    
