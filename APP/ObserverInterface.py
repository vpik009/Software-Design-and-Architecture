from abc import ABC, abstractmethod
"""
ABC: A helper class that creates an abstract class by deriving from ABC module
https://docs.python.org/3/library/abc.html
"""


class ObserverInterface(ABC):
    """
    Observer interface that is to be implemented by some specific subscribers.
    """

    @abstractmethod
    def updateMessages(self):
        """
        Abstract method for updating messages
        """
        pass

    @abstractmethod
    def updateBids(self):
        """
        Abstract method for updating bids
        """
        pass

    @abstractmethod
    def updateContracts(self):
        """
        Abstract method for updating contracts
        """
        pass