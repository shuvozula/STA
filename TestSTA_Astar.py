import os, sys, time, random, math
from STA_Astar.createTaskScheduleASTAR import createTaskScheduleASTAR
from STA_Astar.createData import createData
from STA_Regular.createTaskSchedule import createTaskSchedule

def outputMatches(o1, o2):

    if ((o1[5] == o2[5]) and
        (o1[6] == o2[6]) and
        (o1[7] == o2[7])):
        return True
    else:
        return False


def IsRevenueSame(o1, o2):
    if (o1[7] == o2[7]):
        return True
    else:
        return False


def ensure_Dir(f):
    d = os.path.dirname(f)
    if not os.path.exists(d):
        os.makedirs(d)
    return f


def testAstar():

    numRobots = 10 # constant
    coalitionSize = [1, 9] # 3 for Uniform Distribution, 9 for Random Distribution
    fixedCoalitionSize = False
    bidSubmissionSizes = range(10, 60, 1)
    taskSizes = [20]
    maxIterations = 10
    maxBidValue = 100

    breakOutNow = False
    
    for taskSize in taskSizes:

        if breakOutNow:
            break
        else:
            
            f1 = open(ensure_Dir("statistics/IDAStar/comparison-time-astar/taskSize-" + str(taskSize) + "/aStar.txt"), "w")
            f2 = open(ensure_Dir("statistics/IDAStar/comparison-time-astar/taskSize-" + str(taskSize) + "/regular.txt"), "w")
            
            for bidLimit in bidSubmissionSizes:

                if breakOutNow:
                    break
                else:

                    print "BidLimit: " + str(bidLimit)
                    maxBidsPerTask = int(math.ceil(float(bidLimit)/float(taskSize))) * 2

                    diffTimeAstar = 0.0
                    diffTimeRegular = 0.0
                    
                    for avg in range(maxIterations):

                        print "Creating data....(" + str(avg) + ")"
                        data = createData(numRobots, \
                                          maxBidsPerTask, \
                                          coalitionSize, \
                                          bidLimit, \
                                          taskSize, \
                                          maxBidValue, \
                                          fixedCoalitionSize)
                        print "Finished Creating data!!"
                        
                        # Run data on A-Star version
                        astar = createTaskScheduleASTAR(data, False)
                        print "Executing data on A-Star algorithm...."
                        start = time.time()
                        output1 = astar.run()
                        end = time.time()
                        diffTimeAstar += (end - start)
                        print "EXE TIME --> A-STAR: " + str(diffTimeAstar)

                        # Run data on regular version
                        regular = createTaskSchedule(data, False)
                        print "Executing data on Regular algorithm...."
                        start = time.time()
                        output2 = regular.run()
                        end = time.time()
                        diffTimeRegular += (end - start)
                        print "EXE TIME --> REGULAR: " + str(diffTimeRegular)

                        if (outputMatches(output1, output2)):
                            print "OUTPUT MATCHES.... =)"
                        else:
                            if (IsRevenueSame(output1, output2)):
                                print "REVENUE MATCHES BUT SOLUTIONS ARE DIFFERENT."
                            else:                                
                                print "OOPS, it doesn't match =("
                                breakOutNow = True
                                break

##                            print "--- A-STAR RESULTS: -----------------"
##                            print "Winning coalitions --> " + str(output1[5])
##                            print "Respective tasks   --> " + str(output1[6])
##                            print "Revenue fetched    --> " + str(output1[7])
##                            print "--- REGULAR RESLTS -----------------"
##                            print "Winning coalitions --> " + str(output2[5])
##                            print "Respective tasks   --> " + str(output2[6])
##                            print "Revenue fetched    --> " + str(output2[7])


                    

                    print "***********************************************"

                    avgTimeAStar = diffTimeAstar / maxIterations
                    avgTimeRegular = diffTimeRegular / maxIterations

                    f1.write(str(bidLimit) + ", " +
                             str(avgTimeAStar) + "\n")

                    f1.flush()

                    f2.write(str(bidLimit) + ", " +
                             str(avgTimeRegular) + "\n")

                    f2.flush()
                    
            f1.close()
            f2.close()

def collectData():

    numRobots = 10 # constant
    coalitionSize = [1, 6] # 3 for Uniform Distribution, 9 for Random Distribution
    fixedCoalitionSize = True
    bidSubmissionSizes = range(10, 60, 1)
    taskSizes = [80]
    maxIterations = 10
    maxBidValue = 100

    for taskSize in taskSizes:
            
        f = open(ensure_Dir("statistics/Uniform(6)/taskSize-" + str(taskSize) + "/aStar.txt"), "w")
        
        for bidLimit in bidSubmissionSizes:

            print "BidLimit: " + str(bidLimit)
            maxBidsPerTask = int(math.ceil(float(bidLimit)/float(taskSize))) * 2

            totalTime = 0.0
            
            for avg in range(maxIterations):

                print "Creating data....(" + str(avg) + ")"
                data = createData(numRobots, \
                                  maxBidsPerTask, \
                                  coalitionSize, \
                                  bidLimit, \
                                  taskSize, \
                                  maxBidValue, \
                                  fixedCoalitionSize)
                print "Finished Creating data!!"
                
                # Run data on A-Star version
                astar = createTaskScheduleASTAR(data, False)
                print "Executing data on A-Star algorithm...."
                start = time.time()
                output1 = astar.run()
                end = time.time()
                totalTime += (end - start)
                print "EXE TIME --> A-STAR: " + str(totalTime)
                

            print "***********************************************"

            avgTimeAStar = totalTime / maxIterations

            f.write(str(bidLimit) + ", " +
                    str(avgTimeAStar) + "\n")

            f.flush()

            
        f.close()

            
if __name__ == '__main__':
    
    testAstar()
    #collectData()

                

                             
