
from API.JSONAdapter import JSONAdapter


class RefreshBid:
    """
    RefreshBid class is a class that holds responsibility for refreshing the model collections for user and bids as the
    bid and user are updated every N seconds and hence it re-initializes each model collections.
    """
    def __init__(self):
        """
        Empty constructor
        """
        pass

    @staticmethod
    def refreshBid():
        """
        refreshBid method is to re-initialize the model collections User and Bid.
        """
        adapter = JSONAdapter.getInstance()
        user_list = adapter.getAllUsers()
        bid_list = adapter.getAllBids()
        for user in user_list:  # make a list of users
            # set bids
            list = []
            for bid in bid_list:

                if bid.getOwnerId() == user.getId():  # add bid to the user
                    list.append(bid)
            user.setBids(list)


