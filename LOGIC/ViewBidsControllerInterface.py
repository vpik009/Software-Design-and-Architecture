from abc import ABC, abstractmethod
"""
ABC: A helper class that creates an abstract class by deriving from ABC module
https://docs.python.org/3/library/abc.html
"""


class ViewBidsControllerInterface(ABC):

    @abstractmethod
    def goBack(self):
        """
        Go back to a page.
        """
        pass

    @abstractmethod
    def processBids(self):
        """
        returns the bids the user should see
        """
        pass

    @abstractmethod
    def goToBid(self):
        """
        Go to Bid Page
        """
        pass


