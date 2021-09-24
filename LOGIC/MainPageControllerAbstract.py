from abc import ABC, abstractmethod
"""
ABC: A helper class that creates an abstract class by deriving from ABC module
https://docs.python.org/3/library/abc.html
"""

from tkinter import *
"""
tkinter is the Python interface for GUI tool of tkinter.
https://docs.python.org/3/library/tkinter.html
"""

from LOGIC.Mediator import CollectionMediator


class MainPageControllerAbstract(ABC):
    """
    MainPageControllerAbstract class is an abstract class that holds common methods among all main pages
    to a specific controller. It has abstract methods that can be implemented.
    """

    @abstractmethod
    def __init__(self,username):
        self.user = username


    @abstractmethod
    def viewBids(self):
        """
        This is to redirect to a viewBids controller
        """
        pass

    def displayContractNotifications(self,view):
        user_contracts = CollectionMediator().getUserByUserName(self.user).getContracts()
        for con in user_contracts:
                notification = con.doState()
                if notification and con.getState().type() == "expiring": # if the state has to notify the user, and only applies to expiring contracts
                    Label(view.scrollable_frame, text=notification, font=("Arial", 10)).pack()

