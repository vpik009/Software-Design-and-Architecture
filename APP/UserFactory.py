from abc import ABC, abstractmethod
"""
ABC: A helper class that creates an abstract class by deriving from ABC module
https://docs.python.org/3/library/abc.html
"""

from APP.Tutor import Tutor
from APP.Student import Student


class UserFactory(ABC):
    """
    Abstract user factory method used to make decisions on the type of user that is to be created
    """

    def __init__(self):
        pass

    def createUser(self, isTutor, id, gName, fName, uName, iBids, qualifications, competencies, contracts, messages,
                   additionalInfo):
        '''
        reads the type of user provided and creates the appropriate user class.
        This is assuming that the user can only be either a student or a tutor
        :param isTutor: where the user is tutor or not
        :param id: the id of the user
        :param gName: the user's given name
        :param fName: the user's first name
        :param uName: the user's username
        :param iBids: the user's initiated bids
        :param qualifications: the user's qualifications
        :param competencies: the user's competencies
        :param contracts: the user's contracts
        :param messages: the user's messages
        :param additionalInfo: the user's additional info
        '''
        user = None  # set the scope of the variable

        if isTutor:
            # create a tutor
            user = Tutor(id, gName, fName, uName, iBids, qualifications, competencies, contracts, messages,
                         additionalInfo)


        elif not isTutor:
            # create a student account

            user = Student(id, gName, fName, uName, iBids, qualifications, competencies, contracts, messages)

        return user
