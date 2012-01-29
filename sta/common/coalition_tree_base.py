
__author__ = 'Spondon Saha'

import sta.common.utils

class CoalitionTreeBase(object):
    """Base class for Coalition Tree variants."""

    def __init__(self):
        """Constructor"""
        pass

    def ConstructTree(self):
        """This is the base method, needs to be overriden by derived class."""
        raise NotImplementedError('Needs to be overriden by derived class!')

    def GetEligibleChildren(self, current_children, robots_on_path):
        """Gets the list of children not repeated on the current path.

        This is required to determine if the current path obeys the laws of
        Partition. If a child is repeated on the current path, then it violates
        the law.

        Arguments:
            current_children: A list of BidContainer objects.
            robots_on_path: A list of robots that are currently upstream in the
            bid-tree.

        Returns:
            A list of eligible coalitions that the IDA* algorithm can proceed
            further into using DFS.

        Raises:
            None
        """
        eligible_coalitions = []
        for child in current_children:
            if not sta.common.utils.HasMember(robots_on_path,
                                              child.GetCoalition()):
                eligible_coalitions.append(child)
        return eligible_coalitions

    def EstimateHeuristic(self, cbt_list, coalitions_on_path, all_tasks_on_path,
                          total_revenue):
        """Calculates the heuristic based on Sandholm's heuristic 3.1.

        This method calculates the sum of greatest contributions from coalitions
        of each task, that are not overlapping with the rest of the coalitions
        already on the path and then adds that to current contributions acrrued
        so far on the current path. This heuristic is therefore evaluated as
        g + hF.

        Arguments:
            coalitions_on_path: List of coalitions 
        """
        g = float(total_revenue)
        #hF = 0.0
        heur_cbt_list = []
        # populate 'heur_cbt_list' with all elements from 'cbt_list'
        # that are not in 'all_tasks_on_path'
        # Explanation: Get all taskNodes that have not been covered so far
        for task_node in cbt_list:
            if task_node.task_name not in all_tasks_on_path:
                heur_cbt_list.append(task_node)
        # build list of robots that are in heur_cbt_list
        robots_ahead_in_path = []
        cnodes_ahead_in_path = []
        for task_node in heur_cbt_list:
            list_of_bids = task_node.GetBidList()
            for cnode in list_of_bids:
                # add only unique robots to robots_ahead_in_path
                for robot in cnode.GetCoalition():
                    if robot not in robots_ahead_in_path:
                        robots_ahead_in_path.append(robot)
                # adds it as a list-object to cnodes_ahead_in_path
                cnodes_ahead_in_path.append(cnode)
        # remove duplicates: bench-marked the fastest,
        # look --> http://www.peterbe.com/plog/uniqifiers-benchmark
        #robots_ahead_in_path = {}.fromkeys(robots_ahead_in_path).keys() 
        # now iterate by each robot and pick all coalitions
        hF = 0.0
        for robot in robots_ahead_in_path:
            MaxHolder = []
            for cnode in cnodes_ahead_in_path:
                coalition = cnode.GetCoalition()
                # if the robot is a member of the current coalition,
                # then proceed
                if sta.common.utils.HasMember(coalition, [robot]):
                    # check if the coalition has any robots that are previously
                    # in the path 
                    onPath = False
                    for c in coalitions_on_path: 
                        if sta.common.utils.HasMember(coalition, c):
                            onPath = True
                            break
                    # if not, then collect its heuristic
                    # sandholm's heuristic 3.1, equation (23)
                    if not onPath:
                        bid_value = float(cnode.GetBidValue())
                        coalition_size = len(cnode.GetCoalition())
                        heuristic =  bid_value / coalition_size
                        MaxHolder.append(heuristic)
            if len(MaxHolder) > 0:
                hF += max(MaxHolder)
        # collect the heuristics for each node belonging to each task
        return (g + hF)
