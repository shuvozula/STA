__author__ = 'Spondon Saha'

from bidcontainer import BidNode


class Error(Exception):
    """Native exception class."""
    pass


class TaskNode(object):
    """Container for storing task details and bids submitted for it."""

    def __init__(self, taskname):
        """Constructor.

        Arguments:
            taskname: The task id.

        Raises:
            None
        """
        self.taskname = taskname
        self.bidlist = []

    def GetBidList(self):
        """Accessor for the list of bids stored.

        Arguments:
            None

        Returns:
            The list of bids submitted for this task.
        """
        return self.bidlist

    def IsTask(self, task):
        """Boolean method to verify task id.

        Arguments:
            task: a task-id.

        Returns:
            A boolean value.
        """
        if (self.taskname == task):
            return True
        else:
            return False

    def AddBid(self, coalition, bid_value):
        """Adds a bid that was submitted for this task.

        Arguments:
            coalition: A list of robot-ids.
            bid_value: Bid value submitted for the task.

        Returns:
            None
        """
        bid_node = BidNode(coalition, bid_value)
        self.bidlist.append(bid_node)
