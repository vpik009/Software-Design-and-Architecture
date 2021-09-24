from datetime import datetime
"""
datetime provides functionalities for manipulating dates and times into various formats
https://docs.python.org/3/library/datetime.html
"""

from tkinter import simpledialog, messagebox
"""
tkinter is the Python interface for GUI tool of tkinter. 
https://docs.python.org/3/library/tkinter.html
"""


from API.JSONAdapter import JSONAdapter
from LOGIC.Mediator import CollectionMediator


class CreateContract:
    '''
    Classes used to encapsulate all data and methods used to create contracts
    '''

    def __init__(self):
        '''
        Creates the instance of this class
        '''
        self.adapter = JSONAdapter.getInstance()

    def createContract(self, studentId, tutorId, subId, dComp, acceptedOffer, manual=False): # dcomp added
        '''
        Used to create contracts
        :studentId: the student id of the student that is involved with the contract
        :tutorId: the tutor id of the tutor thats involved with the contract
        :subId: the subject id of the subject for which a contract is being created
        :dComp: the competency that the offer required the tutor to be
        :acceptedOffer: the details of the offer the contract is being signed for
        :manual: this is an optional input that states whether this contract is being created automatically, or prompted by the user
        '''

        ##OPEN A NEW PAGE FOR THE USER TO INPUT VALIDITY LENGTH
        duration_months = None
        while manual:
            duration_months = simpledialog.askinteger("Contract Duration","Input desired contract duration in months")

            if duration_months >= 1:
                break  # the user made a duration choice
            if duration_months == None:
                return  # the user clicked 'cancel'. abort procedure
            # else the user made an invalid choice
            messagebox.showerror("Invalid input","The duration of the contract must be longer than 1 months. Try again")


        ##------------------------------------------------------
        col_mediator = CollectionMediator()
        tut_comp = col_mediator.getUserById(tutorId).getCompetency()
        tut_qual = col_mediator.getUserById(tutorId).getQualifications()

        if not manual:  # if automatic, then 6 month
            duration_months = 6

        contract = self.adapter.postContract(studentId, tutorId, subId, acceptedOffer, tut_comp, tut_qual, dComp, duration_months)  # delegate contract creation to JSONADAPTER

        if not manual: # sign the contract automatically
            self.signContract(contract.getId())

        return contract


    def afterContract(self, bidId):
        '''
        Method used to close down the bid. Used as a method that performs all the necessary functions after creation of a bid
        :bidId: the id of the bid that is to be closed down
        '''

        self.adapter.closeBid(bidId)  # close down the bid


    def signContract(self,con_id):
        '''
        method used to sign a contract
        :con_id: the id of the contract that is to be signed
        '''
        return self.adapter.signContract(con_id, datetime.now())

