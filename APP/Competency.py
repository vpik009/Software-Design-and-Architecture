class Competency:
    '''
    Class used to hold the data relevant to the user's competency
    '''

    def __init__(self, id, subject_id, ownerId, level):
        '''
        constructors to instantiate the competency class
        :param id: the id of the competency that is being created
        :param subject_id: the subject id of the subject the competency is for
        :param ownerId: the owner id of the user the competency belongs to
        :param level: the level of the users proficiency in the subject
        '''
        self.id = id
        self.subject_id = subject_id
        self.level = level
        self.ownerId = ownerId

    def getId(self):
        '''
        A getter to get the id of the competency object
        :output: the id of the competency in the form of a string
        '''
        return self.id

    def getLevel(self):
        '''
        A getter to get the level of the competency's owner in the given subject
        :output: the level of the competency's owner in the given subject as an integer
        '''
        return self.level

    def getSubjectId(self):
        '''
        A getter to get the subject id of the subject the competency is for
        :output: the subject id of the subject the competency is for as a string
        '''
        return self.subject_id

    def getOwnerId(self):
        '''
        A getter to get the id of the owner of the competency
        :output: the id of the owner of the competency as a string
        '''
        return self.ownerId



