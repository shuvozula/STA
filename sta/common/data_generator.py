
__author__ = 'Spondon Saha'


import logging
import math
import random


class Error(Exception):
    """Native exception class."""
    pass


def GenData(num_robots, coalition_size_range, bid_limit, task_size,
            max_bid_value, max_bids_per_task):
    """Data generator for creating random bids submitted by robot coalitions.

    List of tasks to accomplish have been announced and this data generator
    creates random bids and submits them as a tuple of the bid-value and
    the list of robots (robot coalition) that submitted it. The data is
    generated based on the provided parameters.

    The data generated looks a lot like this:
    T3 2,3 7
    T1 1,3,5 9
    T4 4 10
    ...

    Arguments:
        num_robots: the number of robots
        coalition_size_range: allowed range of coalition sizes in the following
        format [min_range, max_range] where min_range <= max_range.
        bid_limit: The maximum number of bids that the STA algorithm will take
        for this round.
        task_size: Number of tasks to accomplish
        max_bid_valiue: Maximum allowable bid value accepted in the auction.
        max_bids_per_task: Maximum number of bids allowed to be submitted for
        each task.

    Raises:
        Error: Whenever we have one of the following problems:
        1. The provided coalition_size_range set does not have 2 elements within
        2.

    Returns:
        The generated data as collected in all_bids.
    """
    all_bids = []
    # create the task list
    task_names = ['T%s' % (task_num + 1) for task_num in range(task_size)]
    task_counts = [0] * task_size
    all_tasks = dict(zip(task_names, task_counts))
    # generate bids
    curr_bid_count = 0
    while curr_bid_count <= bid_limit:
        # acquire a random task
        while True:
            rnd_task = random.choice(task_names)
            if all_tasks[rnd_task] < max_bids_per_task:
                all_tasks[rnd_task] += 1
                break
        # validate coalition size ranges and acquire random coalition size
        if len(coalition_size_range) > 2:
            raise Error('Expected [lower, upper] got %s' % coalition_size_range)
        elif coalition_size_range[0] > coalition_size_range[1]:
            raise Error('Min-range > Max-range: %s' % coalition_size_range)
        else:
            rnd_coalition_size = random.randint(*coalition_size_range)
        # generate a coalition of robots of size rnd_coalition_size
        # assumption: robots are identified as numbers
        coalition = random.sample(range(1, num_robots), rnd_coalition_size)
        coalition = [str(x) for x in coalition]
        # put them together
        rnd_bid_value = random.randint(1, max_bid_value)
        all_bids.append('%s %s %s' % (rnd_task,
                                      ','.join(coalition),
                                      rnd_bid_value))
        # update the bid count
        curr_bid_count += 1
    return '\n'.join(all_bids)

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
