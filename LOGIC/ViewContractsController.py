from tkinter import messagebox

import LOGIC
from LOGIC.CreateContract import CreateContract

from GUI.Application import ViewContractsPage
from tkinter import *
"""
tkinter is the Python interface for GUI tool of tkinter.
https://docs.python.org/3/library/tkinter.html
"""

from LOGIC.Mediator import CollectionMediator
from LOGIC.RenewContractController import RenewContractController


class ViewContractsController:
    """
    StudentViewBidsController is a class that implements ViewBidsControllerInterface that is
    mainly to process bids and redirect to a different page.
    """

    def __init__(self, username):
        """
        Constructor that initializes view and user.
        :param username: user's username
        """
        self.user = username
        self.view = ViewContractsPage(self)


    def goBack(self, view):
        """
        This method supports a page to be destroyed and go back to the main page.
        :param view: Page to be destroyed to avoid multiple windows.
        """
        view.root.destroy()
        controller = LOGIC.MainPageControllerFactory.MainPageControllerFactory().createMainPageController(
            CollectionMediator().getUserByUserName(self.user).getType(),
            self.user)

    def processContracts(self, view):
        """
        This processes all user's contracts and display them on the page.
        :param view: page the bid to be displayed on.
        """
        user = CollectionMediator().getUserByUserName(self.user)
        user_contracts = user.getContracts()
        for con in user_contracts:  # todo check validity (state) similarly to bids
            if con.getState().type() != "expired":  # contract is not expired
                if con.getState().type() == "pending" and user.getType() == "tutor":
                    Button(view.scrollable_frame, text=con.doState()+"\n"+con.stringifyDetails()+"\nClick to sign the contract", font=("Arial", 10),
                           command=lambda con=con: self.signContract(view,con.getId() )).pack()
                else:
                    Button(view.scrollable_frame, text=con.doState()+"\n"+con.stringifyDetails(), font=("Arial", 10)).pack()

            else:  # the contract is expired and the user is a student. Allow them to renew
                if user.getType()=="student":
                    Button(view.scrollable_frame, text=con.doState()+"\n"+con.stringifyDetails(), font=("Arial", 10),
                                   command=lambda con=con: self.renewContract(view, con.getId() )  ).pack()
                else:
                    Button(view.scrollable_frame, text=con.doState()+"\n"+con.stringifyDetails(), font=("Arial", 10)).pack()

    def signContract(self, view ,con_id):
        """
        This method is used to sign a contract, using the contract id, which is done through singContract method from
        CreateContract class.
        :param view: view page to go back to after successfully signing a contract
        :param con_id: id of a contract to be signed.
        """
        CreateContract().signContract(con_id)
        messagebox.showinfo("Contract signed", "The contract with "+str(con_id)+" has been signed")
        self.goBack(view)

    def renewContract(self, view, con_id):
        """
        This method is used to invoke the RenewContractController to renew a contract with the contract id given.
        :param view: view page to be destroyed for a new page
        :param con_id: id of a contract to be renewed.
        """
        view.root.destroy()
        controller = RenewContractController(self.user,con_id)
