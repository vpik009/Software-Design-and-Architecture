

class Observer:

    def __init__(self, subscribers):
        self.subscribers = []  # initialize empty list to hold subscribers

    def subscribe(self, sub):
        """
        Subscribe method to subscribe those who will get notified.
        sub: Subscriber of the publisher to be notified at runtime
        """
        if sub not in self.subscribers:  # only append if doesnt already exist
            self.subscribers.append(sub)

    def notifySubscriberMessages(self, userId, data):
        """
        This method is used to notify and update the users in related collections.
        userId: Id of the user
        data: incoming message data from a user that is to be updated to a subscriber
        """
        for observer in self.subscribers:
            observer.updateMessages(userId, data)

    def notifySubscriberContracts(self, userId, data, tutorId=None, patch=False):
        """
        This method is used to notify and update the contracts in related collections.
        userId: Id of the user
        data: incoming contract data from a user that is to be updated to a subscriber
        tutorId: Id of the tutor
        """
        for observer in self.subscribers:  # update student then tutor is required
            print("json adap patch:", patch)
            observer.updateContracts(userId, data, patch=patch)
            if tutorId:
                observer.updateContracts(tutorId, data, patch=patch)

    def notifySubscriberBids(self, userId, data, offer=None):
        '''
        This method is used to notify and update the bids in related collections.
        :param offer: optional parameter that should only be passed if the update on the bid is only in the form of
        adding an offer to a bid
        '''
        for observer in self.subscribers:
            observer.updateBids(userId, data, offer)

    def notifySubscriberUser(self, userId, bidId):
        """
        This method is used to notify and update the user additional info where it stores the subscribed bid.
        userId: Id of the user
        bidId: Id of the bid to be subscribed
        """
        for observer in self.subscribers:
            observer.addSubedBid(userId, bidId)

    def notifySubscriberCloseBid(self, bidId):
        """
        This method is used to notify and update the closedBids in related collections.
        bidId: id of the bid to be closed
        """
        for observer in self.subscribers:
            observer.closeBid(bidId)