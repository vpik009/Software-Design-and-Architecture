from datetime import datetime, timedelta

from API.Observer import Observer

"""
datetime provides functionalities for manipulating dates and times into various formats
https://docs.python.org/3/library/datetime.html
"""
from API.BidAPI import BidAPI
from API.ContractAPI import ContractAPI
from API.Key import APIKey
from APP.Contract import Contract
import json

"""
json module is used to decode/encode JSON object and convert to object data, and vice versa.
https://docs.python.org/3/library/json.html 
"""
from API.UserAPI import UserAPI
from API.QualificationAPI import QualificationAPI
from API.MessageAPI import MessageAPI
from API.SubjectAPI import SubjectAPI
from API.CompetencyAPI import CompetencyAPI
from APP.BidFactory import BidFactory
from APP.Competency import Competency
from APP.Subject import Subject
from APP.Qualification import Qualification
from APP.Message import Message
from APP.UserFactory import UserFactory


class JSONAdapter:
    """
    This class is a JSONAdapter utility class in the API package. This is to ensure that this class is reused throughout
    the application.

    This utility class follows three major design principles, which are as follows;
    1. Singleton:  this is to hold the access point globally and ensure that the content is cached
    throughout. This is shown in line 62 - line 71 getInstance method.

    2. Observer Pattern: this is to establish a subscription mechanism between the JSONAdapter that behaves as a
    publisher and so it can subscribe some observers (shown in subscribe method from line 75 - 81) and notify them
    when some change happens at runtime. For instance, notifySubscriberUser method (line 105 - 111) is called when
    a user subscribes a bid and it notifies the UserCollection to perform addSubedBid method and updates a user's additional
    information according to the bid that is to be subscribed.

    3. Adapter Pattern: This design pattern is used to convert JSON data into objects and objects into JSON data. This
    is to ensure that the User class will not break the single responsibility class as User class would have to control
    the conversion of JSON data and object data otherwise. This is seen in the getAllUsers method (line135 - 156). It
    collects JSON data from the REST API call and convert it into User object through UserFactory.
    """
    _instance = None

    def __init__(self):
        """
        Constructor that initializes necessary information.
        """
        # self.subscribers = []  # initialize empty list to hold subscribers
        self.observer = Observer([])

        self.api_key = APIKey.getInstance().getKey()  # get user's api key

        self.bidController = BidAPI(self.api_key)
        self.contractController = ContractAPI(self.api_key)
        self.competencyController = CompetencyAPI(self.api_key)
        self.messageController = MessageAPI(self.api_key)
        self.qualificationController = QualificationAPI(self.api_key)
        self.subjectController = SubjectAPI(self.api_key)
        self.userController = UserAPI(self.api_key)

        self.url = "https://fit3077.com/api/v2/"
        self.headers = {
            'Authorization': self.api_key
        }

    @classmethod
    def getInstance(cls):
        """
        singleton is used to keep the instance of subscribers that will get notified and do some specific update action
        accordingly.
        """

        if not cls._instance:
            # doesnt exist
            cls._instance = JSONAdapter()  # create a new instance
        return cls._instance  # return the instance

    def getAllUsers(self):
        """
        To get all users from API endpoint object and add them to model collection.
        """
        url = self.url + "user"
        user_factory = UserFactory()
        response = self.userController.getAll()

        user_list = []
        # reformat into classes
        for user in response:
            if user['additionalInfo'] == {}:
                current_user = user_factory.createUser(user['isTutor'], user['id'], user['givenName'],
                                                       user['familyName'],
                                                       user['userName'], [], [], [], [], [], [])
            else:
                current_user = user_factory.createUser(user['isTutor'], user['id'], user['givenName'],
                                                       user['familyName'],
                                                       user['userName'], [], [], [], [], [],
                                                       user['additionalInfo']['subscribedBids'])

            user_list.append(current_user)

        return user_list

    def getAllSubjects(self):
        """
        To get all users from API endpoint object and add them to model collection.
        """

        response = self.subjectController.getAll()
        subject_list = []
        for subject in response:
            subject = Subject(subject['id'], subject['name'], subject['description'])
            subject_list.append(subject)
        return subject_list

    def postSubject(self, name, description):
        """
        To post a subject to API endpoint and add it to subject collection as well.
        :name: Name of the subject
        :description: description of the subject
        """

        subject = {
            'name': name,
            'description': description
        }

        response = self.subjectController.post(subject)
        # response is the json of the subject
        sub = Subject(response['id'], response['name'], response['description'])
        return sub  # returned the added subject as a class

    def getAllCompetency(self):
        """
        To get all competency from API endpoint object and add them to model collection.
        """

        response = self.competencyController.getAll()
        competency_list = []
        for competency in response:
            competency = Competency(competency['id'], competency['subject']['id'], competency['owner']['id'],
                                    competency['level'])
            competency_list.append(competency)

        return competency_list

    def getAllBids(self):
        """
        To get all bids from API endpoint object and add them to model collection.
        """

        url = self.url + "bid"
        response = self.bidController.getAll()
        bid_factory = BidFactory()
        bid_list = []
        for bid in response:
            # id, subId, dateCreated, dateClosedDown, messages = None
            current_bid = bid_factory.createBid(bid['type'], bid['id'], bid['subject']['id'], bid['initiator']['id'],
                                                bid['dateCreated'], bid['dateClosedDown'], bid['additionalInfo'])
            bid_list.append(current_bid)

        return bid_list

    def postBid(self, type, initiatorId, dateCreated, subjectId, additionalInfo):
        """
        To post a bid to API endpoint and add it to bid factory and add it to a bid collection depending on the bid type as well.
        :type: type of bid
        :initiatorId: id of an initiator of the bid
        :dateCreated: date creation of the bid
        :subjectId: subject id related to the bid
        :additionalInfo: additional information to be added for the bid
        """
        bid = {
            "type": type,
            "initiatorId": initiatorId,
            "dateCreated": dateCreated,
            "subjectId": subjectId,
            "additionalInfo": additionalInfo
        }

        response = self.bidController.post(bid)
        # response is the json of the subject
        bid_factory = BidFactory()
        bid = bid_factory.createBid(response['type'], response['id'], response['subject']['id'],
                                    response['initiator']['id'],
                                    response['dateCreated'], response['dateClosedDown'], response['additionalInfo'])

        self.observer.notifySubscriberBids(initiatorId, bid)  # update the collection

        return bid  # returned the added subject as a class

    def closeBid(self, id):
        """
        This method is used to notify and update the contracts in related collections
        when the bid is closed down
        :id: Id of the bid
        """

        data = {
            "dateClosedDown": datetime.now().__str__()
        }

        response = self.bidController.post_closedown(id, json.dumps(data))
        self.observer.notifySubscriberCloseBid(id)

    def patchOffer(self, bidId, tutorId, sesPerWeek, hoursPerSession, freeLesson, rate, payType, additional, add):
        '''
        Method used to patch the existing offer of a bid
        :bidId: The id of the bid that is to be patched
        :tutorId: The id of the tutor who made the offer
        :sesPerWeek: tutor's new input for sessions per week
        :hoursPerSession: tutor's new input for hours per session
        :freeLesson: tutor's new input for freeLesson indicating whether or not he offers a free lesson
        :rate: the rate the tutor is offering
        :payType: how the rate is to be interpreted (per session or per hour)
        :additional: any additional information the tutor wants to include in his offer.
        :add: the additional information of the bid for which the offer is to be patched
        '''

        data_append = {
            'tutorId': tutorId,
            'sessionsPerWeek': sesPerWeek,
            'hoursPerLesson': hoursPerSession,
            'freeLesson': freeLesson,
            'rate': rate,
            'rateType': payType,
            'additional': additional
        }

        # add it to the correct bid (at index)
        data = add
        offers = add['bids']

        # find the offer with the tutorId
        for i in range(len(offers)):
            if offers[i]['tutorId'] == tutorId:
                offers[i] = data_append
        add['bids'] = offers

        data['bids'] = add['bids']

        data = {
            'additionalInfo': data

        }

        response = self.bidController.patch(bidId, data)  # update model

        print(response, 'response')

        return response

    def createOffer(self, bidId, tutorId, sesPerWeek, hoursPerSession, freeLesson, rate, payType, additional, add):
        '''
        To create an offer when the bid is bought out.
        :bidId: the id of the bid the offer is for
        :sesPerWeek: The number of sessions per week the tutor prefers
        :hoursPerSession: hours per session the tutor desires
        :freeLesson: a yes or a no, depending on whether the tutor provides a free lesson
        :rate: the tutor's rate
        :payType: the type of pay, either per session or per hour
        :additional: any additional information the tutor wants to provide
        :add: the existing additional information from the original offer
        '''

        data_append = {
            'tutorId': tutorId,
            'sessionsPerWeek': sesPerWeek,
            'hoursPerLesson': hoursPerSession,
            'freeLesson': freeLesson,
            'rate': rate,
            'rateType': payType,
            'additional': additional
        }

        data = add
        try:  # if the bids has offers, then append the new offer
            offers = add['bids']
            offers.append(data_append)
            add['bids'] = offers



        except Exception:  # if not then insert bids attribute at the json
            add['bids'] = [data_append]

        data['bids'] = add['bids']

        data = {
            'additionalInfo': data

        }

        response = self.bidController.patch(bidId, data)

        # update the collection
        bid_factory = BidFactory()
        bid = bid_factory.createBid(response['type'], response['id'], response['subject']['id'],
                                    response['initiator']['id'],
                                    response['dateCreated'], response['dateClosedDown'], response['additionalInfo'])

        self.observer.notifySubscriberBids(bid.getOwnerId(), bid, True)  # update the bid holder's information
        return response

    def postMessage(self, bidId, poster_id, ses_per_week, hours_ses, free_les, rate_inp, pay_type, additional,
                    initiatorId):
        '''
        To post a message to API endpoint and add it to bid factory and add it to a message model, using observer pattern.
        :bidId: the id of the bid the message is for
        :ses_per_week: The number of sessions per week to be negotiated
        :hours_ses: hours per session to be negotiated
        :free_les: a yes or a no, depending on whether the tutor provides a free lesson
        :rate_inp: the tutor's rate
        :pay_type: the type of pay, either per session or per hour
        :additional: any additional information to be negotiated
        :initiatorId: id of the initiator
        '''

        content = {
            "sessionsPerWeek": ses_per_week,
            "hoursPerLesson": hours_ses,
            "freeLesson": free_les,
            "rate": rate_inp,
            "rateType": pay_type,
        }

        data = {
            "bidId": bidId,
            "posterId": poster_id,
            "datePosted": datetime.now().__str__(),
            "content": additional,
            "additionalInfo": {
                "initiator": initiatorId,
                "content": content
            }
        }

        response = self.messageController.post(json.dumps(data))
        msg = Message(response['id'], response['bidId'], response['poster']['id'], response['datePosted'],
                      response['content'], response['additionalInfo']['initiator'],
                      response['additionalInfo']['content'])

        self.observer.notifySubscriberMessages(poster_id, msg)  # update collection

        return msg  # returns the created message

    # type, id, subId, ownerId, dateCreated, dateClosedDown, additionalInfo ,messages = None
    def getAllContracts(self):
        """
        To get all contracts from API endpoint object and add them to model collection.
        """

        url = self.url + "bid"
        response = self.contractController.getAll()

        bid_factory = BidFactory()
        contract_list = []
        for contract in response:
            # id, subid, sParty, dCreated, dSigned, eDate
            current_contract = Contract(contract['id'], contract['firstParty']['id'], contract['subject']['id'],
                                        contract['secondParty']['id'], contract['dateCreated'], contract['dateSigned'],
                                        contract['expiryDate'], contract['paymentInfo'], contract['lessonInfo'],
                                        contract['additionalInfo'])
            contract_list.append(current_contract)

        return contract_list

    def signContract(self, con_id, sign_date):
        '''
        Method used to sign a contract
        :con_id: the id of the contract that is to be signed
        :sign_date: the date the contract is signed
        '''

        sign_date = sign_date.__str__()
        date = {
            "dateSigned": sign_date
        }

        self.contractController.post_sign(con_id, date)

        response = self.contractController.get(con_id)  # get the signed contract
        contract = Contract(response['id'], response['firstParty']['id'], response['subject']['id'],
                            response['secondParty']['id'], response['dateCreated'], response['dateSigned'],
                            response['expiryDate'], response['paymentInfo'], response['lessonInfo'],
                            response['additionalInfo'])
        self.observer.notifySubscriberContracts(response['firstParty']['id'], contract, response['secondParty']['id'],
                                       patch=True)

    def postContract(self, studentId, tutorId, subId, acceptedOffer, tutComp, tutQual, dComp,
                     expiryMonths=6):
        '''
        To post a message to API endpoint and add it to bid factory and add it to a message model, using observer pattern.
        :studentId: id of the student
        :tutorId: id of the tutor
        :subId: subject id related to the successful bid
        :acceptedOffer: an offer that is accepted
        :tutComp: the tutor's competency
        :tutQual: tutor's qualification
        :expiryMonths: The duration in months for how long the contract should last. Defaults to 6
        '''

        additional = None
        try:
            additional = acceptedOffer.getContent()  # if its a message get the content
            acceptedOffer = acceptedOffer.getAdditional()  # set local var to param
        except Exception:
            additional = acceptedOffer['additional']  # if open offer get its additional information

        tut_comp = []
        tut_qual = []
        # adapt the competencies for api by converting to json
        for comp in tutComp:
            data = {
                "ownerId": comp.getOwnerId(),
                "subjectId": comp.getSubjectId(),
                "level": comp.getLevel()
            }
            tut_comp.append(data)

        # adapt the competencies for api by converting to json
        for qual in tutQual:
            data = {
                "title": qual.getTitle(),
                "description": qual.getDescription(),
                "verified": qual.getVerified(),
                "ownerId": qual.getOwnerId()
            }

            tut_qual.append(data)

        data = {
            "firstPartyId": studentId,
            "secondPartyId": tutorId,
            "subjectId": subId,
            "dateCreated": datetime.now().__str__(),
            "expiryDate": (datetime.now() + timedelta(days=(30 * expiryMonths))).__str__(),
            # (datetime.now() + timedelta(minutes=1)).__str__(),#
            # expires 30 days after creation
            "paymentInfo": {},
            "lessonInfo": {},
            "additionalInfo": {
                "tutorCompetency": tut_comp,
                "tutorQualification": tut_qual,
                "sessionsPerWeek": acceptedOffer['sessionsPerWeek'],
                "hoursPerLesson": acceptedOffer['hoursPerLesson'],
                "freeLesson": acceptedOffer['freeLesson'],
                "rate": acceptedOffer['rate'],
                "rateType": acceptedOffer['rateType'],
                "desiredCompetency": dComp,  # added
                "additional": additional
            }
        }

        response = self.contractController.post(json.dumps(data))
        contract = Contract(response['id'], response['firstParty']['id'], response['subject']['id'],
                            response['secondParty']['id'], response['dateCreated'], response['dateSigned'],
                            response['expiryDate'], response['paymentInfo'], response['lessonInfo'],
                            response['additionalInfo'])

        self.observer.notifySubscriberContracts(studentId, contract, tutorId)  # update both party members

        return contract  # returns the created message

    def getAllQualification(self):
        """
        To get all qualification from API endpoint object and add them to model collection.
        """

        response = self.qualificationController.getAll()
        qualification_list = []
        for qualification in response:
            qualification = Qualification(qualification['id'], qualification["owner"]["id"], qualification['title'],
                                          qualification["description"], qualification["verified"])
            qualification_list.append(qualification)
        return qualification_list

    def getAllMessage(self):
        """
        To get all messages from API endpoint object and add them to model collection.
        """

        response = self.messageController.getAll()
        message_list = []
        for message in response:
            message = Message(message['id'], message['bidId'], message['poster']['id'], message['datePosted'],
                              message['content'], message['additionalInfo']['initiator'],
                              message['additionalInfo']['content'], message['dateLastEdited'])

            message_list.append(message)
        return message_list

    def verifyUser(self, username, password):
        """
        To verify a user in the login by checking with the API endpoint.
        :username: name of the user
        :password: password of a user
        """

        data = {
            'userName': username,
            'password': password
        }
        response_login = self.userController.login(data)

        if not response_login:
            return False  # incorrect login

        verified = self.userController.verifyToken(response_login)

        return verified

    def updateUserSubscribedBids(self, user_id, bid_id):
        """
        This is to update a user's subscribed bids by adding a bid_id inside the additional information of the user.
        And call the REST Api patch for the user to partially update the user's information. Then, it will notify the
        user collection to update the model according to the update of the subscribed bid information.
        :user_id: id of the user
        :bid_id: id of a bid to be subscribed
        """

        user = self.userController.get(user_id)
        # bid_data = self.bidController.get(bid_id)

        try:
            user['additionalInfo']['subscribedBids'].append(bid_id)

            data = {
                "additionalInfo": {
                    "subscribedBids": user['additionalInfo']['subscribedBids']
                }
            }
        except KeyError:

            subscribed_bid_list = list()
            # bid_data = self.bidController.get(bid_id)
            subscribed_bid_list.append(bid_id)
            data = {
                "additionalInfo": {
                    "subscribedBids": subscribed_bid_list
                }
            }

        response = self.userController.patch(user_id, data)

        # need to update the model using observer
        self.observer.notifySubscriberUser(user_id, bid_id)

        return response
