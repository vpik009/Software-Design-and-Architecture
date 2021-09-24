from APP.UserCollection import UserCollection
from LOGIC.CreateCloseOfferController import TutorCloseOfferController, \
    StudentCloseOfferController
from LOGIC.Mediator import CollectionMediator
from LOGIC.TutorOpenOfferController import TutorOpenOfferController


class CreateOfferControllerFactory:
    """
    A factory class to generate controller class depending on bid type and user type.
    """

    def __init__(self):
        """
        Empty constructor
        """
        pass

    def createCreateOfferController(self, bid, username, poster=None):
        """
        This is responsible to create a createOfferController class, depending on the bid type and user type.
        :param bid: bid instance
        :param username: this is the users username
        :param poster: poster of the offer
        """
        user = CollectionMediator().getUserByUserName(username)

        if bid.getType() == "OpenBid":
            return TutorOpenOfferController(bid, username)

        elif bid.getType() == "ClosedBid":
            if user.getType() == "tutor":
                return TutorCloseOfferController(bid, username)
            elif user.getType() == "student":
                return StudentCloseOfferController(bid, username, poster)
