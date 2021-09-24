from APP.SubjectCollection import SubjectCollection
from APP.UserCollection import UserCollection


class CollectionMediator:
    """
    A mediator class for collection objects to allow the classes from this package to make calls to this object
    (reduce coupling)
    """

    def __init__(self, users=None,subjects=None):
        """
        :param users: users to be processed with for UserCollection
        :param subjects: subjects to be processed with for subjectCollection
        """
        self.userCollection = UserCollection.getInstance(users)
        self.subjectCollecion = SubjectCollection.getInstance(subjects)

    def getAllUsers(self):
        """
        this gets all the users from the UserCollection that holds a list of User Object.
        """
        return self.userCollection.getAll()

    def findUsersBid(self,id):
        """
        this method is used to find a bid from the user collection, consisting of a list of User objects
        :param id: id of a bid
        """
        return self.userCollection.findBid(bid_id=id)

    def getUserByUserName(self,username):
        """
        this method is used to retrieve a specific user from the user collection, consisting of a list of User objects with
        username.
        :param username: name of a user
        """
        return self.userCollection.getUserByUserName(username)

    def getUserById(self,id):
        """
        this method is used to retrieve a specific user from the user collection, consisting
        of a list of User objects with user id.
        :param id: id of a user
        """
        return self.userCollection.get(id)

    def getSubjectById(self, id):
        """
        this method is used to retrieve a specific subject from the subject collection, consisting
        of a list of Subject objects with subject id.
        :param id: id of a subject
        """
        return self.subjectCollecion.getSubjectById(id)

    def getSubjectByName(self,name):
        """
        this method is used to retrieve a specific subject from the subject collection, consisting
        of a list of Subject objects with subject name.
        :param name: name of a subject
        """
        return self.subjectCollecion.getSubjectByName(name)

    def addSubject(self,posted_subject):
        """
        this method is used to add a subject to the Subject Collection.
        :param posted_subject: a subject to be posted to the subject collection
        """
        return self.subjectCollecion.addSubject(posted_subject)


