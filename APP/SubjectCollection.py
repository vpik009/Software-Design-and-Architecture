
class SubjectCollection:
    """
    SubjectCollection that represents the collection of subject objects
    """

    _instance = None

    def __init__(self, subject):
        """
        :subject: A list of subject objects
        """
        self.subject = subject

    @classmethod
    def getInstance(cls, subject=[]):
        """
        Singleton of subject collection that keeps the cache
        :subject: A list of subjects to initialize the Collection with if instance class variable is None
        """
        if not cls._instance:
            cls._instance = SubjectCollection(subject)
        return cls._instance


    def getSubjects(self):
        """
        getter of subjects
        """
        return self.subject

    def getSubjectByName(self,name):
        '''
        gets the subject by name
        if not found, return None
        :param name: name of the subject
        '''
        for subject in self.subject:
            if subject.getName() == name:
                return subject
        return None

    def addSubject(self,subject):
        """
        appends the list of existing subject with the parameter 'subject'
        :param subject: the subject instance that is to be appended into the subject collection
        """
        self.subject.append(subject)

    def getSubjectById(self,id):
        """
        Can search a subject by Id
        If not found, return None
        :param id: id of the subject
        """
        for subject in self.subject:
            if subject.getId() == id:
                return subject
        return None