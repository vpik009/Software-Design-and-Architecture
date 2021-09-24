from APP.User import User


class Student(User):
    """
    Child class of user that represents Student Object
    """

    def __init__(self,id,gName, fName, uName, iBids, qualifications, competencies, contracts, messages):
        """
        Constructor of the student class
        :param id: the id of the student
        :param gName: the student's given name
        :param fName: the student's first name
        :param uName: the student's username
        :param iBids: the student's initiated bids
        :param qualifications: the student's qualifications
        :param competencies: the student's competencies
        :param contracts: the student's contracts
        :param messages: the student's messages
        """
        super().__init__(id,gName, fName, uName, iBids, qualifications, competencies, contracts, messages)


    def getType(self):
        """
        getter of user type
        """
        return "student"


