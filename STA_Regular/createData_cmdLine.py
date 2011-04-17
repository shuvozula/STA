import getopt, sys
import random
from createTaskSchedule import *

def createData(numItems, numBids, numTasks, outFile):

    arrItems = range(1, numItems+1)

    arrTasks = []
    for task in range(numTasks):
        arrTasks.append("T" + str(task+1))

    FILE = open(outFile, 'w')
    line = ""

    for bid in range(numBids):

        task = random.choice(arrTasks) # select a random task
        line = str(task) + " "
        
        numRobots = random.randint(1, numItems) # select a random coalition size
        for i in range(numRobots):
            if (i == (numRobots-1)):
                line += str(random.randint(1,numItems))
                line += " "
            else:
                line += str(random.randint(1,numItems)) + ","
                
        line += str(random.randint(1,100)) # select a random bid value
        
        FILE.write(line) # write string to file

    FILE.close()


def main():

    smallArgs = 'i:b:t:o:'
    longArgs = ['items=', 'bids=', 'tasks=', 'output_file=']

    try:
        opts, args = getopt.getopt(sys.argv[1:], smallArgs, longArgs)
    except getopt.GetoptError:
        print "check yo arguments"
        sys.exit(2)

    for opt, arg in opts:

        if opt in ('-i', '--items'):
            numItems = arg

        if opt in ('-b', '--bids'):
            numBids = arg

        if opt in ('-t', '--tasks'):
            numTasks = arg

        if opt in ('-o', '--output_file'):
            outFile = arg

    createData(numItems, numBids, numTasks, outFile)
    r = createTaskSchedule(outFile)
    r.run()

if __name__ == '__main__':
    main()
