
from API.JSONAdapter import JSONAdapter
from API.Key import APIKey
from GUI.Application import LoginPage
from LOGIC.MainPageControllerFactory import MainPageControllerFactory
from LOGIC.Mediator import CollectionMediator


class LoginVerification:
    """
    This is a controller for login verification. It determines a validity of API key and credentials upon user login.
    Once it successfully validates a user it produces all the Model Collections, using the input API key. Then, it
    determines a specific model collection based on user id and retrieve them along with the user information.
    """

    def __init__(self):
        """
        Initialize LoginPage View and user that initially holds None.
        """

        self.view = LoginPage(self)  # view
        self.user = None

    def showInvalidApiKey(self, view):
        """
        This is to show an error message if the input api key is invalid.
        :param view: view is a page that the error is supposed to be shown on.
        """
        view.login_error_input.config(text="Invalid API key")

    def showInvalidCred(self, view):
        """
        This is to show an error message if the input credential is invalid.
        :params view: view is a page that the error is supposed to be displayed on.
        """
        view.login_error_input.config(text="Invalid Credentials")

    def validateLogin(self, password, username, view):
        """
        This validates if the user is a valid user upon login authentication. It produces relevant model collections based on
        a user information.

        :param password: password is a password of the user.
        :param username: username is a username of the user
        :param api_key: api_key is a user's api key.
        :param view: view is a view page to display all the relevant messages.
        """

        self.user = username

        keyInstance = APIKey.getInstance("NkNkp86CpdQbpKMRcbw7dtzrMPpTrK")  # create key instance

        # initialize the adaptors
        adapter = JSONAdapter.getInstance()
        # try: #todo uncomment try and except when done
        user_list = adapter.getAllUsers()  # initializes the userCollection
        subject_list = adapter.getAllSubjects()
        competency_list = adapter.getAllCompetency()
        bid_list = adapter.getAllBids()
        contract_list = adapter.getAllContracts()
        qualification_list = adapter.getAllQualification()
        message_list = adapter.getAllMessage()

        # except Exception:
        #     view.error1_input.config(text="Invalid API key\n Restart the app and try again")

        # initialize the users
        for user in user_list:  # make a list of users

            list = []
            for mes in message_list:
                if mes.getPosterId() == user.getId():  # if user is the poster
                    list.append(mes)
            user.setMessages(list)
            # set competency
            list = []
            for comp in competency_list:
                if comp.getOwnerId() == user.getId():  # bid belongs to the user
                    list.append(comp)
            user.setCompetency(list)

            # set qualifications
            list = []
            for qual in qualification_list:
                if qual.getOwnerId() == user.getId():  # bid belongs to the user
                    list.append(qual)
            user.setQualifications(list)

            # set bids
            list = []
            for bid in bid_list:

                if bid.getOwnerId() == user.getId():  # add bid to the user
                    list.append(bid)
            user.setBids(list)


            # set contracts
            list = []
            for con in contract_list:
                if con.getOwnerId() == user.getId() or con.getSecondPartyId() == user.getId():  # contract belongs to the user
                    list.append(con)
            user.setContracts(list)

        # initialize user collection class and subject collection class
        col_mediator = CollectionMediator(user_list,subject_list)


        adapter.observer.subscribe(col_mediator.userCollection)

        print(adapter.observer.subscribers)

        #  fill every users competency, qualifications and bids
        current_user = col_mediator.getUserByUserName(username)

        # verify current user with jwt
        verified = adapter.verifyUser(username, password)
        if current_user == None or current_user.getUserName() != password or not verified:
            self.showInvalidCred(view)  # user is not found
        else:

            # user is verified. Log in
            view.root.destroy()
            mainPageCon = MainPageControllerFactory().createMainPageController(
                col_mediator.getUserByUserName(username).getType(), username)


