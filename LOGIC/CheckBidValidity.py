
from LOGIC.CreateContract import CreateContract


class CheckBidValidity:
    '''
    Class that's responsible for checking the validity of the bid provided to the checkPrintValidity Method
    '''
    def __init__(self):
        pass

    def checkPrintValidity(self, bid):
        '''
        Checks if the bid is valid to be printed. If the bid expired, close it down and create a contract.
        If yes, close down the bit through JSONAdapter, and create a contract, return True
        If no, return False
        :bid: the bid that is to be checked for its validity
        :output: True if the has been closed down and False if not
        '''

        if bid.checkTime() and not bid.getDateClosedDown():  # if time expired and it hasnt been closed down yet
            # close down and make a contract
            # adapter = JSONAdapter.getInstance()
            # adapter.closeBid(bid.getId())  # close down the bid
            contract_creator = CreateContract()
            contract_creator.afterContract(bid.getId())  # perform post contract creation actions on the bid

            if bid.getType() == "OpenBid":
                try:  # if the bid has offers
                    offers = bid.getAdditional()['bids']  # if the bid has offers
                    last_offer = offers[len(offers) - 1]
                    dComp = bid.getAdditional()['desiredCompetency']  # to view the desired competency when renewing with a different tutor
                    contract_creator.createContract(bid.getOwnerId(), last_offer['tutorId'], bid.getSubId(), dComp, last_offer, manual=False)


                except Exception:  # bid has no offers, just close it down
                    pass


            return True

        return False