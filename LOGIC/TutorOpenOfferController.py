from API.JSONAdapter import JSONAdapter
from GUI.Application import CreateOpenOfferPage, EditOpenOfferPage
import LOGIC
from LOGIC.CreateContract import CreateContract
from LOGIC.Mediator import CollectionMediator
from LOGIC.OfferController import OfferController


class EditOpenOfferController(OfferController):
    '''
    class used as a controller to edit open offers
    '''
    def __init__(self, bid, username):
        """
        A constructor of the class that initialize view, user, and bid.
        :param bid: a bid instance
        :param username: user's username
        """
        self.view = EditOpenOfferPage(self)
        self.user = username
        self.bid = bid
        print("from edit page",bid.getId())


    def goBack(self, view):
        """
        This method supports a page to be destroyed and go back to the main page.
        :param view: Page to be destroyed to avoid multiple windows.
        """
        view.root.destroy()
        # type = "tutor"  # tutors view controller is for tutors
        controller = LOGIC.ViewMonitorController.ViewMonitorController(self.user, timer=15000)

    def create(self, view, sesPerWeek, hoursPerSession, freeLesson, rate, payType, additional):
        """
        This create method returns a bid that a user should see
        :param view: a view to be redirected back to
        :param sesPerWeek: a session per week
        :param hoursPerSession: hours per session
        :param freeLesson: whether it has a free lesson or not
        :param rate: rate
        :param payType: pay type whether pay per hour or per session
        :param additional: additional information for the offer.
        """
        user = CollectionMediator().getUserByUserName(self.user)
        add = self.bid.getAdditional()  # list of additional information including offers

        # converting data to str
        free_lesson = "no"
        if freeLesson == 1:
            free_lesson = "yes"

        pay_type = "Per hour"
        if payType == 2:
            pay_type = "Per session"

        adapter = JSONAdapter.getInstance()


        response = adapter.patchOffer(self.bid.getId(), user.getId(), sesPerWeek, hoursPerSession, free_lesson, rate,
                                       pay_type, additional, add)

        self.goBack(view)

class TutorOpenOfferController(OfferController):  # just open offer controller
    """
    OpenOfferController is a child class of OfferController, which is for an open-bid offer.
    """

    def __init__(self, bid, username):
        """
        A constructor of the class that initialize view, user, and bid.
        :param bid: a bid instance
        :param username: user's username
        """
        self.view = CreateOpenOfferPage(self)
        self.user = username
        self.bid = bid

    def goBack(self, view):
        """
        This method supports a page to be destroyed and go back to the main page.
        :param view: Page to be destroyed to avoid multiple windows.
        """
        view.root.destroy()
        # type = "tutor"  # tutors view controller is for tutors
        controller = LOGIC.MainPageControllerFactory.MainPageControllerFactory().createMainPageController(
            CollectionMediator().getUserByUserName(self.user).getType(), self.user)

    def create(self, view, sesPerWeek, hoursPerSession, freeLesson, rate, payType, additional):
        """
        This create method returns a bid that a user should see
        :param view: a view to be redirected back to
        :param sesPerWeek: a session per week
        :param hoursPerSession: hours per session
        :param freeLesson: whether it has a free lesson or not
        :param rate: rate
        :param payType: pay type whether pay per hour or per session
        :param additional: additional information for the offer.
        """
        user = CollectionMediator().getUserByUserName(self.user)
        add = self.bid.getAdditional()  # list of additional information including offers

        # converting data to str
        free_lesson = "no"
        if freeLesson == 1:
            free_lesson = "yes"

        pay_type = "Per hour"
        if payType == 2:
            pay_type = "Per session"

        adapter = JSONAdapter.getInstance()

        response = adapter.createOffer(self.bid.getId(), user.getId(), sesPerWeek, hoursPerSession, free_lesson, rate,
                                       pay_type, additional, add)

        self.goBack(view)

    def buyOut(self, view):
        """
        buyOut is a method that allows the tutor user to buy out an open bid.
        :param view: the page the user is currently viewing
        """


        # get tutor competencies and qualifications
        col_mediator = CollectionMediator()
        tut_comp = col_mediator.getUserByUserName(self.user).getCompetency()
        tut_qual = col_mediator.getUserByUserName(self.user).getQualifications()

        # create a contract and set the bid to close-down
        # adapter = JSONAdapter.getInstance()
        # studentId = self.bid.getOwnerId()
        tutorId = col_mediator.getUserByUserName(self.user).getId()  # get the current user who is a tutor
        # subId = self.bid.getSubId()
        bid_additional = self.bid.getAdditional()
        offer =  {  # same bid details
            "sessionsPerWeek": bid_additional['sessionsPerWeek'],
            "hoursPerLesson": bid_additional['hoursPerLesson'],
            "freeLesson": bid_additional['freeLesson'],
            "rate": bid_additional['rate'],
            "rateType": bid_additional['rateType'],
            "additional": ""
        }
        contract_creator = CreateContract()
        dComp = bid_additional['desiredCompetency']  # to view the desired competency when renewing with a different tutor
        contract = contract_creator.createContract(self.bid.getOwnerId(), tutorId, self.bid.getSubId(), dComp, offer, manual=True)  # delegate task of contract creation to another class
        contract_creator.afterContract(self.bid.getId())  #  perform post contract creation actions on the bid
        contract_creator.signContract(contract.getId())

        # contract = adapter.postContract(studentId, tutorId, subId, offer, tut_comp, tut_qual)
        # adapter.closeBid(self.bid.getId())  # close down the bid
        self.goBack(view)

    def subscribeBid(self, view):
        """
        subscribeBid is a method that allows the tutor user to subscribe an open bid.
        :param view: the page the user is currently viewing
        """

        tutorId = CollectionMediator().getUserByUserName(self.user).getId()  # get the current user who is a tutor
        subscribed_bid = JSONAdapter.getInstance().updateUserSubscribedBids(tutorId, self.bid.getId())

        self.goBack(view)






