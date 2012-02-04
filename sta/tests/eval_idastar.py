
__author__ = 'Spondon Saha'


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

    num_robots = 10 # constant
    coalition_size_range = [1, 3] # 3 for Uniform Distribution, 9 for Random Distribution
    maxBidSubmissions = 10
    task_sizes = [3]
    maxIterations = 1
    max_bid_value = 10

    nodeCount = []
    dummyNodeCount = []
    regularNodeCount = []
    dummyTime = []
    regularTime = []
    dummyTimePerNode = []
    regularTimePerNode = []
    meanDummyTime = 0.0
    meanRegularTime = 0.0

    for task_size in task_sizes:

        f = open("../statistics/dummy_regular_nodeCounts_N_times_RANDOM_" + str(task_size) + "-2.txt", "w")

        for bid_limit in range(10, maxBidSubmissions+1):

            print "BidLimit: " + str(bid_limit)
            totalTime = float(0)
            max_bids_per_task = int(math.ceil(float(bid_limit)/float(task_size))) * 2

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
                data = createData(num_robots, max_bids_per_task, coalition_size_range, bid_limit, task_size, max_bid_value)
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
            
            f.write(str(bid_limit) + ", " +
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
            #print str(bid_limit) + ", " + str(avgTime)
            #print "----------------------------------------------------------------------------------------"

        f.close()
        #print "Collected results for 'results_" + str(task_size) + ".txt'"

if __name__ == '__main__':
    runTest()