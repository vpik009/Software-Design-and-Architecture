from datetime import datetime
"""
datetime provides functionalities for manipulating dates and times into various formats
https://docs.python.org/3/library/datetime.html
"""

from APP.ObserverInterface import ObserverInterface


class UserCollection(ObserverInterface):
    '''
    Class responsible for holding the instances of all the users and functionality to update user information in the collection
    '''

    _instance = None

    def __init__(self, users):
        '''
        constructor of the collection of user objects
        :users: A list of user objects
        '''
        self.users = users

    @classmethod
    def getInstance(cls, users=[]):
        """
        Singleton of , collection that keeps the cache
        """
        if not cls._instance:
            # doesnt exist
            cls._instance = UserCollection(users)  # create a user collection
        return cls._instance  # return the instance

    def getAll(self):
        """
        getting all users
        """
        return self.users

    def getUserByUserName(self, userName):
        '''
        Can search a user by username
        If user exists return True, else return False
        :param userName: user's userName
        '''
        user = None
        for u in self.users:
            if u.getUserName() == userName:
                user = u
        return user

    def get(self, id):
        '''
        Can search a user by Id
        If not found return None else return the user
        :param id: user's id
        '''
        for u in self.users:
            if u.getId() == id:
                return u
        return None

    def updateMessages(self, id, data):
        '''
        update messages once the postMessage is called.
        :param id: the id of the user who is to undergo updates
        :param data: the new version of data that the user should hold
        '''
        for i in range(len(self.users)):
            if self.users[i].getId() == id:  # find a user with the provided id
                self.users[i].addMessage(data)

    def updateContracts(self, id, data, patch=False):
        '''
        update contracts once the post contracts is called.
        :param id: the id of the user who is to undergo updates.
        :param data: the new version of data that the user should hold.
        :param patch: parameter specifyin if an existing contract is being updated( patch = contract id). Or new one is being added (patch = False)
        '''
        if patch == False:
            for i in range(
                    len(self.users)):  # checking with else if seems necessary since there is only a single update method
                if self.users[i].getId() == id:  # find a user with the provided id
                    self.users[i].addContracts(data)
        else:
            for user in self.users:
                user_con = user.getContracts()
                for i in range(len(user_con)):
                    if user_con[i].getId() == data.getId():
                        user_con[i] = data  # swap the contract for a newer version



    def closeBid(self, bid_id):
        '''
        Used to update the bid in a certain user to to close that bid down
        :param bid_id: the id of the bid that is to be closed down
        '''
        for i in range(
                len(self.users)):  # checking with else if seems necessary since there is only a single update method
            users_bids = self.users[i].getBids()
            for bid in users_bids:
                if bid.getId() == bid_id:
                    bid.setDateClosedDown(datetime.now())

    def findBid(self, bid_id):
        '''
        Used to update the bid in a certain user to to close that bid down
        :param bid_id: the id of the bid that is to be closed down
        '''
        for i in range(
                len(self.users)):  # checking with else if seems necessary since there is only a single update method
            users_bids = self.users[i].getBids()
            for bid in users_bids:
                if bid.getId() == bid_id:
                    return bid

    def addSubedBid(self, tutorId, bidId):
        for user in self.users:
            if user.getId() == tutorId:
                user.addAdditionalInfo(bidId)

    def updateBids(self, id, data, offer=None):
        '''
        update bids once the post bids is called.
        :id: the id of the user who is to undergo updates
        :data: the new version of data that the user should hold
        :offer: parameter that holds the offer that is to be updated in an existing bid. If None, add new bid
        '''
        for i in range(
                len(self.users)):  # checking with else if seems necessary since there is only a single update method
            if self.users[i].getId() == id:  # find a user with the provided id
                if offer:  # only adding an offer to a bid
                    users_bids = self.users[i].getBids()
                    for j in range(len(users_bids)):
                        # find the bid that is to be updated
                        if users_bids[j].getId() == data.getId():
                            users_bids[j] = data  # replace the bid

                else:  # if not an offer, must be adding a new bid
                    self.users[i].addBids(data)

