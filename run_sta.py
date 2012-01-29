
__author__ = 'Spondon Saha'

import gflags
import heapq
import logging
import os
import sys
import time
import traceback
import sta.common.utils
from sta.common.task_container import TaskContainer
from sta.sta_idastar.coalition_tree import CoalitionTree as IdaCoalitionTree


FLAGS = gflags.FLAGS
COALITION_TREE_CLS = {'regular': None,
                      'a_star': None,
                      'ida_star': IdaCoalitionTree}

# flags
gflags.DEFINE_string('bid_file',
                     None,
                     'Location of the bid file to create the STA tree.',
                     short_name = 'f')

gflags.DEFINE_string('sta_run_type',
                     None,
                     'Type of run, either ida_star, astar or regular.')

# required flags
gflags.MarkFlagAsRequired('bid_file')
gflags.MarkFlagAsRequired('sta_run_type')


class Error(Exception):
    """Native exception class."""
    pass


def GetSubmittedBids(text_stream):
    """Reads the contents of the bid-file and parses it into data-structures.

    The contents of the bid-file are usually of the following format:
    T1 R2,R7,R8 123
    T1 R1,R9 21
    T3 R5,R7 84
    ...
    The format is the Task-id, followed by the comma-separated list of robots
    that submitted a bid for that task (coalition of robots), followed by
    the bid-value that they submitted for that task.

    Arguments:
        text_stream: A file object pointing to the bid-file

    Returns:
        List of TaskContainer objects that contain the list of bids submitted
        to it, along with their corresponding bid-values. This list is sorted
        based on the number of bids submitted for each task (TaskContainer
        object) in increasing order. So the TaskContainer object with the
        least number of bids submitted will appear in the beginning of the
        list, the ones with the highest number of bids appear towards the end.

    Raises:
        None
    """
    task_nodes = {}
    lines = text_stream.split('\n')
    logging.info('Num bids submitted: %s' % len(lines))
    # store coalitions and task bids
    for line in lines:
        task_id, coalition, bid_value = line.split(' ')
        # collect coalition
        coalition = coalition.split(',')
        coalition = map(lambda x: int(x), coalition)
        # add coalition to existing task, else create a new TaskContainer
        # object and make a new entry for coalition
        if task_id not in task_nodes.keys():
            new_task_node = TaskContainer(task_id)
            new_task_node.AddBid(coalition, bid_value)
            task_nodes[task_id] = [1, new_task_node]  # count, object
        else:
            task_nodes[task_id][0] += 1
            task_nodes[task_id][1].AddBid(coalition, bid_value)
    # sort the list based on the number of coalitions assigned to each task
    logging.info('Sorting list of TaskContainer objects to priority queue....')
    task_nodes_heapq = task_nodes.values()
    heapq.heapify(task_nodes_heapq)
    logging.info('Done converting to priority queue/heap!')
    # for display only
    logging.info('Showing tasks with increasing number of submitted bids...')
    for count, task_node in task_nodes_heapq:
        logging.info('Task <%s>' % task_node.task_name)
        bid_containers = task_node.GetBidList()
        coalitions = [x.GetCoalition() for x in bid_containers]
        bid_values = [x.GetBidValue() for x in bid_containers]
        log_msgs = map(lambda x: '    %s, $%s' % (x[0], x[1]),
                       zip(coalitions, bid_values))
        map(lambda x: logging.info(x), log_msgs)
    bid_counts, task_nodes = zip(*task_nodes_heapq)
    return list(task_nodes)


def RunSTA(ctree_cls, task_objects):
    """Runs the IDA* equipped STA algorithm.

    Arguments:
        ctree_cls: The CoalitionTree class to be used for this particular run.
        task_objects: A list of TaskContainer objects containing bids

    Raises:
        None

    Returns:
        None
    """
    # record the start time
    start = time.time()
    # construct the STA bid tree / coalition tree
    ctree_obj = ctree_cls(task_objects)
    output = ctree_obj.ConstructTree()
    # record end time
    end = time.time()
    exe_time = end - start
    output['exe_time'] = exe_time
    return output


def main(argv):
    """Entry point for STA calculation.

    Arguments:
        argv: command line arguments

    Returns:
        None

    Raises:
        Error: Whenever the wrong arguments or no arguments are passed, or when
        opening the bid-file. Also thrown when the STA algorithm encounters
        an exception.
    """
    # setup logging
    log_filepath = os.path.join(sta.common.utils.DEFAULT_LOG_DIR,
                                sta.common.utils.DEFAULT_LOG_FILE)
    sta.common.utils.SetupLogging(logging.DEBUG, log_filepath)
    # get the flag values
    try:
        argv = FLAGS(argv)
    except gflags.FlagsError, ex:
        raise Error('%s \\nUSAGE: %s ARGS\\n%s' % (ex, sys.argv[0], FLAGS))
    # read in submitted bids
    try:
        fp = open(FLAGS.bid_file, "r")
    except IOError, ex:
        raise Error('Error encountered when opening bid-file: \\n%s' % ex)
    else:
        submitted_bids = fp.read()  # read all file contents
    # acquire the CoalitionTree class for the current run requested
    try:
        ctree_cls = COALITION_TREE_CLS[FLAGS.sta_run_type]
    except KeyError, ex:
        raise Error(('Run type not recognized. Needs to be either of '
                     'regular, a_star or ida_star. You Entered: '
                     '%s') % FLAGS.sta_run_type)
    # start the STA algorithm
    try:
        task_container_objects = GetSubmittedBids(submitted_bids)
        output = RunSTA(ctree_cls, task_container_objects)
    except Exception or StandardError, ex:
        typ, val, tb = sys.exc_info()
        formatted_err_msg = traceback.format_exception(typ, val, tb)
        err_msg = '\nTop-level exception:\n%s' % ex
        err_msg += ''.join(formatted_err_msg)
        logging.error(err_msg)
        raise Error(err_msg)
    else:
        logging.info('Total Execution time: %s' % output['exe_time'])
        print >> sys.stdout, 'Completed.'
        print >> sys.stdout, 'Logs are at: %s' % log_filepath


if __name__ == "__main__":
    main(sys.argv)
