
from datetime import datetime
"""
datetime provides functionalities for manipulating dates and times into various formats
https://docs.python.org/3/library/datetime.html
"""

from tkinter import messagebox
"""
tkinter is the Python interface for GUI tool of tkinter. 
https://docs.python.org/3/library/tkinter.html
"""

from API.JSONAdapter import JSONAdapter
from GUI.Application import CreateBidPage
import LOGIC
from LOGIC.Mediator import CollectionMediator


class CreateBidController:
    """
    CreateBidController class is a controller class that has a responsibility of creating a user bid.
    """
    def __init__(self,type,username):
        """
        This is a constructor that initializes type, username, and CreateBidPage View.
        :param type: type defines a user type whether the user is student or tutor.
        :param username: username defines a username of the user.
        """
        self.type = type
        self.user = username
        self.view = CreateBidPage(self)

    def goBack(self, view):
        """
        This method supports a page to be destroyed and go back to the main page.
        :param view: Page to be destroyed to avoid multiple windows.
        """
        view.root.destroy()  # destroy current view page
        controller = LOGIC.MainPageControllerFactory.MainPageControllerFactory().createMainPageController(
            CollectionMediator().getUserByUserName(self.user).getType(), self.user)

    def submit(self, view, name, description, dCompetency, sessions_week, hours_lesson, rate, rate_type, bid_type, freeLesson):
        """
        This method collects user inputs on the bid he wants to create and calls JSONAdapter to create the bid.
        :param view: the page from which to collect user inputs.
        :param name: name defines the name of the subject
        :param description: description defines the description of the subject
        :param dCompetency: dCompetency defines the desired competency of the tutor
        :param sessions_week: sessions_week defines the sessions per the user desires
        :param hours_lesson: hours_lesson defines the hours per lesson is desired by a user.
        :param rate: rate is the rate of a tuition fee
        :param rate_type: rate_type defines whether it is a hourly session or per session
        :param bid_type: bid_type defines whether it is a closed or open bid.
        """
        col_mediator = CollectionMediator()

        if len(col_mediator.getUserByUserName(self.user).getContracts()) >= 5:  # if the user has more than 5 contracts
            messagebox.showinfo(title="Error", message="Cannot have more than 5 contracts at a time")
            self.goBack(view)

        else:

            #search existance of subject
            subject = col_mediator.getSubjectByName(name) #list of subjects

            adapter = JSONAdapter.getInstance()

            if not subject:  # if the subject doesnt exist in the collection, its not in the web service
                # create one

                posted_subject = adapter.postSubject(name, description)
                col_mediator.addSubject(posted_subject)  # adds the subject to the collection

                subject = posted_subject  # set to subject for scope variation

            #use subject in creating the bid
            # close is 2 open is 1
            type = "close"
            if bid_type == 1:
                type = "open"


            p_type = "Per session"
            if rate_type == 1:
                p_type = "Per hour"


            free_lesson = "no"
            if freeLesson == 1:
                free_lesson = "yes"

            additionalInfo = {
                "desiredCompetency": dCompetency,
                "sessionsPerWeek": sessions_week,
                "hoursPerLesson": hours_lesson,
                "freeLesson": free_lesson,
                "rate": rate,
                "rateType": p_type
            }

            #get todays date
            user = col_mediator.getUserByUserName(self.user)
            bid = adapter.postBid(type, user.getId(), datetime.now().__str__() ,subject.getId(),additionalInfo)


            #redirect to homepage
            self.goBack(view)
