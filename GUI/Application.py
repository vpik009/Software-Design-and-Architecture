from tkinter import *
"""
tkinter is the Python interface for GUI tool of tkinter. 
https://docs.python.org/3/library/tkinter.html
"""

from LOGIC import LoginController as user, MainPageControllerAbstract, ViewBidsControllerInterface

from abc import ABC
"""
ABC: A helper class that creates an abstract class by deriving from ABC module 
https://docs.python.org/3/library/abc.html
"""


class Page(ABC):
    '''
    The main Abstract page class,that holds the TK instance, sets the geometry of the window, title, and gets passes the controller from its child classes.
    '''

    def __init__(self, controller):
        self.controller = controller
        self.root = Tk()
        self.root.geometry("800x800")
        self.root.title("Student-Tutor Application")


class LoginPage(Page):
    '''
    Class responsible for representing the UI of the login page
    '''

    def __init__(self, controller):
        '''
        Contructor of the login page, the takes in the controller that is responsible for the logic operations of this page
        :param controller: the controller of the page the user is currently on
        '''
        super().__init__(controller)

        self.border = LabelFrame(self.root, text='Login', bg='ivory', bd=10, font=("Arial", 20))
        self.border.pack(fill="both", expand="yes", padx=150, pady=150)

        self.username_input = Label(self.border, text="Username", font=("Arial Bold", 15), bg='ivory')
        self.username_input.place(x=50, y=20)
        self.username = Entry(self.border, width=30, bd=5)
        self.username.place(x=180, y=20)

        self.password_input = Label(self.border, text="Password", font=("Arial Bold", 15), bg='ivory')
        self.password_input.place(x=50, y=80)
        self.password = Entry(self.border, width=30, show='*', bd=5)
        self.password.place(x=180, y=80)

        self.login_error_input = Label(self.border, text="", font=("Arial Bold", 15), bg='ivory')
        self.login_error_input.place(x=20, y=250)

        self.login_button = Button(self.border, text="Login", font=("Arial", 15),
                                   command=lambda: self.controller.validateLogin(self.username.get(),
                                                                                 self.password.get(), self))
        self.login_button.place(x=220, y=255)

        self.root.mainloop()


class MainPageFactory:
    '''
    Main page factory class that is mainly responsible for creating the correct main page controller
    '''

    def __init__(self, controller: MainPageControllerAbstract):
        '''
        constructor takes in the controller
        :param controller: the controller of the page the user is currently on
        '''
        self.controller = controller

    def createMainPage(self, type, username):
        '''
        method responsible for decision making in terms of the concrete factory that is to be created for main page
        :param type: the type of user who is using the system
        :param username: the username of the current user
        '''
        page = None
        if type == "tutor":
            page = TutorMainPageFactory(self.controller).createMainPage(type, username)
        elif type == "student":
            page = StudentMainPageFactory(self.controller).createMainPage(type, username)
        return page


class StudentMainPageFactory(MainPageFactory):
    '''
    the concrete main page factory that creates the main page for student user
    '''

    def __init__(self, controller: MainPageControllerAbstract):
        self.controller = controller

    def createMainPage(self, type, username):
        '''
        method responsible for creating the student main page
        :param type: the type of user who is using the system
        :param username: the username of the current user
        '''

        return StudentMainPage(self.controller, username)


class TutorMainPageFactory(MainPageFactory):
    '''
    the concrete main page factory that creates the main page for tutor user
    '''

    def __init__(self, controller: MainPageControllerAbstract):
        self.controller = controller

    def createMainPage(self, type, username):
        '''
        method responsible for creating the tutor main page
        :param type: the type of user who is using the system
        :param username: the username of the current user
        '''

        return TutorMainPage(self.controller, username)


from abc import ABC


class AbstractMainPage(Page, ABC):
    '''
    The abstract main page holding elements common across all main pages for all users
    '''

    def __init__(self, controller: MainPageControllerAbstract, username):
        '''
        Contructor for the student's main page
        :param controller: the controller for the student's main page
        :param username: the users username
        '''
        super().__init__(controller)

        self.username_display = Label(self.root, text="Logged in as: " + str(username), font=("Arial Bold", 15))
        self.username_display.place(x=50, y=50)

        self.view_bids_button = Button(self.root, text="View Bids", font=("Arial", 15),
                                       command=lambda: self.controller.viewBids(self))
        self.view_bids_button.place(x=200, y=200)

        self.view_all_contracts_button = Button(self.root, text="View Contracts", font=("Arial", 15),
                                                command=lambda: self.controller.viewContracts(self))
        self.view_all_contracts_button.place(x=200, y=300)

        # SCOLLABLE---Used for notifications

        self.border = LabelFrame(self.root, text='', bg='ivory', bd=10, font=("Arial", 20))
        self.border.place(x=50, y=450, height=300, width=700)

        self.canvas_frame = Canvas(self.border)
        # set the scroll bar
        self.scrolling_bar = Scrollbar(self.border, orient="vertical", command=self.canvas_frame.yview)

        # creating a canvas within the given frame
        self.scrollable_frame = Frame(self.canvas_frame)

        # Calling a function whenever the contents inside the scrollable frame change
        self.scrollable_frame.bind(
            "<Configure>",  # triggers when there is a change in the scrollable_frame
            lambda a: self.canvas_frame.configure(
                scrollregion=self.canvas_frame.bbox("all")  # adjust the size accordingly
            )
        )

        # using create_window functionality to create a window within the canvas
        self.canvas_frame.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        # configuring the canvas to be able to resize the change in the size of the scrollbar
        self.canvas_frame.configure(yscrollcommand=self.scrolling_bar.set)

        self.canvas_frame.pack(side="left", fill="both", expand=True)
        self.scrolling_bar.pack(side="right", fill="y")
        # ---

        # LOAD NOTIFICATIONS
        controller.displayContractNotifications(self)


class StudentMainPage(AbstractMainPage):
    '''
    The student main page UI
    '''

    def __init__(self, controller: MainPageControllerAbstract, username):
        '''
        Contructor for the student's main page
        :param controller: the controller for the student's main page
        :param username: the users username
        '''
        super().__init__(controller, username)

        self.create_bids_button = Button(self.root, text="Create Bid", font=("Arial", 15),
                                         command=lambda: self.controller.goToCreateBid(self))
        self.create_bids_button.place(x=200, y=250)



class TutorMainPage(AbstractMainPage):
    '''
    The tutor main page UI
    '''

    def __init__(self, controller: MainPageControllerAbstract, username):
        '''
        Contructor for the tutor's main page
        :param controller: the controller for the student's main page
        :param username: the users username
        '''
        super().__init__(controller, username)

        self.view_monitor = Button(self.root, text="View Monitor", font=("Arial", 15),
                                   command=lambda: self.controller.viewMonitor(self))
        self.view_monitor.place(x=200, y=250)


class CreateBidPage(Page):
    '''
    UI for the page that is used to create Bids.
    '''

    def __init__(self, controller):
        '''
        Contructorthat initialized UI elements and takes in the controller for this page
        :param  controller: the controller that instantiated this page
        '''

        super().__init__(controller)

        self.root.configure(bg='White')

        # --- inputs---

        self.border = LabelFrame(self.root, text='Bid Creation', bg='ivory', bd=10, font=("Arial", 20))
        self.border.pack(fill="both", expand="yes", padx=100, pady=100)

        self.subject_label = Label(self.border, text="Subject Name", font=("Arial Bold", 10), bg='ivory')
        self.subject_label.place(x=10, y=20)
        self.subject_input = Entry(self.border, width=30, bd=5)
        self.subject_input.place(x=220, y=20)

        self.subject_description_label = Label(self.border, text="Subject Description", font=("Arial Bold", 10),
                                               bg='ivory')
        self.subject_description_label.place(x=10, y=90)
        self.subject_description_input = Entry(self.border, width=30, bd=5)
        self.subject_description_input.place(x=220, y=90)

        self.competency_label = Label(self.border, text="Desired Competency", font=("Arial Bold", 10), bg='ivory')
        self.competency_label.place(x=10, y=160)
        self.competency_input = Spinbox(self.border, from_=0, to=10, bg='white')
        self.competency_input.place(x=220, y=160)

        self.session_week_label = Label(self.border, text="Sessions per week", font=("Arial Bold", 10), bg='ivory')
        self.session_week_label.place(x=10, y=230)
        self.session_week_input = Spinbox(self.border, from_=1, to=70, bg="white")  # up to 10 sessions per day
        self.session_week_input.place(x=220, y=230)

        self.hours_session_label = Label(self.border, text="Hours per session", font=("Arial Bold", 10), bg='ivory')
        self.hours_session_label.place(x=10, y=300)
        self.hours_session_input = Spinbox(self.border, from_=1, to=24, bg="white")  # no more than 24 hours
        self.hours_session_input.place(x=220, y=300)

        bid_type = IntVar()

        self.open_bid_radio = Radiobutton(self.border, text="Open Bid", variable=bid_type, value=1, bg="ivory")
        self.open_bid_radio.place(x=50, y=370)

        self.close_bid_radio = Radiobutton(self.border, text="Close Bid", variable=bid_type, value=2, bg="ivory")
        self.close_bid_radio.place(x=210, y=370)

        self.rate_label = Label(self.border, text="Preferred rate", font=("Arial Bold", 10), bg='ivory')
        self.rate_label.place(x=10, y=440)
        self.rate_input = Spinbox(self.border, from_=0, to=999999999, bg="white")
        self.rate_input.place(x=220, y=440)

        pay_type = IntVar()

        self.rate_hr_input = Radiobutton(self.border, text="Per hour", variable=pay_type, value=1, bg="ivory")
        self.rate_hr_input.place(x=370, y=440)

        self.rate_ses_input = Radiobutton(self.border, text="Per session", variable=pay_type, value=2, bg="ivory")
        self.rate_ses_input.place(x=450, y=440)

        self.free_lesson = IntVar()
        self.free_lesson_label = Label(self.border, text="Free session", font=("Arial Bold", 10), bg='ivory')
        self.free_lesson_label.place(x=10, y=480)

        self.yes_radio = Radiobutton(self.border, text="Yes", variable=self.free_lesson, value=1, bg="ivory")
        self.yes_radio.place(x=150, y=480)

        self.no_radio = Radiobutton(self.border, text="No", variable=self.free_lesson, value=2, bg="ivory")
        self.no_radio.place(x=200, y=480)

        # -------------
        # submitBid(self, name, description, dCompetency, sessions_week, hours_lesson, rate, rate_type):
        self.submit_button = Button(self.root, text="Submit", font=("Arial", 15),
                                    command=lambda: self.controller.submit(
                                        self, self.subject_input.get(), self.subject_description_input.get(),
                                        self.competency_input.get(),
                                        self.session_week_input.get(), self.hours_session_input.get(),
                                        self.rate_input.get(), pay_type.get(),
                                        bid_type.get(), self.free_lesson.get())
                                    )
        self.submit_button.place(x=500, y=710)

        self.submit_button = Button(self.root, text="Back", font=("Arial", 15),
                                    command=lambda: self.controller.goBack(self))
        self.submit_button.place(x=100, y=710)


class OfferPage(Page):
    '''
    The base page UI used to display offers and bids with a scrollable UI
    '''

    def __init__(self, controller):
        '''
        Constructor that initialized UI elements and takes in a controller that created this page
        :param controller: the controller that instantiated this page
        '''
        super().__init__(controller)

        self.root.configure(bg='White')

        # --- inputs---

        self.border = LabelFrame(self.root, text='', bg='ivory', bd=10, font=("Arial", 20))
        self.border.pack(fill="both", expand="yes", padx=60, pady=100)

        # ______________________________
        self.canvas_frame = Canvas(self.border)
        # set the scroll bar
        self.scrolling_bar = Scrollbar(self.border, orient="vertical", command=self.canvas_frame.yview)

        # creating a canvas within the given frame
        self.scrollable_frame = Frame(self.canvas_frame)

        # Calling a function whenever the contents inside the scrollable frame change
        self.scrollable_frame.bind(
            "<Configure>",  # triggers when there is a change in the scrollable_frame
            lambda a: self.canvas_frame.configure(
                scrollregion=self.canvas_frame.bbox("all")  # adjust the size accordingly
            )
        )

        # using create_window functionality to create a window within the canvas
        self.canvas_frame.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        # configuring the canvas to be able to resize the change in the size of the scrollbar
        self.canvas_frame.configure(yscrollcommand=self.scrolling_bar.set)

        self.canvas_frame.pack(side="left", fill="both", expand=True)
        self.scrolling_bar.pack(side="right", fill="y")

        self.root.configure(bg='White')

        self.print_bid_button = Button(self.root, text="Print Bid Info", font=("Arial", 15),
                                       command=lambda: self.controller.printBidInfo(self))
        self.print_bid_button.place(x=550, y=710)

        self.back_button = Button(self.root, text="Back", font=("Arial", 15),
                                  command=lambda: self.controller.goBack(self))
        self.back_button.place(x=100, y=710)

class OpenOfferPage(OfferPage,ABC):
    def __init__(self, controller):
        '''
        Contructor that initialized the page's UI elements
        :param controller: the controller that initialized this page
        '''
        super().__init__(controller)

        self.session_week_label = Label(self.border, text="Sessions per week", font=("Arial Bold", 10), bg='ivory')
        self.session_week_label.place(x=10, y=320)
        self.session_week_input = Spinbox(self.border, from_=1, to=70, bg="white")  # up to 10 sessions per day
        self.session_week_input.place(x=220, y=320)

        self.hours_session_label = Label(self.border, text="Hours per session", font=("Arial Bold", 10), bg='ivory')
        self.hours_session_label.place(x=10, y=360)
        self.hours_session_input = Spinbox(self.border, from_=1, to=24, bg="white")  # no more than 24 hours
        self.hours_session_input.place(x=220, y=360)

        self.free_lesson = IntVar()
        self.free_lesson_label = Label(self.border, text="Free session", font=("Arial Bold", 10), bg='ivory')
        self.free_lesson_label.place(x=10, y=400)

        self.yes_radio = Radiobutton(self.border, text="Yes", variable=self.free_lesson, value=1, bg="ivory")
        self.yes_radio.place(x=150, y=400)

        self.no_radio = Radiobutton(self.border, text="No", variable=self.free_lesson, value=2, bg="ivory")
        self.no_radio.place(x=200, y=400)

        self.rate_label = Label(self.border, text="Preferred rate", font=("Arial Bold", 10), bg='ivory')
        self.rate_label.place(x=10, y=440)
        self.rate_input = Spinbox(self.border, from_=0, to=999999999, bg="white")
        self.rate_input.place(x=220, y=440)

        self.pay_type = IntVar()

        self.rate_hr_input = Radiobutton(self.border, text="Per hour", variable=self.pay_type, value=1, bg="ivory")
        self.rate_hr_input.place(x=370, y=440)

        self.rate_ses_input = Radiobutton(self.border, text="Per session", variable=self.pay_type, value=2,
                                          bg="ivory")
        self.rate_ses_input.place(x=450, y=440)

        self.additional_info_label = Label(self.border, text="Additonal Information", font=("Arial Bold", 10),
                                           bg='ivory')
        self.additional_info_label.place(x=10, y=480)
        self.additional_info = Entry(self.border, width=60, bd=5)
        self.additional_info.place(x=220, y=480)


class EditOpenOfferPage(OpenOfferPage):

    def __init__(self,controller):
        super().__init__(controller)

        # self.reminder_label = Label(self.border, text="Keep a field as it is if you dont wish to change it", font=("Arial Bold", 10)).place(x=10,y=10)

        self.create_button = Button(self.root, text="Edit", font=("Arial", 15),
                                    command=lambda: self.controller.create(self,
                                                                           self.session_week_input.get(),
                                                                           self.hours_session_input.get(),
                                                                           self.free_lesson.get(),
                                                                           self.rate_input.get(), self.pay_type.get(),
                                                                           self.additional_info.get())
                                    )
        self.create_button.place(x=180, y=710)

class RenewContractPage(Page):

    def __init__(self,controller):
        super().__init__(controller)

        self.root.configure(bg='White')

        # --- inputs---

        self.border = LabelFrame(self.root, text='', bg='ivory', bd=10, font=("Arial", 20))
        self.border.place(x=50, y=30, height=300, width=700)

        # ______________________________
        self.canvas_frame = Canvas(self.border)
        # set the scroll bar
        self.scrolling_bar = Scrollbar(self.border, orient="vertical", command=self.canvas_frame.yview)

        # creating a canvas within the given frame
        self.scrollable_frame = Frame(self.canvas_frame)

        # Calling a function whenever the contents inside the scrollable frame change
        self.scrollable_frame.bind(
            "<Configure>",  # triggers when there is a change in the scrollable_frame
            lambda a: self.canvas_frame.configure(
                scrollregion=self.canvas_frame.bbox("all")  # adjust the size accordingly
            )
        )

        # using create_window functionality to create a window within the canvas
        self.canvas_frame.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        # configuring the canvas to be able to resize the change in the size of the scrollbar
        self.canvas_frame.configure(yscrollcommand=self.scrolling_bar.set)

        self.canvas_frame.pack(side="left", fill="both", expand=True)
        self.scrolling_bar.pack(side="right", fill="y")

        self.root.configure(bg='White')

        self.back_button = Button(self.root, text="Back", font=("Arial", 15),
                                  command=lambda: self.controller.goBack(self))
        self.back_button.place(x=100, y=710)


        self.info_label = Label(self.root, text="Or... Update agreement terms", font=("Arial Bold", 12), bg='ivory')
        self.info_label.place(x=30, y=350)

        self.session_week_label = Label(self.root, text="Sessions per week", font=("Arial Bold", 10), bg='ivory')
        self.session_week_label.place(x=30, y=400)
        self.session_week_input = Spinbox(self.root, from_=1, to=70, bg="white")  # up to 10 sessions per day
        self.session_week_input.place(x=220, y=400)

        self.hours_session_label = Label(self.root, text="Hours per session", font=("Arial Bold", 10), bg='ivory')
        self.hours_session_label.place(x=30, y=450)
        self.hours_session_input = Spinbox(self.root, from_=1, to=24, bg="white")  # no more than 24 hours
        self.hours_session_input.place(x=220, y=450)


        self.rate_label = Label(self.root, text="Preferred rate", font=("Arial Bold", 10), bg='ivory')
        self.rate_label.place(x=30, y=500)
        self.rate_input = Spinbox(self.root, from_=0, to=999999999, bg="white")
        self.rate_input.place(x=220, y=500)

        self.pay_type = IntVar()

        self.rate_hr_input = Radiobutton(self.root, text="Per hour", variable=self.pay_type, value=1, bg="ivory")
        self.rate_hr_input.place(x=400, y=500)

        self.rate_ses_input = Radiobutton(self.root, text="Per session", variable=self.pay_type, value=2,
                                          bg="ivory")
        self.rate_ses_input.place(x=480, y=500)

        self.freeLess = IntVar()

        self.freeLes_label = Label(self.root, text="Free Lesson: ",font=("Arial Bold", 10), bg="ivory")
        self.freeLes_label.place(x=30, y=570)
        self.freeLes_input = Radiobutton(self.root, text="Yes", variable=self.freeLess, value=1, bg="ivory")
        self.freeLes_input.place(x=150, y=570)

        self.freeLes_input = Radiobutton(self.root, text="No", variable=self.freeLess, value=2,
                                          bg="ivory")
        self.freeLes_input.place(x=270, y=570)



        self.renew_button = Button(self.root, text="Renew", font=("Arial", 15), # need to get variables into this command
                                  command=lambda: self.controller.renewContractPreliminary(self,
                                                                                           self.session_week_input.get(),
                                                                                           self.hours_session_input.get(),
                                                                                           self.rate_input.get(),
                                                                                           self.pay_type.get(),
                                                                                           self.freeLess.get()
                                                                                           ))
        self.renew_button.place(x=300, y=710)

        self.root.after(10,self.process())

    def process(self):
        self.controller.displayLastContracts(self)




class CreateOpenOfferPage(OpenOfferPage):  # Only for tutors
    '''
    Page that holds the UI elements for creating an open offer
    '''


    def __init__(self, controller):
        '''
        Contructor that initialized the page's UI elements
        :param controller: the controller that initialized this page
        '''
        super().__init__(controller)


        self.create_button = Button(self.root, text="Create Offer", font=("Arial", 15),
                                    command=lambda: self.controller.create(self,
                                                                           self.session_week_input.get(),
                                                                           self.hours_session_input.get(),
                                                                           self.free_lesson.get(),
                                                                           self.rate_input.get(), self.pay_type.get(),
                                                                           self.additional_info.get())
                                    )
        self.create_button.place(x=180, y=710)

        self.subscribe_bid_button = Button(self.root, text="Subscribe", font=("Arial", 15),
                                           command=lambda: self.controller.subscribeBid(self))
        self.subscribe_bid_button.place(x=300, y=710)

        self.buyout_button = Button(self.root, text="Buy Out", font=("Arial", 15),
                                    command=lambda: self.controller.buyOut(self))
        self.buyout_button.place(x=400, y=710)


class MessagePage(OfferPage):
    '''
    The page that holds UI elements for messaging
    '''

    def __init__(self, controller):
        '''
        Contructor that initialized the page's UI elements
        :param controller: the controller that initialized this page
        '''
        super().__init__(controller)

        self.messages_label = Label(self.scrollable_frame, text="Message History:", font=("Arial Bold", 10))
        self.messages_label.pack()

        self.session_week_label = Label(self.scrollable_frame, text="Sessions per week", font=("Arial Bold", 10),
                                        bg='ivory')
        self.session_week_label.pack()
        self.session_week_input = Spinbox(self.scrollable_frame, from_=1, to=70,
                                          bg="white")  # up to 10 sessions per day
        self.session_week_input.pack()

        self.hours_session_label = Label(self.scrollable_frame, text="Hours per session", font=("Arial Bold", 10),
                                         bg='ivory')
        self.hours_session_label.pack()
        self.hours_session_input = Spinbox(self.scrollable_frame, from_=1, to=24, bg="white")  # no more than 24 hours
        self.hours_session_input.pack()

        self.free_lesson = IntVar()
        self.free_lesson_label = Label(self.scrollable_frame, text="Free session", font=("Arial Bold", 10), bg='ivory')
        self.free_lesson_label.pack()

        self.yes_radio = Radiobutton(self.scrollable_frame, text="Yes", variable=self.free_lesson, value=1, bg="ivory")
        self.yes_radio.pack()

        self.no_radio = Radiobutton(self.scrollable_frame, text="No", variable=self.free_lesson, value=2, bg="ivory")
        self.no_radio.pack()

        self.rate_label = Label(self.scrollable_frame, text="Preferred rate", font=("Arial Bold", 10), bg='ivory')
        self.rate_label.pack()
        self.rate_input = Spinbox(self.scrollable_frame, from_=0, to=999999999, bg="white")
        self.rate_input.pack()

        self.pay_type = IntVar()

        self.rate_hr_input = Radiobutton(self.scrollable_frame, text="Per hour", variable=self.pay_type, value=1,
                                         bg="ivory")
        self.rate_hr_input.pack()

        self.rate_ses_input = Radiobutton(self.scrollable_frame, text="Per session", variable=self.pay_type, value=2,
                                          bg="ivory")
        self.rate_ses_input.pack()

        self.additional_info_label = Label(self.scrollable_frame, text="Additonal Information", font=("Arial Bold", 10),
                                           bg='ivory')
        self.additional_info_label.pack()
        self.additional_info = Entry(self.scrollable_frame, width=60, bd=5)
        self.additional_info.pack()

        self.send_msg_button = Button(self.scrollable_frame, text="Send Message", font=("Arial", 15),
                                      command=lambda: self.controller.create(self,
                                                                             self.session_week_input.get(),
                                                                             self.hours_session_input.get(),
                                                                             self.free_lesson.get(),
                                                                             self.rate_input.get(),
                                                                             self.pay_type.get(),
                                                                             self.additional_info.get()
                                                                             )
                                      )
        self.send_msg_button.pack()

        self.msg_histoy_button = Button(self.root, text="Message History", font=("Arial", 15),
                                        command=lambda: self.controller.printMessageHistory(self))
        self.msg_histoy_button.place(x=370, y=710)

        self.back_button = Button(self.root, text="Back", font=("Arial", 15),
                                  command=lambda: self.controller.goBack(self))
        self.back_button.place(x=100, y=710)


class ViewBidsPage(Page):
    '''
    Page that holds the UI elements for viewing Bids
    '''

    def __init__(self, controller: ViewBidsControllerInterface):
        '''
        Contructor that initialized the page's UI elements
        :param controller: the controller that initialized this page
        '''
        super().__init__(controller)

        self.border = LabelFrame(self.root, text="Bid List", bg='ivory', bd=10, font=("Arial", 20))
        self.border.pack(fill="both", expand="yes", padx=100, pady=100)

        # using Canvas with the initialized frame
        self.canvas_frame = Canvas(self.border)

        # set the scroll bar
        self.scrolling_bar = Scrollbar(self.border, orient="vertical", command=self.canvas_frame.yview)

        # creating a canvas within the given frame
        self.scrollable_frame = Frame(self.canvas_frame)

        # Calling a function whenever the contents inside the scrollable frame change
        self.scrollable_frame.bind(
            "<Configure>",  # triggers when there is a change in the scrollable_frame
            lambda a: self.canvas_frame.configure(
                scrollregion=self.canvas_frame.bbox("all")  # adjust the size accordingly
            )
        )

        # using create_window functionality to create a window within the canvas
        self.canvas_frame.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        # configuring the canvas to be able to resize the change in the size of the scrollbar
        self.canvas_frame.configure(yscrollcommand=self.scrolling_bar.set)

        self.canvas_frame.pack(side="left", fill="both", expand=True)
        self.scrolling_bar.pack(side="right", fill="y")

        self.root.configure(bg='White')

        self.bid_view_label = Label(self.root, text="Bids View", bg="white", font=("Arial Bold", 25))
        self.bid_view_label.place(x=40, y=50)

        self.view_bids = Button(self.root, text="View Bids", font=("Arial", 15),
                                command=lambda: self.controller.processBids(self))
        self.view_bids.place(x=250, y=700)

        self.back = Button(self.root, text="Back", font=("Arial", 15),
                           command=lambda: self.controller.goBack(self))
        self.back.place(x=100, y=700)


class ViewContractsPage(Page):
    '''
    Page that holds the UI elements for viewing Bids
    '''

    def __init__(self, controller):
        '''
        Contructor that initialized the page's UI elements
        :param controller: the controller that initialized this page
        '''
        super().__init__(controller)

        self.border = LabelFrame(self.root, text="Contracts View Page", bg='ivory', bd=10, font=("Arial", 20))
        self.border.pack(fill="both", expand="yes", padx=100, pady=100)

        # using Canvas with the initialized frame
        self.canvas_frame = Canvas(self.border)

        # set the scroll bar
        self.scrolling_bar = Scrollbar(self.border, orient="vertical", command=self.canvas_frame.yview)

        # creating a canvas within the given frame
        self.scrollable_frame = Frame(self.canvas_frame)

        # Calling a function whenever the contents inside the scrollable frame change
        self.scrollable_frame.bind(
            "<Configure>",  # triggers when there is a change in the scrollable_frame
            lambda a: self.canvas_frame.configure(
                scrollregion=self.canvas_frame.bbox("all")  # adjust the size accordingly
            )
        )

        # using create_window functionality to create a window within the canvas
        self.canvas_frame.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        # configuring the canvas to be able to resize the change in the size of the scrollbar
        self.canvas_frame.configure(yscrollcommand=self.scrolling_bar.set)

        self.canvas_frame.pack(side="left", fill="both", expand=True)
        self.scrolling_bar.pack(side="right", fill="y")

        self.root.configure(bg='White')

        self.bid_view_label = Label(self.root, text="Contract View", bg="white", font=("Arial Bold", 25))
        self.bid_view_label.place(x=40, y=50)



        self.back = Button(self.root, text="Back", font=("Arial", 15),
                           command=lambda: self.controller.goBack(self))
        self.back.place(x=100, y=700)

        self.root.after(10,self.process())

    def process(self):
        self.controller.processContracts(self)


class MessageView(Page):
    '''
    UI for the users to view tutors who have messages on their bids
    '''

    def __init__(self, controller):
        '''
        Contructor that initialized the page's UI elements
        :param controller: the controller that initialized this page
        '''
        super().__init__(controller)

        self.border = LabelFrame(self.root, text="Open Bid List", bg='ivory', bd=10, font=("Arial", 20))
        self.border.pack(fill="both", expand="yes", padx=100, pady=100)

        # using Canvas with the initialized frame
        self.canvas_frame = Canvas(self.border)

        # set the scroll bar
        self.scrolling_bar = Scrollbar(self.border, orient="vertical", command=self.canvas_frame.yview)

        # creating a canvas within the given frame
        self.scrollable_frame = Frame(self.canvas_frame)

        # Calling a function whenever the contents inside the scrollable frame change
        self.scrollable_frame.bind(
            "<Configure>",  # triggers when there is a change in the scrollable_frame
            lambda a: self.canvas_frame.configure(
                scrollregion=self.canvas_frame.bbox("all")  # adjust the size accordingly
            )
        )

        # using create_window functionality to create a window within the canvas
        self.canvas_frame.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        # configuring the canvas to be able to resize the change in the size of the scrollbar
        self.canvas_frame.configure(yscrollcommand=self.scrolling_bar.set)

        self.canvas_frame.pack(side="left", fill="both", expand=True)
        self.scrolling_bar.pack(side="right", fill="y")

        self.Label = Label(self.root, text="Message View", bg="white", font=("Arial Bold", 25))
        self.Label.place(x=40, y=50)

        self.view_message = Button(self.root, text="View Your Message", font=("Arial", 15),
                                   command=lambda: self.controller.processMessages(self))

        self.view_message.place(x=250, y=700)

        self.root.configure(bg='White')

        self.back_button = Button(self.root, text="Back", font=("Arial", 15),
                                  command=lambda: self.controller.goBack(self))
        self.back_button.place(x=100, y=700)


class ViewMonitorPage(Page):
    '''
    Page that holds the UI elements for viewing subscribed bids
    '''

    def __init__(self, controller, time):
        super().__init__(controller)
        self.controller = controller
        self.timer = time



        self.border = LabelFrame(self.root, text="Bid List", bg='ivory', bd=10, font=("Arial", 20))
        self.border.pack(fill="both", expand="yes", padx=100, pady=100)

        self.canvas_frame = Canvas(self.border)

        self.scrolling_bar = Scrollbar(self.border, orient="vertical", command=self.canvas_frame.yview)

        self.scrollable_frame = Frame(self.canvas_frame)

        self.scrollable_frame.bind(
            "<Configure>",  # triggers when there is a change in the scrollable_frame
            lambda a: self.canvas_frame.configure(
                scrollregion=self.canvas_frame.bbox("all")  # adjust the size accordingly
            )
        )

        self.canvas_frame.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        self.canvas_frame.configure(yscrollcommand=self.scrolling_bar.set)

        self.canvas_frame.pack(side="left", fill="both", expand=True)
        self.scrolling_bar.pack(side="right", fill="y")

        self.root.configure(bg='White')

        self.bid_view_label = Label(self.root, text="Subscribed Bids", bg="white", font=("Arial Bold", 25))
        self.bid_view_label.place(x=40, y=50)


        self.back = Button(self.root, text="Back", font=("Arial", 15),
                           command=lambda: self.controller.goBack(self))
        self.back.place(x=100, y=700)

        self.controller.processSubscribedBids(self)

        self.root.after(self.timer, self.refresh)


    def refresh(self):

        self.controller.refreshSubscribedBids(self)
        self.root.after(self.timer, self.refresh)



if __name__ == "__main__":
    user.LoginVerification()
