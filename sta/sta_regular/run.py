import sys
import time
from taskNode import *
from coalitionNode import *
from coalitionTree import *

tasks = []
coalitionsByTasks = []

# READ IN THE FILE >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
f = open('input.txt', 'r')
fcontent = f.read()
lines = fcontent.split('\n')

# STORE COALITIONS AND TASK BIDS >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
for line in range(len(lines)):
    t, c, b = lines[line].split(' ')
    
    # collect coalition
    blah = []
    blah = c.split(',')
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
print "-------------------------------------------------------------"
print "<<<<<<<<<<<<<<<<<<<<<< INPUT FILE DUMP >>>>>>>>>>>>>>>>>>>>>>"
print "-------------------------------------------------------------"

for line in range(len(lines)):
    print lines[line]

# DUMP CONTENTS OF COLLECTED TASKS AND THEIR COALITION BIDS >>>>>>>>>>
print "-------------------------------------------------------------"
print "<<<<<<<<<<<<<< TASKS WITH COALITIONS AND BIDS >>>>>>>>>>>>>>>"
print "-------------------------------------------------------------"

for tNode in coalitionsByTasks:

    print "Task <" + str(tNode.taskName) + ">"
    print ""

    for coalition in tNode.coalitionList:
        print "    " + str(coalition.getCoalition()) + ", $" + str(coalition.getBid())

    print ""
# RECORD EXECUTION TIME
start = time.time()

# CONSTRUCT COALITIONTREE
cTree = coalitionTree(coalitionsByTasks)
cTree.constructTree()

# DETERMINE WINNING COALITION
cTree.determineWinner()

end = time.time()
exeTime = end - start

print "-------------------------------------------------------------"
print "TOTAL EXECUTION TIME: " + str(exeTime)
print "-------------------------------------------------------------"
