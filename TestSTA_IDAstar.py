import os, sys, time, random, math
#from STA_IDAstar.createData import createData
#from STA_Astar.createData import createData
from STA_Regular.createTaskSchedule import createTaskSchedule
from STA_Astar.createTaskScheduleASTAR import createTaskScheduleASTAR
from STA_IDAstar.createTaskScheduleIDASTAR import createTaskScheduleIDASTAR
from STA_IDAstar.createData import createData

def outputMatches(o1, o2):
    if ((o1[0] == o2[5]) and
        (o1[1] == o2[6]) and
        (o1[2] == o2[7])):
        return True
    else:
        return False


def IsRevenueSame(o1, o2):
    if (o1[2] == o2[7]):
        return True
    else:
        return False


def ensure_Dir(f):
    d = os.path.dirname(f)
    if not os.path.exists(d):
        os.makedirs(d)
    return f


def testIDAstar():

    numRobots = 10 # constant
    coalitionSize = [1, 9] # 3 for Uniform Distribution, 9 for Random Distribution
    fixedCoalitionSize = True  # True = uniform (higher coalition size is chosen), false = random
    bidSubmissionSizes = range(10, 200, 1)
    taskSizes = [20]
    maxIterations = 10
    maxBidValue = 100
    showInput = False

    breakOutNow = False
    
    for taskSize in taskSizes:

        if breakOutNow:
            break
        else:
            
            f1 = open(ensure_Dir("statistics/IDAStar/comparison-time/taskSize-" + str(taskSize) + "/regular.txt"), "w")
            f2 = open(ensure_Dir("statistics/IDAStar/comparison-time/taskSize-" + str(taskSize) + "/AStar.txt"), "w")
            f3 = open(ensure_Dir("statistics/IDAStar/comparison-time/taskSize-" + str(taskSize) + "/IDAStar.txt"), "w")
            
            f4 = open(ensure_Dir("statistics/IDAStar/comparison-space/taskSize-" + str(taskSize) + "/regular.txt"), "w")
            f5 = open(ensure_Dir("statistics/IDAStar/comparison-space/taskSize-" + str(taskSize) + "/AStar.txt"), "w")
            f6 = open(ensure_Dir("statistics/IDAStar/comparison-space/taskSize-" + str(taskSize) + "/IDAStar.txt"), "w")
            
            for bidLimit in bidSubmissionSizes:

                if breakOutNow:
                    break
                else:

                    print "BidLimit: " + str(bidLimit)
                    maxBidsPerTask = int(math.ceil(float(bidLimit)/float(taskSize))) * 2

                    diffTimeRegular = 0.0
                    diffTimeAStar = 0.0
                    diffTimeIDAStar = 0.0
                    
                    nodecountRegular = 0
                    nodecountAStar = 0
                    nodecountIDAStar = 0
                    
                    for avg in range(maxIterations):

                        print "Creating data....(" + str(avg) + ")"
                        data = createData(numRobots, \
                                          maxBidsPerTask, \
                                          coalitionSize, \
                                          bidLimit, \
                                          taskSize, \
                                          maxBidValue, \
                                          fixedCoalitionSize, \
                                          showInput)
                        print "Finished Creating data!!"

                        # Run data on IDA-Star version
                        idastar = createTaskScheduleIDASTAR(data, False)
                        print "Executing data on IDA-Star algorithm...."
#                        start = time.time()
                        output3 = idastar.run()
#                        end = time.time()
                        diffTimeIDAStar += output3[4] #(end - start)
                        nodecountIDAStar += output3[3]
                        print "EXE TIME --> IDA-STAR: " + str(output3[3]) #diffTimeIDAStar)
                        
                        # Run data on A-Star version
                        astar = createTaskScheduleASTAR(data, False)
                        print "Executing data on A-Star algorithm...."
#                        start = time.time()
                        output2 = astar.run()
#                        end = time.time()
                        diffTimeAStar += output2[8] #(end - start)
                        nodecountAStar += output2[0]
                        print "EXE TIME --> A-Star: " + str(output2[8])#diffTimeAStar)
                        
                        # Run data on regular version
                        regular = createTaskSchedule(data, False)
                        print "Executing data on Regular algorithm...."
#                        start = time.time()
                        output1 = regular.run()
#                        end = time.time()
                        diffTimeRegular += output1[8]#(end - start)
                        nodecountRegular += output1[0]
                        print "EXE TIME --> REGULAR: " + str(output1[8])#diffTimeRegular)
                        
                        print output1
                        print len(output1)
                        print output2
                        print len(output2)
                        print output3
                        print len(output3)
                        
                        if (outputMatches(output3, output1)):
                            print "OUTPUT MATCHES.... =)"
                        else:
                            if (IsRevenueSame(output3, output1)):
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
                    
                    avgTimeRegular = diffTimeRegular / maxIterations
                    avgTimeAStar   = diffTimeAStar / maxIterations
                    avgTimeIDAStar = diffTimeIDAStar / maxIterations
                    
                    avgNodeCountRegular = nodecountRegular / maxIterations
                    avgNodeCountAStar   = nodecountAStar / maxIterations
                    avgNodeCountIDAStar = nodecountIDAStar / maxIterations 
                    
                    # report times
                    f1.write(str(bidLimit) + ", " + str(avgTimeRegular) + "\n")
                    f1.flush()

                    f2.write(str(bidLimit) + ", " + str(avgTimeAStar) + "\n")
                    f2.flush()
                    
                    f3.write(str(bidLimit) + ", " + str(avgTimeIDAStar) + "\n")
                    f3.flush()
                    
                    # report node counts - space
                    f4.write(str(bidLimit) + ", " + str(avgNodeCountRegular) + "\n")
                    f4.flush()

                    f5.write(str(bidLimit) + ", " + str(avgNodeCountAStar) + "\n")
                    f5.flush()
                    
                    f6.write(str(bidLimit) + ", " + str(avgNodeCountIDAStar) + "\n")
                    f6.flush()
                    
                    #time.sleep(5)
                    
            f1.close()
            f2.close()
            f3.close()
            f4.close()
            f5.close()
            f6.close()

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
    
    testIDAstar()
    #collectData()
