from abc import ABC, abstractmethod
"""
ABC: A helper class that creates an abstract class by deriving from ABC module
https://docs.python.org/3/library/abc.html
"""

from GUI.Application import ViewBidsPage
import LOGIC.MainPageControllerFactory
from LOGIC.CheckBidValidity import CheckBidValidity
from LOGIC.CreateContract import CreateContract
from LOGIC.CreateOfferControllerFactory import CreateOfferControllerFactory
from LOGIC.Mediator import CollectionMediator
from LOGIC.ViewBidsControllerInterface import ViewBidsControllerInterface
import LOGIC.LoginController
from tkinter import *
"""
tkinter is the Python interface for GUI tool of tkinter.
https://docs.python.org/3/library/tkinter.html
"""


class StudentViewBidsController(ViewBidsControllerInterface):
    """
    StudentViewBidsController is a class that implements ViewBidsControllerInterface that is
    mainly to process bids and redirect to a different page.
    """

    def __init__(self, username):
        """
        Constructor that initializes view and user.
        :param username: user's username
        """
        self.view = ViewBidsPage(self)
        self.user = username

    def goBack(self, view):
        """
        This method supports a page to be destroyed and go back to the main page.
        :param view: Page to be destroyed to avoid multiple windows.
        """
        view.root.destroy()
        type = "student"  # tutors view controller is for tutors
        controller = LOGIC.MainPageControllerFactory.MainPageControllerFactory().createMainPageController(type,
                                                                                                          self.user)

    def processBids(self, view):
        """
        This processes all user bids and displays it on the page.
        :param view: page the bid to be displayed on.
        """
        user = CollectionMediator().getUserByUserName(self.user)
        user_bids = user.getBids()
        for bid in user_bids:
            if not CheckBidValidity().checkPrintValidity(
                    bid) and not bid.getDateClosedDown():  # if bid didnt close down
                Button(view.scrollable_frame, text=bid.getType() + "\n Bid ID:" + bid.getId(), font=("Arial", 10),
                       command=lambda bid=bid: self.goToBid(view, bid)).pack()

    def goToBid(self, view, bid):
        """
        goToBid is a method that redirects to a controller depending on its bid type
        :param view: a previous window to be destroyed
        :param bid: a bid to view a list of offers on
        """
        view.root.destroy()
        if bid.getType() == "OpenBid":
            controller = StudentViewOpenOffersController(self.user,
                                                         bid)  # take them to view a list of offers on the bid
        elif bid.getType() == "ClosedBid":
            controller = ViewCloseOffersController(self.user, bid)  # take them to view a list of offers on the bid


class ViewOffersControllerInterface(ABC):
    """
    ViewOffersControllerInterface is an interface for the offer controllers to implement its abstract methods.
    """

    @abstractmethod
    def processBids(self):
        """
        To process bids
        """
        pass

    @abstractmethod
    def goBack(self):
        """
        To go back to a different page
        """
        pass


class StudentViewOpenOffersController(ViewOffersControllerInterface):
    """
    ViewOpenOffersController is a class that implements ViewBidsControllerInterface that is
    mainly to process and accept offer on an open bid and redirect to a different page.
    """

    def __init__(self, username, bid):
        """
        Constructor that initializes view, user, and bid.
        :param username: user's username
        :param bid: bid
        """
        self.view = ViewBidsPage(self)
        self.user = username
        self.bid = bid

    def goBack(self, view):
        """
        This method supports a page to be destroyed and go back to the main page.
        :param view: Page to be destroyed to avoid multiple windows.
        """
        view.root.destroy()
        type = "student"  # this view page is only used by student
        controller = LOGIC.MainPageControllerFactory.MainPageControllerFactory().createMainPageController(type,
                                                                                                          self.user)

    def processBids(self, view):
        """
        This processes a user offer and display it in the specific page.
        :param view: a offer information to be displayed on.
        """
        # get all the bids related to this bid and all the messages related to this bid
        offer_list = []

        try:
            additional = self.bid.getAdditional()['bids']

            for offer in additional:
                offer_list.append(offer)

        except Exception:  # the bid does not have offers, then skip it
            pass

        for offer in offer_list:  # print the offers on user's bids
            Button(view.scrollable_frame,
                   text="Weekly Sessions: " + offer['sessionsPerWeek'] + "\nHours/Session:" + offer['hoursPerLesson']
                        + "\nFree Lesson:" + offer['freeLesson'] + "\nRate:" + offer['rate'] + "\nRate Type:" + offer[
                            'rateType'] + "\nExtra:" + offer['additional'] + "\n\nClick to Accept Offer",
                   font=("Arial", 10),
                   command=lambda offer=offer: self.accept(view, self.bid.getOwnerId(), offer['tutorId'],
                                                           self.bid.getSubId(), offer)).pack(fill=BOTH, expand=True)

    def accept(self, view, studentId, tutorId, subId, offer):
        """
        method used to accept the offer by student from a tutor
        Delegates the task of creating a contract to the JSONAdapter
        :param view: the instance of the current page
        :param studentId: a accepted bid of student's student id
        :param tutorId: a accepted bid of tutor's tutor id
        :param subId: a accepted bid of subject's subject id
        :param offer: an offer for the bid
        """
        # create a contract and set the bid to close-down
        # get tutor competencies and qualifications
        contract_creator = CreateContract()
        dComp = self.bid.getAdditional()['desiredCompetency']  # to view the desired competency when renewing with a different tutor
        contract = contract_creator.createContract(self.bid.getOwnerId(), tutorId, self.bid.getSubId(), dComp, offer,manual=True)  # delegate task to another class
        contract_creator.afterContract(self.bid.getId())
        contract_creator.signContract(contract.getId())

        self.goBack(view)  # go back


class ViewCloseOffersController(ViewOffersControllerInterface):
    """
    ViewCloseOffersController is a class that implements ViewBidsControllerInterface that is
    mainly to process offers on a close bid and redirect to a different page.
    Only for student since tutors cant see other's messages
    """

    def __init__(self, username, bid):
        """
        Constructor that initializes view, user, and bid.
        :param username: user's username
        :param bid: bid
        """
        self.view = ViewBidsPage(self)
        self.user = username
        self.bid = bid

    def goBack(self, view):
        """
        This method  supports a page to be destroyed and go back to the main page.
        :param view: Page to be destroyed to avoid multiple windows.
        """
        view.root.destroy()
        controller = LOGIC.MainPageControllerFactory.MainPageControllerFactory().createMainPageController(
            CollectionMediator().getUserByUserName(self.user).getType(),
            self.user)

    def processBids(self, view):
        """
        This processes a user bid and display it in the specific page.
        :param view: a bid information to be displayed on.
        """
        # get all the messages related to this bid

        col_mediator = CollectionMediator()
        us = col_mediator.getUserByUserName(self.user)

        msg_list = []
        users = col_mediator.getAllUsers()
        for user in users:
            msg_list += user.getMessages()

        msg_list_bid = []
        for msg in msg_list:  # only keep those that are for this bid and arent the user
            if msg.getBidId() == self.bid.getId() and msg.getPosterId() != us.getId():
                msg_list_bid.append(msg)

        for i in range(len(msg_list_bid)):  # have to make sure they dont repeat multiple times
            j = 0
            while j < i:
                if msg_list_bid[j].getPosterId() != msg_list_bid[
                    i].getPosterId():  # if the user was previously posted dont post again
                    button = Button(view.scrollable_frame,
                                    text="Tutor ID: " + msg_list_bid[i].getPosterId() + "\n Bid ID:" + self.bid.getId(),
                                    font=("Arial", 10),
                                    command=lambda msg=msg_list[i]: self.goToBid(view, msg_list_bid[i].getPosterId()))
                    button.pack()
                j += 1
            if j == 0:  # if j == 0 no possible same tutor previously.
                button = Button(view.scrollable_frame,
                                text="Tutor ID: " + msg_list_bid[i].getPosterId() + "\n Bid ID:" + self.bid.getId(),
                                font=("Arial", 10),
                                command=lambda msg=msg_list[i]: self.goToBid(view, msg_list_bid[i].getPosterId()))
                button.pack()

    def goToBid(self, view, poster):
        """
        goToBid is a method that redirects to a offer page
        :param view: a previous window to be destroyed
        :param poster: poster of the bid
        """
        view.root.destroy()
        controller = CreateOfferControllerFactory().createCreateOfferController(self.bid, self.user, poster)


class TutorViewBidsController(ViewBidsControllerInterface):
    """
    TutorViewBidsController is a class that implements ViewBidsControllerInterface that is
    mainly to process bids and redirect to a different page.
    """

    def __init__(self, username):
        self.view = ViewBidsPage(self)
        self.user = username

    def goBack(self, view):
        """
        This method supports a page to be destroyed and go back to the main page.
        :param view: Page to be destroyed to avoid multiple windows.
        """
        view.root.destroy()
        type = "tutor"  # tutors view controller is for tutors only
        controller = LOGIC.MainPageControllerFactory.MainPageControllerFactory().createMainPageController(type,
                                                                                                          self.user)

    def processBids(self, view):
        """
        This method processes all the bids for the tutor to see and displays it on the page.
        :param view: Page to display bid information on.
        """
        # get all bids from user collection
        col_mediator = CollectionMediator()
        users = col_mediator.getAllUsers()
        user_comp = col_mediator.getUserByUserName(self.user).getCompetency()
        bid_list = []
        for user in users:
            bid_list += user.getBids()

        for bid in bid_list:
            if not CheckBidValidity().checkPrintValidity(bid) and not bid.getDateClosedDown():
                for comp in user_comp:
                    dComp = bid.getAdditional()['desiredCompetency']
                    if comp.getSubjectId() == bid.getSubId() and comp.getLevel() >= (int(
                            dComp) + 2):  # display bid if user has a competency for the subject and comp >= bid comp +2
                        Button(view.scrollable_frame, text=bid.getType() + "\n Bid ID:" + bid.getId(),
                               font=("Arial", 10),
                               command=lambda bid=bid: self.goToBid(view, bid)).pack()

    def goToBid(self, view, bid):
        """
        goToBid is a method that redirects to a controller depending on its bid type
        :param view: a previous window to be destroyed
        :param bid: a bid to create an offer for
        """
        view.root.destroy()

        if bid.getType() == "OpenBid":  # allow the tutor to view other tutor' offers
            controller = TutorViewOpenOffersController(self.user, bid)
        else:  # otherwise let the factory decide
            controller = CreateOfferControllerFactory().createCreateOfferController(bid, self.user)


class TutorViewOpenOffersController(ViewOffersControllerInterface):
    """
    ViewOpenOffersController is a class that implements ViewBidsControllerInterface that is
    mainly to process and accept bids and redirect to a different page.
    """

    def __init__(self, username, bid):
        """
        Constructor that initializes view, user, and bid.
        :param username: user's username
        :param bid: bid
        """
        self.view = ViewBidsPage(self)
        self.user = username
        self.bid = bid

    def goBack(self, view):
        """
        This method supports a page to be destroyed and go back to the main page.
        :param view: Page to be destroyed to avoid multiple windows.
        """
        view.root.destroy()
        controller = LOGIC.MainPageControllerFactory.MainPageControllerFactory().createMainPageController(
            CollectionMediator().getUserByUserName(self.user).getType(), self.user)

    def processBids(self, view):
        """
        This processes all the bid's offers and displays it on a page.
        :param view: Page the offer information it to be displayed on.
        """
        # get all the bids related to this bid and all the messages related to this bid
        offer_list = []
        Button(view.root,
               text="Create Your Offer",
               font=("Arial", 15),
               command=lambda: self.createOffer(view, self.bid)).place(x=500, y=710)

        try:
            additional = self.bid.getAdditional()['bids']

            for offer in additional:
                offer_list.append(offer)

        except Exception:  # the bid does not have offers, then skip it
            pass

        for offer in offer_list:  # print the offers on user's bids
            Button(view.scrollable_frame,
                   text="Weekly Sessions: " + offer['sessionsPerWeek'] + "\nHours/Session:" + offer['hoursPerLesson']
                        + "\nFree Lesson:" + offer['freeLesson'] + "\nRate:" + offer['rate'] + "\nRate Type:" + offer[
                            'rateType'] + "\nExtra:" + offer['additional'],
                   font=("Arial", 10), ).pack()

    def createOffer(self, view, bid):
        """
        method used to redirect the tutor to a page where he can creat an offer on the current bid
        :param view: the instance of the current page that is to be destroyed
        :param bid: the bid the offer is to be made for
        """
        view.root.destroy()
        CreateOfferControllerFactory().createCreateOfferController(bid, self.user)
