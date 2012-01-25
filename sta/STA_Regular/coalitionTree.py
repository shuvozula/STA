import sys, time
from treeNode import *

class coalitionTree:

    def __init__(self, coalitionsByTasksList, screenDump):
        self.coalitionsByTasksList = coalitionsByTasksList
        self.root = treeNode("root", [], []) # name, coalition, onPath
        self.orderOfTasks = []
        self.bestRevenue = 0
        self.bestPartition = None
        self.chosenTasks = []

        self.nodecount = 0
        self.dummyNodeCount = 0
        self.regularNodeCount = 0
        self.dummyTime = 0.0
        self.regularTime = 0.0

        # enable/disable print
        self.screenDump = screenDump

    def printit(self, msg):
        if self.screenDump == True:
            print msg

    def constructTree(self):

        # START BUILDING THE TREE
        self.printit("-------------------------------------------------------------")
        self.printit("<<<<<<<<<<<<<<<< CONSTRUCTING COALITION TREE >>>>>>>>>>>>>>>>")
        self.printit("-------------------------------------------------------------")
        
        for tNode in self.coalitionsByTasksList:

            cNodes = tNode.coalitionList
            self.orderOfTasks.append(tNode.taskName)
            self.printit("Adding coalition nodes: ")
            for c in cNodes:
                self.printit("    " + str(c.getCoalition()))

            if (len(self.coalitionsByTasksList)-1 == self.coalitionsByTasksList.index(tNode)):
                self.addNodes(self.root, cNodes, tNode.taskName, False) # add dummy nodes
            else:
                self.addNodes(self.root, cNodes, tNode.taskName, True) # dont add dummy nodes
            self.printit("-------------------------------------------------------------")

        self.printit("Order of Tasks: " + str(self.orderOfTasks))

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
        output.append(str(self.bestPartition))
        output.append(str(self.chosenTasks))
        output.append(str(self.bestRevenue))
        return output


    def addNodes(self, ptr, cNodes, taskName, addDummy, nodesOnPath = []):

        if ((ptr.name == "root") and (len(ptr.children) == 0)):

            # add the coalitions to the root node
            self.printit("    Adding Nodes to root....")
            for cn in cNodes:
                coalition = cn.getCoalition()
                
                start = time.time() # start time
                tN = treeNode(str(coalition), coalition, coalition)
                tN.coalitionsOnPath.append(coalition)
                tN.totalRevenue = int(cn.getBid())
                tN.tasksOnPath.append(taskName)
                self.root.children.append(tN)
                end = time.time() # end time
                
                self.trackWinner(tN.totalRevenue, tN.coalitionsOnPath, tN.tasksOnPath)
                
                self.regularTime += (end - start)
                self.regularNodeCount += 1
                self.nodecount += 1

            # add dummy node
            self.printit("    Adding dummy node to node '" + str(ptr.name) + "'....")
            start = time.time() # start time
            self.root.children.append(treeNode("dummy", [], []))
            end = time.time() # end time
            self.dummyTime += (end - start)
            self.dummyNodeCount += 1
            self.nodecount += 1
            return    

        else:

            if (len(ptr.children) > 0):
                self.printit("    - - - - - - - - - - - - - - - - - - - - - - - - - - - - -")
                self.printit("    Traversing children of '" + str(ptr.name) + "'....")

                for child in ptr.children:
                    self.addNodes(child, cNodes, taskName, addDummy)

            else:

                self.printit("    For node " + str(ptr.name) + ", adding the current coalitions....")

                coalition = []
                for cn in cNodes:
                    coalition = cn.getCoalition()
                    self.printit("        Adding node " + str(coalition) + "....")
                    if (self.hasMember(ptr.hasOnPath, coalition) == False):
                        self.printit("        -- current nodes not repeated in path")
                        self.printit("        -- items on path " + str(ptr.hasOnPath))
                        
                        start = time.time() # start time
                        tN = treeNode(str(coalition), coalition, ptr.hasOnPath + coalition)
                        tN.coalitionsOnPath = ptr.coalitionsOnPath[:]
                        tN.coalitionsOnPath.append(coalition) # --> extra operation than DUMMY
                        tN.totalRevenue = int(ptr.totalRevenue) + int(cn.getBid())
                        tN.tasksOnPath = ptr.tasksOnPath[:]
                        tN.tasksOnPath.append(taskName) # --> extra operation than DUMMY
                        self.printit("        -- tasks on path " + str(tN.tasksOnPath))
                        ptr.children.append(tN)
                        end = time.time() # end time
                        
                        self.trackWinner(tN.totalRevenue, tN.coalitionsOnPath, tN.tasksOnPath)

                        self.regularTime += (end - start)
                        self.regularNodeCount += 1
                        
                        self.nodecount += 1
                    else:
                        self.printit("        -- current nodes repeated -> NOT ADDING")
                        self.printit("        -- items on path " + str(ptr.hasOnPath))

                    coalition = []

                if (addDummy):
                    # add dummy node
                    self.printit("      ** Adding dummy node to node '" + str(ptr.name) + "'....")
                    
                    start = time.time() # start time
                    tN = treeNode("dummy", [], ptr.hasOnPath)
                    tN.coalitionsOnPath = ptr.coalitionsOnPath[:]
                    tN.totalRevenue = ptr.totalRevenue
                    tN.tasksOnPath = ptr.tasksOnPath
                    ptr.children.append(tN)
                    end = time.time() # end time
                    
                    self.dummyTime += (end - start)
                    self.dummyNodeCount += 1
                    self.nodecount += 1
                else:
                    # dont add dummy node
                    self.printit("      ** Skipping adding dummy node to node '" + str(ptr.name) + "'....")
                    
                self.printit("    . . . . . . . . . . . . . . . . . . . . . . . . . . . . .")
                return

        
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
        self.printit("Winning coalitions --> " + str(self.bestPartition))
        self.printit("Respective tasks   --> " + str(self.chosenTasks))
        self.printit("Revenue fetched    --> " + str(self.bestRevenue))
