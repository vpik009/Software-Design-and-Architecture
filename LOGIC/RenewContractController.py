from tkinter import *
"""
tkinter is the Python interface for GUI tool of tkinter.
https://docs.python.org/3/library/tkinter.html
"""

from GUI.Application import RenewContractPage
import LOGIC
from tkinter import simpledialog, messagebox
from LOGIC.Mediator import CollectionMediator
from LOGIC.CreateContract import CreateContract


class RenewContractController:
    def __init__(self, user, con_id):
        self.user = user
        self.contract_id = con_id
        self.view = RenewContractPage(self)

    def goBack(self, view):
        '''
        Method used to go to the previous page
        :view: the page that is being displayed (RenewContractPage)
        '''
        view.root.destroy()
        LOGIC.ViewContractsController.ViewContractsController(self.user)

    def displayLastContracts(self, view):
        '''
        this method is used to display the student's last 5 contracts on the page as clickable buttons
        view: the page that is being displayed (RenewContractPage)
        '''
        Label(view.scrollable_frame, text="Your last 5 Contracts: (For when same tutor is to be used)", padx=10,
              font=("Arial Bold", 12)).pack()  # the user does not have any bids to which he/she is subscribed to
        user = CollectionMediator().getUserByUserName(self.user)
        user_contracts = user.getContracts()  # returns a list of their contracts. First is most recent
        i = 0  # contract counter , up to 5
        for con in user_contracts:
            Button(view.scrollable_frame, text=con.stringifyDetails() + "\n CLICK TO RENEW WITH THESE DETAILS",
                   font=("Arial", 10),
                   command=lambda con=con: self.renewContract(view,
                                                            con.getAdditionalInfo()['sessionsPerWeek'], con.getAdditionalInfo()['hoursPerLesson'],
                                                            con.getAdditionalInfo()['rate'],con.getAdditionalInfo()['rateType'],con.getAdditionalInfo()['freeLesson']
                                                            )).pack()
            i += 1
            if i >= 5:
                break

    def renewContractPreliminary(self,view, sesPerWeek, hoursPerSes, rate, rateType, freeLesson):
        '''
            Function used as a prelimianary function to renewContract. Used to collect and format data to be stored in the renewed contract
            :view: the page that is being displayed (RenewContractPage)
            :sesPerWeek: tutor's new input for sessions per week
            :hoursPerSes: tutor's new input for hours per session
            :rate: the rate the tutor is offering
            :rateType: how the rate is to be interpreted (per session or per hour)
            :freeLesson: tutor's new input for freeLesson indicating whether or not he offers a free lesson
        '''
        if rateType == 1:
            rateType = "Per hour"
        elif rateType == 2:
            rateType = "Per sesson"


        if freeLesson == 1:
            freeLesson = "yes"
        elif freeLesson == 2:
            freeLesson = "no"

        self.renewContract(view,sesPerWeek,hoursPerSes,rate,rateType,freeLesson)

    def renewContract(self, view, sesPerWeek, hoursPerSes, rate, rateType, freeLesson):
        '''
        Function used to create a new contract with the provided terms
        :view: the page that is being displayed (RenewContractPage)
        :sesPerWeek: tutor's new input for sessions per week
        :hoursPerSes: tutor's new input for hours per session
        :rate: the rate the tutor is offering
        :rateType: how the rate is to be interpreted (per session or per hour)
        :freeLesson: tutor's new input for freeLesson indicating whether or not he offers a free lesson
        '''
        duration_months = None
        manual = True
        subject_id = None
        user_id = CollectionMediator().getUserByUserName(self.user).getId()
        dComp = None
        for user in CollectionMediator().getAllUsers():
            for con in user.getContracts():
                if con.getId() == self.contract_id:
                    subject_id = con.getSubjectId()
                    dComp = con.getAdditionalInfo()['desiredCompetency']

        while manual:
            tutor_username = simpledialog.askstring("Tutor Username", "Input tutor' username with whome to renew this contract")
            if not tutor_username:
                break
            tutor = CollectionMediator().getUserByUserName(tutor_username)

            if tutor:
                # get the desired competency
                # dComp = con.getAdditionalInfo()["desiredCompetency"]
                tutor_comp = tutor.getCompetency()

                # does it need to loop through the tutor_comp list?
                for i in range(len(tutor_comp)):

                    if tutor_comp[i].getSubjectId() == subject_id and int(tutor_comp[i].getLevel()) >= (int(dComp) + 2):

                            # same offer from the last contract
                            offer = {
                                "sessionsPerWeek": sesPerWeek,
                                "hoursPerLesson": hoursPerSes,
                                "freeLesson": freeLesson,
                                "rate": rate,
                                "rateType": rateType,
                                "additional": ""
                            }
                            # creating a new contract as per requirement
                            CreateContract().createContract(user_id, tutor.getId(), subject_id, dComp, offer, manual=True)
                            self.goBack(view)
                            break


                    else:
                        messagebox.showerror("Error","The tutor does not fulfill the desired competency")
                break
                        
            else:
                messagebox.showerror("Error", "No tutor exists under the specified username")
