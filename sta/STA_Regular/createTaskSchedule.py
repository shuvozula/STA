import sys
import time
from taskNode import *
from coalitionNode import *
from coalitionTree import *


class createTaskSchedule:

    def __init__(self, textStream, screenDump):
        self.textStream = textStream
        self.ncount = 0
        self.screenDump = screenDump

    def printit(self, msg):
        if self.screenDump == True:
            print msg

    def run(self):

        tasks = []
        coalitionsByTasks = []

        # READ IN THE FILE >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        #f = open(self.inputFile, 'r')
        #fcontent = f.read()
        #lines = fcontent.split('\n')
        lines = self.textStream.split("\n")
##        print " "
##        print lines

        # STORE COALITIONS AND TASK BIDS >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        for line in range(len(lines)):
            t, c, b = lines[line].split(" ")
            
            # collect coalition
            blah = []
            blah = c.split(",")
            coalition = []
            for i in range(len(blah)):
                coalition.append(int(blah[i]))

            # check if the task 't' exists
            taskPresent = False
            for i in range(len(coalitionsByTasks)):
                if (coalitionsByTasks[i].isTask(t) == True):
                    cbt = coalitionsByTasks[i]
                    taskPresent = True
                    break

            if (taskPresent):
                cbt.addCoalition(coalition, b)
            else:
                cbtNode = taskNode(str(t))
                cbtNode.addCoalition(coalition, b)
                coalitionsByTasks.append(cbtNode)     

        # DUMP CONTENTS OF INPUT FILE >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
##        print "-------------------------------------------------------------"
##        print "<<<<<<<<<<<<<<<<<<<<<< INPUT FILE DUMP >>>>>>>>>>>>>>>>>>>>>>"
##        print "-------------------------------------------------------------"
##
##        for line in range(len(lines)):
##            print lines[line]

        # DUMP CONTENTS OF COLLECTED TASKS AND THEIR COALITION BIDS >>>>>>>>>>
##        print "-------------------------------------------------------------"
##        print "<<<<<<<<<<<<<< TASKS WITH COALITIONS AND BIDS >>>>>>>>>>>>>>>"
##        print "-------------------------------------------------------------"

##        for tNode in coalitionsByTasks:
##
##            print "Task <" + str(tNode.taskName) + ">"
##            print ""
##
##            for coalition in tNode.coalitionList:
##                print "    " + str(coalition.getCoalition()) + ", $" + str(coalition.getBid())
##
##            print ""

         # SORT THE LIST BASED ON THE NUMBER OF COALITIONS ASSIGNED TO EACH TASK
        self.printit("-------------------------------------------------------------")
        self.printit("<<<<<<<<<<< SORTING TASKS BY NUMBER OF COALITIONS >>>>>>>>>>>")
        self.printit("-------------------------------------------------------------")

        self.printit("sorting....")
        coalitionsByTasks.sort(lambda x, y: cmp(len(x.coalitionList), len(y.coalitionList)))
        self.printit("done sorting...\n")

        self.printit("Displaying all bids submitted per task...")
        self.printit("Showing tasks with increasing number of submitted bids...\n")
        for tNode in coalitionsByTasks:
            self.printit("Task <" + str(tNode.taskName) + ">\n")
            
            for coalition in tNode.coalitionList:
                self.printit("    " + str(coalition.getCoalition()) + ", $" + str(coalition.getBid()))

            self.printit("")
        


        self.ncount = 0
        
        # RECORD EXECUTION TIME
        start = time.time()

        # CONSTRUCT COALITIONTREE
        cTree = coalitionTree(coalitionsByTasks, self.screenDump)
        output = cTree.constructTree()

        # DETERMINE WINNING COALITION
        cTree.determineWinner()

        end = time.time()
        exeTime = end - start
        #print "Execution time     --> " + str(exeTime)

##        print "-------------------------------------------------------------"
##        print "TOTAL EXECUTION TIME: " + str(exeTime)
##        print "-------------------------------------------------------------"
        
        output.append(exeTime)
        return output


def main():

    filelocation = "C:\\Documents and Settings\\ssaha\\Desktop\\My Research\\Regular\\"
    f = open("gandu.txt", "r")
    fcontent = f.read()
    screenDump = False

    r = createTaskSchedule(fcontent, screenDump)
    xtime = r.run()
##    print xtime

##    # parse command line options
##    try:
##        opts, args = getopt.getopt(sys.argv[1:], "i:", ["input="])
##    except getopt.GetoptError:
##        print "Error: specify input file foo"
##        sys.exit(2)
##
##    # parse options
##    for opt, arg in opts:
##        if opt in ("-i", "--input"):
##            input_file = arg
##            parseFile(input_file)


if __name__ == "__main__":
    main()
        
