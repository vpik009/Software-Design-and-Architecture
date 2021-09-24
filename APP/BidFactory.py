from abc import ABC, abstractmethod
"""
ABC: A helper class that creates an abstract class by deriving from ABC module
https://docs.python.org/3/library/abc.html
"""


from APP.CloseBid import CloseBid
from APP.OpenBid import OpenBid

'''
Class responsbile for decision making and creating the correct bid class
If another bid is added, the only code that will need to change is inside this factory class. Promoting the open/closed principle
'''
class BidFactory(ABC):
    '''
    Abstract bid factory method used to make decisions on the type of bid that is to be created
    '''
    def __init__(self):
        '''
        empty constructor
        '''
        pass


    def createBid(self,type, id, subId, ownerId, dateCreated, dateClosedDown, additionalInfo):
        '''
        method that reads the type of bid provided and creates the appropriate bid instance
        :param type: The type of bid that is to be created
        :param id: the id of the bid that is to be created
        :param subId: the subject id that the bid is for
        :param ownerId: the id of the owner of the bid (initiator)
        :param dateCreated: the date the bid was created on
        :param dateClosedDown: the date the bid was closed down on
        :param additionalInfo: additional information on the bid ion the form of a json
        :param messages: optional parameter, the messages the bid has
        :output: the appropriate bid instance
        '''
        bid = None  # set the scope of the variable
        if type == "open":
            # create the open bid
            bid = OpenBid(id, subId, ownerId, dateCreated, dateClosedDown, additionalInfo)

        elif type == "close":
            # create a close bid
            bid = CloseBid(id, subId, ownerId, dateCreated, dateClosedDown, additionalInfo)

        return bid


