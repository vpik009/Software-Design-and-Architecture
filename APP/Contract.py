from datetime import datetime
"""
datetime provides functionalities for manipulating dates and times into various formats
https://docs.python.org/3/library/datetime.html
"""


from APP import ContractState


class Contract:
    '''
    A class that represents a contract object
    '''

    def __init__(self, id, ownerId, subject_id, sParty, dCreated, dSigned, eDate, paymentI=None, lessonI=None, additionalI=None):
        '''
        Contructor to instantiate contract instances
        :param id: the id of the contract
        :param ownerId: the id of the student party of the contract
        :param subject_id: the id of the subject the contract is for
        :param sParty: the id of the tutor party of the contract
        :param dCreated: the date the contract was created
        :param dSigned: the date the contract was signed
        :param eDate: the date the contract is set to expire on
        :param paymentI: extra information on the payment in JSON
        :param lessonI: extra information on the lesson in JSON
        :param additionalI: general additional information on the contract in JSON
        '''
        self.id = id
        self.ownerId = ownerId
        self.subjectId = subject_id
        self.secondPartyId = sParty
        self.dateCreated = datetime.strptime((dCreated.replace("T", " ")).replace("Z",""), '%Y-%m-%d %H:%M:%S.%f') # datetime object
        self.dateSigned = dSigned #datetime.strptime((dSigned.replace("T", " ")).replace("Z",""), '%Y-%m-%d %H:%M:%S.%f') # datetime object
        self.expiryDate = datetime.strptime((eDate.replace("T", " ")).replace("Z",""), '%Y-%m-%d %H:%M:%S.%f') # datetime object

        self.additionalInfo = additionalI
        self.paymentInfo = paymentI
        self.lessonInfo = lessonI

        self.state = ContractState.PendingContractState()  # initialize the contract's state to be pending

    def doState(self):
        '''
        Method that performs the actions of the current contract state and changed the state to the next state if ready
        :output: None if the current state doesnt have any actions, String if the current action has a notification text
        '''
        return self.state.doState(self)  # update its own state if necessary and perform the current state

    def setState(self, state):
        '''
        Sets the contracts state
        :state: the new state of the contract.
        '''
        self.state = state

    def getState(self):
        '''
        A getter for getting the instance of the state the contract is currently in
        '''
        return self.state

    def getId(self):
        '''
        A getter to get the id of the contract object
        :output: the id of the contract in the form of a string
        '''
        return self.id

    def getOwnerId(self):
        '''
        A getter to get the id of the student party of the contract
        :output: the id of student party of the contract as a string
        '''
        return self.ownerId

    def getSecondPartyId(self):
        '''
        A getter to get the id of the tutor party of the contract
        :output: the id of the tutor party of the contract as a string
        '''
        return self.secondPartyId

    def getSubjectId(self):
        '''
        A getter to get the id of the subject the contract is for
        :output: the id of the subject the contract is for as a string
        '''
        return self.subjectId

    def getDateCreated(self):
        '''
        A getter to get the date the contract was created on
        :output: the date the contract was created on as a string
        '''
        return self.dateCreated

    def getDateSigned(self):
        '''
        A getter to get the date the contract was signed on
        :output: the date the contract was signed on as a string
        '''
        return self.dateSigned

    def getExpiryDate(self):
        '''
        A getter to get the date the contract is to expire on
        :output: the date the contract is to expire on as a string
        '''
        return self.expiryDate

    def stringifyDetails(self):
        '''
        Method that is used to stringify the details of the offer the contract for signed for in user friendly string format
        '''
        return_string = "Sessions per week:" + self.additionalInfo['sessionsPerWeek']
        return_string += "\nHours per session:" + self.additionalInfo['hoursPerLesson']
        return_string += "\nRate:" + self.additionalInfo['rate']
        return_string += "\nPaid:" + self.additionalInfo['rateType']
        return return_string

    def getAdditionalInfo(self): # added to get desired competency
        '''
        Returns the additional information of the contract
        '''
        return self.additionalInfo


    def isExpired(self):
        '''
        Checks if the current contract is expired
        :output: True if expired, False otherwise
        '''
        if self.expiryDate <= datetime.now():
            return True
        return False
