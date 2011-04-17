import getopt, sys
import random
import math
from createTaskScheduleASTAR import *

def createData(numRobots, maxBidsPerTask, coalitionSize, bidLimit, taskSize, maxBidValue, fixedCoalitionSize):

    ALLBIDS = []
    dataCollection = ""
    arrTasks = []
    arrBidsPerTaskCount = []
    for task in range(taskSize):
        arrTasks.append("T" + str(task+1))
        arrBidsPerTaskCount.append(0)

    line = ""
    for bidSize in range(bidLimit):

        doublePositive = True
        while (doublePositive):
        
            task = ""
            taskCountExceeded = True
            while (taskCountExceeded):
                task = random.choice(arrTasks) # select a random task
                if ((arrBidsPerTaskCount[arrTasks.index(task)]+1) <= maxBidsPerTask):
                    arrBidsPerTaskCount[arrTasks.index(task)] += 1
                    taskCountExceeded = False
                else:
                    taskCountExceeded = True
                    print "task count exceeded: " + str(arrBidsPerTaskCount)
    
            
            if (fixedCoalitionSize):
                randSize = coalitionSize[1]
            else:
                randSize = random.randint(coalitionSize[0], coalitionSize[1]) # select a random coalition size

            printCoalition = ""    
            coalition = []
            coalition.append(random.randint(1,numRobots))
            for i in range(randSize):
                repeat = True
                while (repeat):
                    val = random.randint(1,numRobots)
                    if (coalition.count(val) > 0):
                        repeat = True
                    else:
                        coalition.append(val)
                        repeat = False
    
            for j in range(randSize):
                if (j == (randSize-1)):
                    printCoalition += str(coalition[j]) + " "
                else:
                    printCoalition += str(coalition[j]) + ","
            
            line = ""
            line = str(task) + " " + printCoalition
#            print "**** ||" + str(line) + "||"
            
            dblPos = False
            for taskCoal in ALLBIDS:
                if (taskCoal == line):
                    dblPos = True
            
            if (dblPos):
                print str(line) + " ---> bid is being repeated, skipping...."
            else:
                ALLBIDS.append(line)
                line += str(random.randint(1,maxBidValue))
                doublePositive = False
                print line
                #if (bidSize < (bidLimit-1)):
                if (range(bidLimit).index(bidSize) == (len(range(bidLimit)) - 1)):
                    dataCollection += line
                else:
                    dataCollection += line + "\n"

    #print line
    
#    print "#_#_#_#_#"
#    for blah in ALLBIDS:
#        print blah
#    print "#_#_#_#_#"
    print "- - - - - - - - - - - - - - - - -"
    print "Count of the bids per task: " + str(arrBidsPerTaskCount)
    print "----------------------------------------------------"
    
    print dataCollection
    
    return dataCollection

def calcSD(nodecounts):

    print "Nodecounts: " + str(nodecounts)
    total = 0
    for i in nodecounts:
        total += int(i)

    mean = float(total) / float(len(nodecounts))
    print "Total: " + str(total)
    print "Mean: " + str(mean)

    deviation = []
    for i in nodecounts:
        deviation.append(float(i) - mean)

    print "Deviation: " + str(deviation)

    squaredDeviations = []
    for i in deviation:
        squaredDeviations.append(i * i)

    print "Sq. Deviations: " + str(squaredDeviations)

    sumSquaredDevs = 0.0
    for i in squaredDeviations:
        sumSquaredDevs += i

    print "Sum Squared Deviations: " + str(sumSquaredDevs)

    divsum = float(sumSquaredDevs / float(len(nodecounts)))
    print "DivSum: " + str(divsum)

    return math.sqrt(divsum)


def runTest():

    numRobots = 10 # constant
    coalitionSize = [1, 3] # 3 for Uniform Distribution, 9 for Random Distribution
    maxBidSubmissions = 10
    taskSizes = [3]
    maxIterations = 1
    maxBidValue = 10

    nodeCount = []
    dummyNodeCount = []
    regularNodeCount = []
    dummyTime = []
    regularTime = []
    dummyTimePerNode = []
    regularTimePerNode = []
    meanDummyTime = 0.0
    meanRegularTime = 0.0

    for taskSize in taskSizes:

        f = open("../statistics/dummy_regular_nodeCounts_N_times_RANDOM_" + str(taskSize) + "-2.txt", "w")

        for bidLimit in range(10, maxBidSubmissions+1):

            print "BidLimit: " + str(bidLimit)
            totalTime = float(0)
            maxBidsPerTask = int(math.ceil(float(bidLimit)/float(taskSize))) * 2

            nodeCount = []
            dummyNodeCount = []
            regularNodeCount = []
            dummyTime = []
            regularTime = []
            dummyTimePerNode = []
            regularTimePerNode = []
            meanDummyTime = 0.0
            meanRegularTime = 0.0
            
            for avg in range(maxIterations): # execute it 10 times for each bidSize
                print "Creating data....(" + str(avg) + ")"
                data = createData(numRobots, maxBidsPerTask, coalitionSize, bidLimit, taskSize, maxBidValue)
                print "Finished Creating data!!"
                r = createTaskScheduleASTAR(data, True)
                print "Executing data on algorithm...."
                output = r.run()

                nodeCount.append(output[0])
                dummyNodeCount.append(output[1])
                regularNodeCount.append(output[2])
                dummyTime.append(output[3])
                regularTime.append(output[4])
                meanDummyTime = output[3] / output[1]
                dummyTimePerNode.append(meanDummyTime)
                meanRegularTime = output[4] / output[2]
                regularTimePerNode.append(meanRegularTime)
                xTime = output[5]
                
                print "Finished running!!"
                totalTime += float(str(xTime))

            print "----------------------------"

            avgTime = totalTime / 10
            sd = calcSD(nodeCount)

            meanDummyTime = meanDummyTime / 10
            meanRegularTime = meanRegularTime / 10
            
            f.write(str(bidLimit) + ", " +
                    str(avgTime) + ", " +
                    str(nodeCount) + ", " +
                    str(sd) + " ||| " +
                    str(dummyNodeCount) + ", " +
                    str(regularNodeCount) + ", " +
                    str(dummyTime) + ", " +
                    str(regularTime) + ", " +
                    str(dummyTimePerNode) + ", " +
                    str(regularTimePerNode) + ", " +
                    str(meanDummyTime) + ", " +
                    str(meanRegularTime) + "\n")
            f.flush()
            #print str(bidLimit) + ", " + str(avgTime)
            #print "----------------------------------------------------------------------------------------"

        f.close()
        #print "Collected results for 'results_" + str(taskSize) + ".txt'"

if __name__ == '__main__':
    runTest()
