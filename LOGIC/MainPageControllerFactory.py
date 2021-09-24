
from GUI.Application import MainPageFactory
from LOGIC.CreateBidController import CreateBidController
from LOGIC.MainPageControllerAbstract import MainPageControllerAbstract
from LOGIC.ViewBidsController import StudentViewBidsController, TutorViewBidsController
from LOGIC.ViewContractsController import ViewContractsController
from LOGIC.ViewMonitorController import ViewMonitorController

class MainPageControllerFactory:
    """
    MainPageControllerFactory is a factory class that is used to create an object without specifying their concrete
    classes.
    """

    def __init__(self):
        """
        Empty constructor
        """
        pass

    def createMainPageController(self, type, username):
        """
        createMainPageController is a class that declares that factory
        method that returns an object of its concrete class of mainPageController depending on the type of user.
        :param type: type of a user whether a user is student or tutor
        :param username: user's username
        :output: The concrete factory for the creation of concrete main page
        """

        if type == "tutor":
            return TutorMainPageControllerFactory().createMainPageController(type, username)
        elif type == "student":
            return StudentMainPageControllerFactory().createMainPageController(type, username)


class StudentMainPageControllerFactory(MainPageControllerFactory):
    """
    StudentMainPageControllerFactory class is a concrete class of MainPageController Factory class that has a responsibility
    of returning an object of StudentMainPageController without specifying its concrete classes.
    """

    def __init__(self):
        """
        Empty Constructor
        """
        pass

    def createMainPageController(self, type, username):
        """
        createMainPageController is a class that returns an object of StudentMainPageController.
        :param type: type of a user whether a user is student or tutor
        :param username: user's username
        :output: concrete student main page
        """

        return StudentMainPageController(type, username)


class TutorMainPageControllerFactory(MainPageControllerFactory):
    """
    TutorMainPageControllerFactory class is a concrete class of MainPageController Factory class that has a responsibility
    of returning an object of TutorMainPageController without specifying its concrete classes.
    """

    def __init__(self):
        """
        Empty Constructor
        """
        pass

    def createMainPageController(self, type, username):
        """
        createMainPageController is a class that returns an object of TutorMainPageController.
        :param type: type of a user whether a user is student or tutor
        :param username: user's username
        :output: the concrete tutor main page
        """

        return TutorMainPageController(type, username)


class StudentMainPageController(MainPageControllerAbstract):
    """
    StudentMainPageController class implements the abstract methods of MainPageControllerInterface. This mainly has a
    responsibility of redirecting and view a new specific page.
    """

    def __init__(self, type, username):
        """
        A constructor that intializes type and username.
        :param type: type of a user whether a user is student or tutor
        :param username: user's username
        """
        super().__init__(username)  # initialize the parent class

        self.type = type
        # self.user = username
        self.view = MainPageFactory(self).createMainPage(type, username)

    def goToCreateBid(self, view):
        """
        It has a functionality of destroying the previous window and invoke CreateBidController and redirect user to create bids page.
        :param view: view that the user is currently on.
        """
        view.root.destroy()
        controller = CreateBidController(self.type, self.user)

    def viewBids(self, view):
        """
        It has a functionality of destroying the previous window and invoke StudentViewBidsController to redirect to view bids page.
        :param view: view that the user is currently on.
        """
        view.root.destroy()
        controller = StudentViewBidsController(self.user)

    def viewContracts(self, view):
        view.root.destroy()
        controller = ViewContractsController(self.user)


class TutorMainPageController(MainPageControllerAbstract):
    """
    TutorMainPageController class implements the abstract methods of MainPageControllerInterface. This mainly has a
    responsibility of redirecting and view a new specific page.
    """

    def __init__(self, type, username):
        """
        A constructor that intializes type and username.
        :param type: type of a user whether a user is student or tutor
        :param username: user's username
        """
        super().__init__(username)  # initialize the parent class

        self.type = type
        # self.user = username
        self.view = MainPageFactory(self).createMainPage(type, username)
        # display notifications

    def viewBids(self, view):
        """
        It has a functionality of destroying the previous window and invoke TutorViewBidsController to redirect to view bids page.
        :param view: view that the user is currently on.
        """
        view.root.destroy()
        controller = TutorViewBidsController(self.user)

    def viewContracts(self, view):
        view.root.destroy()
        controller = ViewContractsController(self.user)

    def viewMonitor(self, view):
        view.root.destroy()
        controller = ViewMonitorController(self.user, timer=15000)  # time in milliseconds
