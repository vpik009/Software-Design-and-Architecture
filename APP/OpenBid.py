from datetime import datetime, timedelta
"""
datetime provides functionalities for manipulating dates and times into various formats
https://docs.python.org/3/library/datetime.html
"""


from APP.Bid import Bid


class OpenBid(Bid):
    '''
    Class that represents the message object and holds its relevant fields
    '''

    def __init__(self, id, subId, ownerId, dateCreated, dateClosedDown, additional):
        '''
        Constructor that initializes the instance of CloseBid
        :param id: the id of the bid that is to be created
        :param subId: the subject id that the bid is for
        :param ownerId: the id of the owner of the bid (initiator)
        :param dateCreated: the date the bid was created on
        :param dateClosedDown: the date the bid was closed down on
        :param additional: additional information on the bid ion the form of a json

        '''
        super().__init__(id, subId, ownerId, dateCreated, dateClosedDown, additional)
        # time is an object to be able to compare
        self.time = self.dateCreated+timedelta(minutes=30)  # date & time of creation + 30 min


    def getType(self):
        '''
        method returns a string specifying the type of bid
        :return: a string that specifies the type of bid this is
        '''
        return "OpenBid"




