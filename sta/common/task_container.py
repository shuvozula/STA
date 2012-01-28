__author__ = 'Spondon Saha'

from sta.common.bid_container import BidContainer


class Error(Exception):
    """Native exception class."""
    pass


class TaskContainer(object):
    """Container for storing task details and bids submitted for it."""

    def __init__(self, task_name):
        """Constructor.

        Arguments:
            task_name: The task id.

        Raises:
            None
        """
        self.task_name = task_name
        self.bidlist = []
        self.num_bids = 0

    def GetBidList(self):
        """Accessor for the list of bids stored.

        Arguments:
            None

        Returns:
            The list of bids submitted for this task.
        """
        return self.bidlist

    def IsTask(self, task_name):
        """Boolean method to verify task id.

        Arguments:
            task_name: a task-id.

        Returns:
            A boolean value.
        """
        if (self.task_name == task_name):
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
        bid_node = BidContainer(coalition, bid_value)
        self.bidlist.append(bid_node)
        self.num_bids += 1
