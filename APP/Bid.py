from abc import ABC, abstractmethod
"""
ABC: A helper class that creates an abstract class by deriving from ABC module
https://docs.python.org/3/library/abc.html
"""

from datetime import datetime
"""
datetime provides functionalities for manipulating dates and times into various formats
https://docs.python.org/3/library/datetime.html
"""


class Bid(ABC):
    '''
    Abstract class that is responsible for holding common methods among all bid types.
    '''

    @abstractmethod
    def __init__(self, id, subId, ownerId, dateCreated, dateClosedDown, additional):
        self.id = id
        self.subjectId = subId
        self.dateCreated = datetime.strptime((dateCreated.replace("T", " ")).replace("Z",""), '%Y-%m-%d %H:%M:%S.%f') # datetime object
        self.dateClosedDown = dateClosedDown  # string
        self.ownerId = ownerId
        self.additional = additional


    def getId(self):
        '''
        method used to return the bid's id
        :output: the bid's id in the form a string
        '''
        return self.id

    def getSubId(self):
        '''
        method used to return the bid's subject id
        :output: the subject id of the subject the bid is for in the form of a string
        '''
        return self.subjectId

    def getDateCreated(self):
        '''
        method used to return bid's date of creation
        :output: the date the bid was created in the form of a datetime object
        '''
        return self.dateCreated

    def getDateClosedDown(self):
        '''
        method used to return the bid's date it was closed down on
        :output: the date of the bid's close down in the form of a string or a None if it is not closed down
        '''
        return self.dateClosedDown

    def getOwnerId(self):
        '''
        method used to return the bid owner's id
        :output: the owner's id in the form of a string
        '''
        return self.ownerId

    def getAdditional(self):
        '''
        method used to return the bid's additional information
        :output: additional information of the bid in the form of a JSON object
        '''
        return self.additional

    def getTime(self):
        '''
        method used to return the bid's time it is supposed to automatically close
        :output: the date and time the bid should automatically close at in the form of a datetime object
        '''
        return self.time

    def checkTime(self):
        '''
        used to check if its time for the bid to be closed down
        :output: a boolean True if its time to close down and False is not
        '''
        return self.getTime() <= datetime.now()

    def setDateClosedDown(self,set):
        '''
        Method that is used to set the closed down date of the bid
        :set: the date that is to be used for the closed down date of the bid
        '''
        self.dateClosedDown = set

    @abstractmethod
    def getType(self):
        '''
        Abstract method used to get the type of the bid
        '''
        pass
