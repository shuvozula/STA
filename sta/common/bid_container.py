__author__ = 'Spondon Saha'


class Error(Exception):
    """Native exception class."""
    pass


class BidContainer(object):
    """Container for storing bid details."""

    def __init__(self, coalition, bid):
        """Constructor. Sets the coalition and bid values at init.

        Arguments:
            coalition: A list of robot-ids that submitted the bid
            bid: the bid value placed by the coalition.

        Returns:
            None

        Raises:
            None
        """
        self.coalition = coalition
        self.bid = bid
        
    def GetCoalition(self):
        """Accessor for coalition class variable.

        Arguments:
            None

        Returns:
            The list of robot-members/coalition.
        """
        return self.coalition

    def GetBidValue(self):
        """Accessor for fetching the bid-value.

        Arguments:
            None

        Returns:
            The bid value that the coalition submitted in the auction.
        """
        return self.bid
