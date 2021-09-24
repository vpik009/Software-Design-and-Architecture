
class Message:
    '''
    Class that represents the message object and holds its relevant fields
    '''

    def __init__(self, id, bidId, poster_id, datePosted, content, initiator, additional,dateLastEdited=None):
        '''
        Contructor to instantiate message instances
        :param id: the id of the message
        :param bidId: the id of the bid the message is for
        :param poster_id: the id of the user who posted the message
        :param datePosted: the date the message was posted
        :param content: message content
        :param initiator: the id of the bid initiator of the bid the message is for
        :param additional: additional data of the message
        :param dateLastEdited: the last date the message was edited. Optional

        '''
        self.id = id
        self.bidId = bidId
        self.poster_id = poster_id
        self.datePosted = datePosted
        self.dateLastEdited = dateLastEdited
        self.content = content
        self.initiator = initiator
        self.additional = additional  # json object of bid information

    def getId(self):
        '''
        getter for the message id
        :output: the id of the message as a string
        '''
        return self.id

    def getBidId(self):
        '''
        getter for the id of the bid the message is for
        :output: the id of the bid the message is for as a string
        '''
        return self.bidId

    def getPosterId(self):
        '''
        getter for the id of the user that posted the message
        :output: the id of the user who posted the message as a string
        '''
        return self.poster_id

    def getDatePosted(self):
        '''
        getter for the date on which the message was posted
        :output: the date on which the message was posted as a string
        '''
        return self.datePosted

    def getDateLastEdited(self):
        '''
        getter for the date the message was last edited
        :output: the date on which the message was last edited as a string
        '''
        return self.dateLastEdited

    def getContent(self):
        '''
        getter for the content of the message
        :output: the message's content as a string
        '''
        return self.content

    def getAdditional(self):
        '''
        getter for the message's additional information
        :output: the additional information of the message as a JSON
        '''
        return self.additional

    def stringifyContent(self):
        '''
        converts the content JSON object into a readable string
        :output: a single string that is easily readable and printable on UI
        '''
        # content is a json object
        ret = "Sessions per week: "+ self.additional['sessionsPerWeek']
        ret += "\nhours per lesson:"+self.additional['hoursPerLesson']
        ret += "\nfree lesson:"+self.additional['freeLesson']
        ret += "\nrate:"+self.additional['rate']
        ret += "\nrate type:"+self.additional['rateType']
        ret += "\nextra:"+self.content
        return ret


    def getInitiator(self):
        '''
        getter for the initiator id
        :output: the id of the bid initiator as a string
        '''
        return self.initiator
