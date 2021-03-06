import sys, time
from treeNode import *

class coalitionTree:

    def __init__(self, coalitionsByTasksList, screenDump):
        self.coalitionsByTasksList = coalitionsByTasksList
        self.root = treeNode("root", [], []) # name, coalition, onPath
        self.root.blocked = False
        self.orderOfTasks = []
        self.bestRevenue = 0
        self.bestPartition = None
        self.chosenTasks = []
        
        # purely A-star DSs
        self.nodeHeuristics = [] # used for collecting all the heuristics for each node for a particular task level
        self.leaves = [] # used for collecting all the leaf nodes
        self.winnerNode = None
        self.unexpandedWinnerNodesPresent = False
        
        # declarations below used for statistical data collection
        self.nodecount = 0
        self.dummyNodeCount = 0
        self.regularNodeCount = 0
        self.dummyTime = 0.0
        self.regularTime = 0.0
        
        # enable/disable print
        self.screenDump = screenDump

    def getOrderOfTasks(self):
        
        taskList = []
        for tNode in self.coalitionsByTasksList:
            taskList.append(tNode.taskName)
        return taskList
            
    def getTaskNode(self, taskName):
        
        for tNode in self.coalitionsByTasksList:
            if (tNode.taskName == taskName):
                return tNode
            
    def printit(self, msg):
        if self.screenDump == True:
            print msg

    def IsWinnerNode(self, ptr):
        
        if (self.winnerNode.parent == ptr.parent) and \
           (self.winnerNode.name == ptr.name) and \
           (self.winnerNode.totalRevenue == ptr.totalRevenue) and \
           (self.winnerNode.memberOfTask == ptr.memberOfTask):
            return True
        else:
            return False

    def hasMember(self, c1, c2):

        for elem in c2:
            if (c1.count(elem) > 0):
                return True

        return False

    def trackWinner(self, revenue, coalitionsOnPath, tasksOnPath):

        if (revenue > self.bestRevenue):
            self.printit("        << Highest revenue so far : '" + str(revenue) + "', from partition : " + str(coalitionsOnPath) + " >>")
            self.bestRevenue = revenue
            self.bestPartition = coalitionsOnPath
            self.chosenTasks = tasksOnPath
        else:
            self.printit("        << Revenue of '" + str(revenue) + "' still < highest revenue '" + str(self.bestRevenue) + "' >>")

    def determineWinner(self):

        self.printit("")
        self.printit("WINNING COALITIONS AND TASKS")
        self.printit("")
        self.printit("Winning coalitions --> " + str(self.winnerNode.coalitionsOnPath))
        self.printit("Respective tasks   --> " + str(self.winnerNode.tasksOnPath))
        self.printit("Revenue fetched    --> " + str(self.winnerNode.totalRevenue))

    def constructTree(self):

        # START BUILDING THE TREE
        self.printit("-------------------------------------------------------------")
        self.printit("<<<<<<<<<<<<<<<< CONSTRUCTING COALITION TREE >>>>>>>>>>>>>>>>")
        self.printit("-------------------------------------------------------------")

        # keep looping until we have found the node with the highest revenue that has no more child nodes to add
        # this node then alternatively would have a heuristic value (h) of zero (no more children on path)
        # this node would also have the highest revenue (g+h) --> self.heuristicVal
                
        taskList = self.getOrderOfTasks()
        lastTask = self.coalitionsByTasksList[len(self.coalitionsByTasksList) - 1].taskName
        solutionFound = False
        taskIndex = -1
        
        while not solutionFound:
            
            # determine if end condition has been met
            if self.winnerNode is not None:
                if (self.winnerNode.totalRevenue == self.winnerNode.heuristicVal): # and # if there are no children on path, then total revenue = g + hF (heuristicVal)
                    #(self.unexpandedWinnerNodesPresent == False)): 
                    solutionFound = True
            
            # get children for current task level
            if not solutionFound:
                
                # get the correct taskIndex
                if (self.winnerNode is not None):
                    taskIndex = taskList.index(self.winnerNode.memberOfTask) + 1
                    if (taskIndex == len(taskList)):
                        taskIndex -= 1
                else:
                    taskIndex += 1
                
                # get the taskNode
                taskNode = self.getTaskNode(taskList[taskIndex])
                
                self.printit("^^^^^^^^^^^^^^^^^^^")
                self.printit("^^^^^ TASK " + str(taskNode.taskName) + " ^^^^^")
                self.printit("^^^^^^^^^^^^^^^^^^^")
                
                self.printit("Adding coalition nodes: ")
                coalitionNodes = taskNode.getCoalitionList()
                for cNode in coalitionNodes:
                    self.printit("    " + str(cNode.getCoalition()))
                
                # if it's the last task, then don't add dummy nodes
                if (taskIndex == (len(taskList) - 1)): 
                    self.addNodes(self.root, coalitionNodes, taskNode.taskName, False) # don't add dummy nodes
                else:
                    self.addNodes(self.root, coalitionNodes, taskNode.taskName, True) # add dummy nodes


                # =======================================================================================================
                # now sort the heuristics in decreasing order for each node that has been added in the last step
                self.printit("        << SORTING HEURISTICS FOR RECENTLY ADDED NODES >>")
                
                # sort the list of heuristics in descending order. The first element will have the highest heuristic
                # basically going for the path with the highest heuristic
                # we want to overestimate the heuristic.
                #self.nodeHeuristics.sort(lambda x, y: cmp(y, x))
                self.leaves.sort(lambda x, y: cmp(y.heuristicVal, x.heuristicVal))
                
                self.printit("        " + str(map(lambda a: a.name, self.leaves)))
                self.printit("        " + str(map(lambda a: a.heuristicVal, self.leaves)))
                self.printit("        << HIGHEST HEURISTIC FOUND: " + str(self.leaves[0].heuristicVal) + " >>")
                self.printit("        << -- nodes in current task & heuristics: >>")
                
                # now we know which path is the best to take to add nodes on, so lets block the other ones.
                self.winnerNode = None
##                self.unexpandedWinnerNodesPresent = False
                self.assignBlocksOnPath(self.root, taskNode.taskName)
                
                self.printit("        << DONE BLOCKING PATHS >>")
                
                self.printit( "        WINNER NODE IS ---->>>> " + str(self.winnerNode.name) + ", " + \
                                                                   str(self.winnerNode.heuristicVal) + ", " + \
                                                                   str(self.winnerNode.memberOfTask))
                                                    
                self.printit("        LEAVES ARE:")
                for leaf in self.leaves:
                    self.printit("            " + str(leaf.name) + ", " + str(leaf.heuristicVal))
                
##                self.nodeHeuristics = [] # empty the heuristics for next round
##                self.leaves = []
                self.printit("-------------------------------------------------------------")

                # =======================================================================================================                
                

        self.printit("Order of Tasks: " + str(taskList))

        self.printit("-------------------------------------------------------------")
        self.printit("<<<<<<<<<<< CONSTRUCTING COALITION TREE COMPLETED >>>>>>>>>>>")
        self.printit("-------------------------------------------------------------")
        self.printit("Done adding nodes....")

        output = []
        output.append(self.nodecount)
        output.append(self.dummyNodeCount)
        output.append(self.regularNodeCount)
        output.append(self.dummyTime)
        output.append(self.regularTime)
        output.append(str(self.winnerNode.coalitionsOnPath))
        output.append(str(self.winnerNode.tasksOnPath))
        output.append(str(self.winnerNode.totalRevenue))
        return output


    def assignBlocksOnPath(self, node, taskName):
        # recursively travel down the tree and get the heuristics from each node with the specified taskName

        hasWinnerOnPath = False
        
        if (len(node.children) == 0):

##            if (node.name != "root"):
##                self.nodeHeuristics.append(node.heuristicVal)
##                self.leaves.append(node)
            
            if (node.heuristicVal == self.leaves[0].heuristicVal):
                node.blocked = False
                node.winnerOnPath = True
                self.printit("        --     [" + str(node.name) + ", +$" + str(node.heuristicVal) + "]")
                self.printit("       << PATH WITH NODE-NAME [" + str(node.name) + "] HAS THE HIGHEST g+h (" + str(node.heuristicVal) + "), AND REVENUE IS (" + str(node.totalRevenue) + "), UNBLOCKING PATH >>")

                # keep track of the winner
                self.winnerNode = node

                # keep track of any winnerNode that is unexpanded; only in the case of multiple winner nodes
##                if (node.totalRevenue is not node.heuristicVal):
##                    self.unexpandedWinnerNodesPresent = True

                return True
                
            else:
                self.printit("        --     [" + str(node.name) + ", +$" + str(node.heuristicVal) + "]")
                node.blocked = True
                
                return False
        
        else:
            #print "Node: " + str(node.name)
            for child in node.children:
                
                # reset the winnerOnPath flag
                child.winnerOnPath = False
                
                # recursively look into children
                hasWinnerOnPath = self.assignBlocksOnPath(child, taskName) # recursive call
                
                # if winner(s) is on path, set flag
                if (node.winnerOnPath is False):
                    node.winnerOnPath = hasWinnerOnPath
                
        return node.winnerOnPath
    

    def addNodes(self, ptr, cNodes, taskName, addDummy, nodesOnPath = []):

        if ((ptr.name == "root") and (len(ptr.children) == 0)):

            # add the set of coalitions to the root node
            self.printit("    Adding Nodes to root....")
            for cn in cNodes:
                coalition = cn.getCoalition()
                
                start = time.time() # start time
                tN = treeNode(str(coalition), coalition, coalition) # name, coalition, robotsOnPath
                tN.parent = ptr
                tN.coalitionsOnPath.append(coalition)
                tN.totalRevenue = int(cn.getBid())
                tN.tasksOnPath.append(taskName)
                tN.memberOfTask = taskName
                tN.allTasksOnPath.append(taskName)
                tN.blocked = False
                tN.hasWinnerOnPath = True
                #---------------------------------------------------------------------------------------------
                # determine the heuristic - used exclusively for A*
                tN.heuristicVal, tN.futureNodes = self.estimateHeuristic(tN, tN.coalitionsOnPath, tN.allTasksOnPath, tN.totalRevenue)
##                self.nodeHeuristics.append(tN.heuristicVal)
                self.leaves.append(tN)
                #---------------------------------------------------------------------------------------------
                self.root.children.append(tN)
                end = time.time() # end time
                
                self.trackWinner(tN.totalRevenue, tN.coalitionsOnPath, tN.tasksOnPath)
                
                self.regularTime += (end - start)
                self.regularNodeCount += 1
                self.nodecount += 1

            # add dummy node
            self.printit("    Adding dummy node to node '" + str(ptr.name) + "'....")
            start = time.time() # start time
            tN = treeNode("dummy", [], []) # name, coalition, robotsOnPath
            tN.parent = ptr
            tN.memberOfTask = taskName
            tN.allTasksOnPath.append(taskName)
            #---------------------------------------------------------------------------------------------
            # determine the heuristic - used exclusively for A*
            tN.heuristicVal, tN.futureNodes = self.estimateHeuristic(tN, tN.coalitionsOnPath, tN.allTasksOnPath, tN.totalRevenue)
            self.leaves.append(tN)
            #---------------------------------------------------------------------------------------------
            self.root.children.append(tN)
            end = time.time() # end time
            self.dummyTime += (end - start)
            self.dummyNodeCount += 1
            self.nodecount += 1
            return    

        else:

            if (len(ptr.children) > 0):
                self.printit("    - - - - - - - - - - - - - - - - - - - - - - - - - - - - -")
                self.printit("    Traversing children of '" + str(ptr.name) + "'....")
                
                # only expand nodes that have not been blocked
                for child in ptr.children:
                    if ((child.blocked == False) and (child.winnerOnPath == True)):
                        self.printit("    Path to " + str(child.name) + " not blocked and has winner on path...")
                        self.addNodes(child, cNodes, taskName, addDummy) # recursive call
                    else:
                        self.printit("    !! Path to " + str(child.name) + " is blocked or no winner(s) on path, not proceeding !!")
                        
            else:
                
                self.printit("    For node " + str(ptr.name) + ", adding the current coalitions....")

                # if the leaf node is the winnerNode, then add children
                # we validate this by checking if the winnerNode's parent is the current ptr node's parent
                if (self.IsWinnerNode(ptr)):

                    coalition = []
                    for cn in cNodes:
                        coalition = cn.getCoalition()
                        self.printit("        Adding node " + str(coalition) + "....")
                        if (self.hasMember(ptr.robotsOnPath, coalition) == False):
                            self.printit("        -- current nodes not repeated in path")
                            self.printit("        -- items on path " + str(ptr.robotsOnPath))
                            
                            start = time.time() # start time
                            tN = treeNode(str(coalition), coalition, ptr.robotsOnPath + coalition)
                            tN.parent = ptr
                            tN.coalitionsOnPath = ptr.coalitionsOnPath[:] # deep copy the entire list
                            tN.coalitionsOnPath.append(coalition) # --> extra operation than DUMMY
                            #- - - - - - - - - - - - - -
                            tN.totalRevenue = int(ptr.totalRevenue) + int(cn.getBid())
                            #- - - - - - - - - - - - - -
                            tN.tasksOnPath = ptr.tasksOnPath[:] # deep copy the entire list
                            tN.tasksOnPath.append(taskName) # --> extra operation than DUMMY
                            #- - - - - - - - - - - - - -
                            tN.memberOfTask = taskName
                            #- - - - - - - - - - - - - -
                            tN.allTasksOnPath = ptr.allTasksOnPath[:]
                            tN.allTasksOnPath.append(taskName)
                            #- - - - - - - - - - - - - -
                            #---------------------------------------------------------------------------------------------
                            # determine the heuristic - used exclusively for A*
                            tN.heuristicVal, tN.futureNodes = self.estimateHeuristic(tN, tN.coalitionsOnPath, tN.allTasksOnPath, tN.totalRevenue)
                            #---------------------------------------------------------------------------------------------
                            self.printit("        -- tasks on path " + str(tN.tasksOnPath)) 
                            ptr.children.append(tN)
                            end = time.time() # end time
                            
                            self.trackWinner(tN.totalRevenue, tN.coalitionsOnPath, tN.tasksOnPath)

                            self.regularTime += (end - start)
                            self.regularNodeCount += 1
                            
                            self.nodecount += 1
                        else:
                            self.printit("        -- current nodes repeated -> NOT ADDING")
                            self.printit("        -- items on path " + str(ptr.robotsOnPath))

                        coalition = []
                    
                    if (addDummy):
                        # add dummy node
                        self.printit("      ** Adding dummy node to node '" + str(ptr.name) + "'....")
                        
                        start = time.time() # start time
                        tN = treeNode("dummy", [], ptr.robotsOnPath)
                        tN.parent = ptr
                        tN.coalitionsOnPath = ptr.coalitionsOnPath[:]
                        tN.totalRevenue = ptr.totalRevenue
                        tN.tasksOnPath = ptr.tasksOnPath
                        tN.memberOfTask = taskName
                        tN.allTasksOnPath = ptr.allTasksOnPath[:]
                        tN.allTasksOnPath.append(taskName)
                        #---------------------------------------------------------------------------------------------
                        # determine the heuristic - used exclusively for A*
                        tN.heuristicVal, tN.futureNodes = self.estimateHeuristic(tN, tN.coalitionsOnPath, tN.allTasksOnPath, tN.totalRevenue)
                        #---------------------------------------------------------------------------------------------
                        ptr.children.append(tN)
                        end = time.time() # end time
                        
                        self.dummyTime += (end - start)
                        self.dummyNodeCount += 1
                        self.nodecount += 1
                    else:
                        # dont add dummy node
                        self.printit("      ** Skipping adding dummy node to node '" + str(ptr.name) + "'....")
                        
                    self.printit("    . . . . . . . . . . . . . . . . . . . . . . . . . . . . .")
                    
                else:
                    self.printit("      ^^ Cannot add children to this node. It has the same g+h but these children are for " + str(self.winnerNode.name))

            
                # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
                # if no children could be added to current node, then that node is a leaf
                # add it to list of leaves and record revenue for A*
                self.printit("Children Added: --->>>>> " + str(len(ptr.children)))
                if (len(ptr.children) == 0):
                    #self.leaves.append(ptr)
                    self.printit("        No children added for " + str(ptr.name))
                else:
                    # remove ptr from self.leaves and add its children as the new leaves
                    for leaf in self.leaves:
                        if ((leaf.parent == ptr.parent) and
                            (leaf.name == ptr.name) and
                            (leaf.totalRevenue == ptr.totalRevenue) and
                            (leaf.memberOfTask == ptr.memberOfTask)):
                            self.leaves.pop(self.leaves.index(leaf))

                    for child in ptr.children:
                        self.leaves.append(child)
                        
                        

                # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
                    
                return

    def estimateHeuristic(self, node, coalitionsOnPath, allTasksOnPath, totalRevenue):
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
                        heuristic = float(cNode.getBid()) / len(cNode.getCoalition())
                        MaxHolder.append(heuristic)
            
            if len(MaxHolder) > 0:
                hF += max(MaxHolder)
            
        # collect the heuristics for each node belonging to each task
##        self.nodeHeuristics.append(g + hF)
##        self.leaves.append(node)
        
        return (g + hF), heurCBTList
    
