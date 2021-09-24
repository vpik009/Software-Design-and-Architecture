import LOGIC
from APP.UserCollection import UserCollection
from GUI.Application import ViewMonitorPage
from tkinter import *

"""
tkinter is the Python interface for GUI tool of tkinter.
https://docs.python.org/3/library/tkinter.html
"""

from LOGIC.Mediator import CollectionMediator
from LOGIC.TutorOpenOfferController import EditOpenOfferController
from LOGIC.RefreshBid import *


class ViewMonitorController:
    """
    ViewMonitorController is a class that is used to monitor tutor's subscribed active bids.
    """

    def __init__(self, username, timer):
        """
        Constructor that initializes view, user, and timer.
        :param username: user's username
        :param timer: time to be updated at
        """
        self.user = username
        self.timer = timer
        self.view = ViewMonitorPage(self, self.timer)

    def goBack(self, view):
        """
        This method supports a page to be destroyed and go back to the main page.
        :param view: Page to be destroyed to avoid multiple windows.
        """
        view.root.destroy()
        controller = LOGIC.MainPageControllerFactory.MainPageControllerFactory().createMainPageController(
            CollectionMediator().getUserByUserName(self.user).getType(),
            self.user)

    def clearView(self, view):
        '''
        Function used to clear the widow of the already printed bids and offers
        :view: the instance of the page that is being viewed. ViewMonitorPage
        '''
        view.scrollable_frame.destroy()
        view.scrolling_bar.destroy()

        view.scrolling_bar = Scrollbar(view.border, orient="vertical", command=view.canvas_frame.yview)

        view.scrollable_frame = Frame(view.canvas_frame)

        view.scrollable_frame.bind(
            "<Configure>",  # triggers when there is a change in the scrollable_frame
            lambda a: view.canvas_frame.configure(
                scrollregion=view.canvas_frame.bbox("all")  # adjust the size accordingly
            )
        )

        view.canvas_frame.create_window((0, 0), window=view.scrollable_frame, anchor="nw")

        view.canvas_frame.configure(yscrollcommand=view.scrolling_bar.set)

        view.canvas_frame.pack(side="left", fill="both", expand=True)
        view.scrolling_bar.pack(side="right", fill="y")

        view.root.configure(bg='White')

        view.bid_view_label = Label(view.root, text="Subscribed Bids", bg="white", font=("Arial Bold", 25))
        view.bid_view_label.place(x=40, y=50)

    def processSubscribedBids(self, view):
        """
        This method processes all the subscribed bids for the tutor to see and displays it on the page. If the tutor has
        already offered to the subscribed bid then it can revise the offer to remain competitive from the other bidders
        from the button in the frame, which will redirect to the edit offer page.
        :param view: ViewMonitorPage that displays a information that each subscribed bid holds.
        """
        # get all bids from user collection
        user = CollectionMediator().getUserByUserName(self.user)
        subed_bids = user.getAdditionalInfo()

        if len(subed_bids) == 0:
            Label(view.scrollable_frame, text="You haven't subscribed to any bids yet",
                  padx=10,
                  font=("Arial", 10)).pack()  # the user does not have any bids to which he/she is subscribed to
            return

        for bid_id in subed_bids:
            print(bid_id)
            bid = CollectionMediator().findUsersBid(bid_id)

            if bid == None:
                return  # bug safety net for when deleting bids from api directly
            
            if str(bid.getDateClosedDown()) == "None":  # only display non closed down bids
                Label(view.scrollable_frame, text="Open Bid" + "\n Bid ID:" + bid.getId(),
                      padx=10, font=("Arial", 10)).pack()

                try:

                    for offer_request in bid.getAdditional()['bids']:
                        if offer_request['tutorId'] == user.getId():  # make a clickable button
                            Button(view.scrollable_frame,
                                   text="Weekly Sessions: " + offer_request['sessionsPerWeek']
                                        + "\nHours/Session:" + offer_request['hoursPerLesson']
                                        + "\nFree Lesson:" + offer_request['freeLesson'] + "\nRate:" +
                                        offer_request['rate'] + "\nRate Type:"
                                        + offer_request['rateType'] + "\nExtra:"
                                        + offer_request['additional'] + "\n\n CLICK TO EDIT OFFER", padx=10,
                                   font=("Arial", 10),
                                   command=lambda bid=bid: self.editOffer(view, bid.getId(), self.user)).pack()

                        else:
                            Button(view.scrollable_frame,
                                   text="Weekly Sessions: " + offer_request['sessionsPerWeek']
                                        + "\nHours/Session:" + offer_request['hoursPerLesson']
                                        + "\nFree Lesson:" + offer_request['freeLesson'] + "\nRate:" +
                                        offer_request['rate'] + "\nRate Type:"
                                        + offer_request['rateType'] + "\nExtra:"
                                        + offer_request['additional'], padx=10,
                                   font=("Arial", 10)).pack()

                except KeyError:
                    Button(view.scrollable_frame, text="No offer to the bid",
                           padx=10, font=("Arial", 10)).pack()

    def editOffer(self, view, bid_id, username):
        '''
        This is a method that calls a EditOpenOfferController if the bid that the user hold matches with the given
        bid_id. then it will redirect to the edit offer page.
        :param view: ViewMonitorPage that the user is currently on.
        :param bid_id: id of a bid that the user wants to revise its own offer for.
        '''
        # view.destroy()

        users = CollectionMediator().getAllUsers()
        for user in users:
            bids = user.getBids()
            for bid in bids:
                if bid.getId() == bid_id:
                    view.root.destroy()  # exit the current window
                    controller = EditOpenOfferController(bid,
                                                         self.user)  # index is required to have for easy access to the bid that is to be patched
        # should always be able to find at least one. otherwise what did they click on?

    def refreshSubscribedBids(self, view):
        """
        This method refreshes all the subscribed bids for the tutor at every N seconds. This is done by
        invoking refreshBid method and clear the view then re-process the subscribed bids again to keep up with
        a change.
        :param view: ViewMonitorPage that the user is currently on.
        """

        RefreshBid.refreshBid()

        # refresh the page by creating another instance of this page

        self.clearView(view)
        self.processSubscribedBids(view)
