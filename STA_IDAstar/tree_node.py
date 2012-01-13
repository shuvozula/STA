__author__ = 'Spondon Saha'


class Error(Exception):
    """Native exception class."""
    pass


class TreeNode(object):
    """Node object used for building the STA tree."""

    def __init__(self, name, bid_node, robots_on_path):
        """Constructor.

        Arguments:
            name: a tree-node id.
            bid: A bidcontainer.BidNode object containing bid-value information
            and robot coalition members that submitted that bid.
            robots_on_path: All the robots that so far exist on the current
            path.

        Raises:
            None
        """
        self.name = name
        self.totalRevenue = 0
        self.parent = None
        self.children = []
        self.blocked = True
        self.heuristicVal = 0.0
        self.futureNodes = None
        self.winnerOnPath = False
        # - - - - - - - - - - - - - -
        self.bid_node = bid_node
        self.coalitionsOnPath = []
        self.robots_on_path = robots_on_path
        # - - - - - - - - - - - - - -
        self.memberOfTask = None
        # stores the list of tasks excluding task-levels taken up by dummy nodes
        self.tasksOnPath = []
        # stores the list of all the tasks that are used up on the current path
        self.allTasksOnPath = [] 
        
        
        
        
        
