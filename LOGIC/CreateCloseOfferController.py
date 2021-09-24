import GUI
from API.JSONAdapter import JSONAdapter
from LOGIC.CreateContract import CreateContract
from LOGIC.Mediator import CollectionMediator
from LOGIC.OfferController import OfferController
import LOGIC
from tkinter import *
"""
tkinter is the Python interface for GUI tool of tkinter. 
https://docs.python.org/3/library/tkinter.html
"""



class TutorCloseOfferController(OfferController):  # has extra buyOut button
    """
    TutorCloseOfferController is a controller class that has a responsibility of creating messages on a bid, and displaying already existing messages on this bid.
    This is inherited from an abstract class of OfferController class and hence this is a child class.
    It mainly prints out a message history and add a message to a user and update with a new incoming message
    """

    def __init__(self, bid, username):
        """
        A constructor class that initializes the bid and user as well as the student message page view.
        :param bid: a bid for close offer.
        :param username: username is a username of the user.
        """

        self.view = GUI.Application.MessagePage(self)  # only a tutor can make a closed offer
        self.bid = bid
        self.user = username

    def goBack(self, view):
        """
        This method supports a page to be destroyed and go back to the main page.
        :param view: Page to be destroyed to avoid multiple windows.
        """
        view.root.destroy()
        controller = LOGIC.ViewBidsController.TutorViewBidsController(
            self.user)

    def create(self, view, ses_per_week,hours_ses,free_les,rate_inp,pay_type,additional):
        """
        This create method creates a new message and uploads it through JSONAdapter. then updates the view.
        :param view: view is the view page to print message history on.
        :param content: content is a content of a message to be sent
        """
        rate_type = "Per session"
        if pay_type == 1:
            rate_type = "Per hour"

        free_lesson = "no"
        if free_les == 1:
            free_lesson = "yes"

        adapter = JSONAdapter.getInstance()
        user = CollectionMediator().getUserByUserName(self.user)
        initiator = self.bid.getOwnerId()
        msg = adapter.postMessage(self.bid.getId(), user.getId(), ses_per_week,hours_ses,free_lesson,rate_inp,rate_type,additional, initiator)

        self.printMessageHistory(view)  # update message history

    def printMessageHistory(self, view):  # differs from tutor messageHistory
        """
        This method prints out a message history
        :param view: view is the view page to print message history on.
        """
        # get the initiator of the bid
        Label(view.scrollable_frame, text="\n\nMessage History:", font=("Arial Bold", 10)).pack()
        col_mediator = CollectionMediator()
        initiator = col_mediator.getUserById(self.bid.getOwnerId())  # get the intiator
        user = col_mediator.getUserByUserName(self.user)
        initiator_messages = initiator.getMessages()
        user_messages = user.getMessages()

        # only take messages specific to this bid
        initiator_messages_bid = []
        user_messages_bid = []
        for msg in initiator_messages:
            if msg.getBidId() == self.bid.getId():
                initiator_messages_bid.append(msg)

        for msg in user_messages:
            if msg.getBidId() == self.bid.getId():
                user_messages_bid.append(msg)

        initiator_messages = initiator_messages_bid
        user_messages = user_messages_bid

        Label(view.scrollable_frame, text="User Messages:", font=("Arial Bold", 12)).pack()

        for msg in user_messages:
            print(user.getUserName(),msg.stringifyContent())
            Button(view.scrollable_frame, text=user.getUserName() + ": " + msg.stringifyContent(),
                  font=("Arial Bold", 10)).pack()


        Label(view.scrollable_frame, text="Student Messages:", font=("Arial Bold", 12)).pack()

        for msg in initiator_messages:
            Button(view.scrollable_frame, text=initiator.getUserName() + ": " + msg.stringifyContent(),
                  font=("Arial Bold", 10)).pack()



class StudentCloseOfferController(OfferController):
    """
    StudentCloseOfferController is a controller class that has a responsibility of closing an offer.
    This is inherited from an abstract class of OfferController class and hence this is a child class.
    It mainly prints out a message history and add a message to a user and update with a new incoming message
    """

    def __init__(self, bid, username, poster):
        """
        A constructor class that initializes the bid and user as well as the student message page view.
        :param bid: the bid instance for the offer.
        :param username: username is a username of the user.
        :param poster: poster is a poster of the offer.
        """
        self.view = GUI.Application.MessagePage(self)  # only a tutor can make a closed offer
        self.bid = bid
        self.user = username
        self.poster = poster

    def goBack(self, view):
        """
        This method supports a page to be destroyed and go back to the main page.
        :param view: Page to be destroyed to avoid multiple windows.
        """
        view.root.destroy()
        controller = LOGIC.ViewBidsController.StudentViewBidsController(
            self.user)


    def create(self, view, ses_per_week,hours_ses,free_les,rate_inp,pay_type,additional):
        """
        This create method posts a message with a context and print out the message history by updating the user's
        message log.
        :param view: view is the view page to print message history on.
        :param content: content is a content of a message to be sent
        """
        rate_type = "Per session"
        if pay_type == 1:
            rate_type = "Per hour"

        free_lesson = "no"
        if free_les == 1:
            free_lesson = "yes"

        adapter = JSONAdapter.getInstance()
        user = CollectionMediator().getUserByUserName(self.user)
        initiator = self.bid.getOwnerId()
        msg = adapter.postMessage(self.bid.getId(), user.getId(), ses_per_week,hours_ses,free_lesson,rate_inp,rate_type,additional, initiator)

        self.printMessageHistory(view)  # update message history


    def printMessageHistory(self, view):
        """
        This method prints out a message history
        :param view: view is the view page to print message history on.
        """
        # get the initiator of the bid
        Label(view.scrollable_frame, text="\n\nMessage History:", font=("Arial Bold", 10)).pack()
        col_mediator = CollectionMediator()
        tutor = col_mediator.getUserById(self.poster)
        user = col_mediator.getUserByUserName(self.user)
        tutor_messages = tutor.getMessages()
        user_messages = user.getMessages()  # = the initiator of the bid

        # only take messages specific to this bid
        tutor_messages_bid = []
        user_messages_bid = []
        for msg in tutor_messages:
            if msg.getBidId() == self.bid.getId():
                tutor_messages_bid.append(msg)

        for msg in user_messages:
            if msg.getBidId() == self.bid.getId():
                user_messages_bid.append(msg)

        user_messages = user_messages_bid
        tutor_messages = tutor_messages_bid

        Label(view.scrollable_frame, text="User Messages:", font=("Arial Bold", 12)).pack()
        for msg in user_messages:
            Button(view.scrollable_frame, text=user.getUserName() + ": " + msg.stringifyContent(),
                  font=("Arial Bold", 10)).pack()

        Label(view.scrollable_frame, text="Tutor Messages:", font=("Arial Bold", 12)).pack()
        for msg in tutor_messages:
            tutor_msg = Button(view.scrollable_frame, text=tutor.getUserName() + ": " + msg.stringifyContent() + "\n Click to Accept offer",
                  font=("Arial Bold", 10), command=lambda msg=msg: self.accept(view, msg) )

            tutor_msg.pack()

    def accept(self,view, msg):
        '''
        method used to accept an offer, and delegates closing down and creating contract for the offer to JSONAdapter
        :param view: the page the user is currently viewing
        :param msg: the message that the user has accepted as an offer
        '''


        # get tutor competencies and qualifications
        contract_creator = CreateContract()

        dComp = self.bid.getAdditional()['desiredCompetency']
        contract = contract_creator.createContract(self.bid.getOwnerId(), msg.getPosterId(), self.bid.getSubId(), dComp, msg, manual=True) # delegate task to another class
        contract_creator.afterContract(self.bid.getId())  # perform post contract creation actions on the bid
        contract_creator.signContract(contract.getId())



        self.goBack(view)  # go back
