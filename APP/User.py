from abc import ABC, abstractmethod
"""
ABC: A helper class that creates an abstract class by deriving from ABC module
https://docs.python.org/3/library/abc.html
"""

class User(ABC):
    '''
    Abstract class
    '''

    @abstractmethod
    def __init__(self,id,gName, fName, uName, iBids, qualifications, competencies, contracts, messages):
        """
        Constructor of the user class
        :param id: the id of the user
        :param gName: the user's given name
        :param fName: the user's first name
        :param uName: the user's username
        :param iBids: the user's initiated bids
        :param qualifications: the user's qualifications
        :param competencies: the user's competencies
        :param contracts: the user's contracts
        :param messages: the user's messages
        """
        self.id = id
        self.givenName = gName
        self.familyName = fName
        self.userName = uName
        self.initiatedBids = iBids
        self.qualifications = qualifications
        self.competencies = competencies
        self.contracts = contracts
        self.messages = messages




    def getId(self):
        """
        getter of user's id
        """
        return self.id

    def getUserName(self):
        """
        getter of user's username
        """
        return self.userName


    def getGivenName(self):
        """
        getter of user's given name
        """
        return self.givenName

    def getFamilyName(self):
        """
        getter of user's family name
        """
        return self.familyName

    def getBids(self):
        """
        getter of user's bids
        """
        #return a copy of the initiated bids??
        return self.initiatedBids

    def setBids(self,bids):
        """
        setter of user's bids
        :param bids: the users initiated bids in a list
        """
        self.initiatedBids = bids

    def addBids(self, bid):
        """
        add bids to the initated bids.
        :param bid: user's bid
        """
        self.initiatedBids.append(bid)

    def getCompetency(self):
        """
        getter of the competency
        """
        #return a copy of competencies??
        return self.competencies


    def setCompetency(self,competency):
        """
        setter of the competency
        :param competency: user's competency
        """
        self.competencies = competency

    def getQualifications(self):
        """
        getter of the qualification
        """
        #return a copy of qualifications??
        return self.qualifications

    def setQualifications(self,qualification):
        """
        setter of the qualification
        :param qualification: user's qualification
        """
        self.qualifications = qualification

    def getContracts(self):
        """
        getter of the contracts
        """
        return self.contracts

    def setContracts(self, contracts):
        """
        setter of the contracts
        :param contracts: user's contracts
        """
        self.contracts = contracts

    def addContracts(self, contracts):
        """
        add contracts to the contracts list
        :param contracts: user's contracts
        """
        self.contracts.append(contracts)

    def getMessages(self):
        """
        getter of the messages
        """
        return self.messages


    def setMessages(self,mes):
        """
        setter of the messages
        :param mes: user's messages
        """
        self.messages = mes

    def addMessage(self,msg):
        """
        add messages to the messages list.
        :param msg: user's messages
        """
        self.messages.append(msg)



    @abstractmethod
    def getType(self):
        """
        abstract method of user's type whether a student or tutor
        """
        pass

