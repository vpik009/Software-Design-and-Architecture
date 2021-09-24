from APP.User import User


class Tutor(User):
    """
    Child class of user that represents Tutor Object
    """

    def __init__(self, id, gName, fName, uName, iBids, qualifications, competencies, contracts, messages,
                 additionalInfo):
        """
        Constructor of the tutor class
        :param id: the id of the tutor
        :param gName: the tutor's given name
        :param fName: the tutor's first name
        :param uName: the tutor's username
        :param iBids: the tutor's initiated bids
        :param qualifications: the tutor's qualifications
        :param competencies: the tutor's competencies
        :param contracts: the tutor's contracts
        :param messages: the tutor's messages
        :param additionalInfo: the tutor's additionalInfo
        """
        super().__init__(id, gName, fName, uName, iBids, qualifications, competencies, contracts, messages)

        self.additionalInfo = additionalInfo # a python list of subscribed bid id's


    def getType(self):
        """
        getter of user type
        """
        return "tutor"

    def getAdditionalInfo(self):
        """
        getter of user's additionalInfo
        """
        return self.additionalInfo

    def addAdditionalInfo(self, id):
        '''
        method used to add to the users additional information
        :id: the id of the subscribed bid that is to be added to the tutor
        '''
        self.additionalInfo.append(id)
