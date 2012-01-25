import logging
import gflags
import sys
import time
from taskNode import *
from coalitionNode import *
from coalitionTree import *

FLAGS = gflags.FLAGS

gflags.DEFINE_string('bid_file',
                     None,
                     'Location of the bid file to create the STA tree.',
                     short_name = 'f')

gflags.MarkFlagAsRequired('bid_file')


class Error(Exception):
    """Native exception class."""
    pass


def ReadData(text_stream):
    """"""
    task_nodes = {}
    lines = text_stream.split("\n")
    logging.debug('Num bids submitted: %s' % len(lines))
    # store coalitions and task bids
    for line in lines:
        task_id, coalition, bid_value = line.split(" ")
        # collect coalition
        coalition = coalition.split(",")
        coalition = map(lambda x: int(x), coalition)
        # add coalition to existing task, else create a new TaskContainer
        # object and make a new entry for coalition
        if task_id not in task_nodes.keys():
            new_task_node = TaskContainer(task_id)
            new_task_node.AddBid(coalition, bid_value)
            task_nodes[task_id] = new_task_node
        else:
            task_nodes[task_id].AddBid(coalition, bid_value)
    # sort the list based on the number of coalitions assigned to each task
    logging.debug("----------------------------------------------------------")
    logging.debug("<<<<<<<<< SORTING TASKS BY NUMBER OF COALITIONS >>>>>>>>>>")
    logging.debug("----------------------------------------------------------")
    logging.debug("sorting....")
    #coalitionsByTasks.sort(lambda x, y: cmp(len(x.coalitionList), len(y.coalitionList)))
    coalitionsByTasks.sort(lambda x, y: cmp(len(x.coalitionList), len(y.coalitionList)))
    logging.debug("done sorting...\n")
    
    logging.debug("Displaying all bids submitted per task...")
    logging.debug("Showing tasks with increasing number of submitted bids...\n")
    for tNode in coalitionsByTasks:
        logging.debug("Task <" + str(tNode.taskName) + ">\n")

        for coalition in tNode.coalitionList:
            logging.debug("    " + str(coalition.getCoalition()) + ", $" + str(coalition.getBid()))

        logging.debug("")
    
    self.ncount = 0


def RunSTA(self, text_stream):
    """Runs the IDA* equipped STA algorithm.

    Arguments:
        text_stream: A file object.

    Raises:
        None

    Returns:
        None
    """
    
    
    # RECORD EXECUTION TIME
    start = time.time()

    # CONSTRUCT COALITIONTREE
    cTree = coalitionTree(coalitionsByTasks, self.screenDump)
    output = cTree.constructTree()

    # DETERMINE WINNING COALITION
    #cTree.determineWinner()

    end = time.time()
    exeTime = end - start
    #print "Execution time     --> " + str(exeTime)

    #print "-------------------------------------------------------------"
    #print "TOTAL EXECUTION TIME: " + str(exeTime)
    #print "-------------------------------------------------------------"
    
    output.append(exeTime)
    return output


def main(argv):
    """Entry point for STA calculation.

    Arguments:
        argv: command line arguments

    Returns:
        None

    Raises:
        None
    """
    # get the flag values
    try:
        argv = FLAGS(argv)
    except gflags.FlagsError, ex:
        raise Error('%s \\nUSAGE: %s ARGS\\n%s' % (ex, sys.argv[0], FLAGS))
    # read in submitted bids
    if FLAGS.bid_file is not None:
        try:
            fp = open(FLAGS.bid_file, "r")
        except IOError, ex:
            raise Error('Error encountered when opening bid-file: \\n%s' % ex)
    else:
        raise Error('No bid-file parameter value passed.')
    # read all file contents
    fcontent = fp.read()
    # start the STA algorithm
    try:
        execution_time = RunSTA(fcontent)
    except Exception or StandardError, ex:
        raise Error('Error encountered!\nOriginal Exception:\n%s' % ex)
    else:
        logging.debug('Total Execution time: %s' % execution_time)


if __name__ == "__main__":
    main()
        
