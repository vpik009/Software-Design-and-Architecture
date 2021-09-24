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


class OfferController(ABC):
    """
    OfferController is an abstract class that has an abstract method and also a functionality of
    printing necessary information of a bid.
    """

    @abstractmethod
    def create(self):
        """
        an abstract method to be implemented by child classes
        """
        pass

    def printBidInfo(self, view):
        """
        This method prints an information of a bid.
        :param view: Page that is being viewed by the user at the time of using this controller class
        method used to print the information of the current bid on the page's scrollable frame
        """

        # get the current bid from the user collection
        # print bid's subject
        Label(view.scrollable_frame, text="Bid Information:", font=("Arial Bold", 10)).pack()

        subject = CollectionMediator().getSubjectById(self.bid.getSubId())
        add = self.bid.getAdditional()

        subName_label = Label(view.scrollable_frame, text="Subject Name: " + subject.getName(),
                              font=("Arial Bold", 10), bg='ivory').pack()

        subDes_label = Label(view.scrollable_frame, text="Subject Description: " + subject.getDescription(),
                             font=("Arial Bold", 10), bg='ivory').pack()

        try:  # might not have this additional field
            dComp_label = Label(view.scrollable_frame, text="Desired Competency: " + add['desiredCompetency'],
                                font=("Arial Bold", 10), bg='ivory').pack()

        except Exception:
            pass
        try:
            sesPerWeek_label = Label(view.scrollable_frame, text="Sessions per week: " + add['sessionsPerWeek'],
                                     font=("Arial Bold", 10), bg='ivory').pack()

        except Exception:
            pass
        try:
            hoursPerLesson_label = Label(view.scrollable_frame, text="Hours per lesson: " + add['hoursPerLesson'],
                                         font=("Arial Bold", 10), bg='ivory').pack()

        except Exception:
            pass
        try:
            rate_label = Label(view.scrollable_frame, text="Rate: " + add['rate'], font=("Arial Bold", 10),
                               bg='ivory').pack()

        except Exception:
            pass
        try:
            rateType_label = Label(view.scrollable_frame, text="Rate type: " + add['rateType'], font=("Arial Bold", 10),
                                   bg='ivory').pack()

        except Exception:
            pass
