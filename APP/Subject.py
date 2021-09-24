

class Subject:
    """
    Subject class that represents subject object
    """

    def __init__(self, id, name, description):
        """
        constructor of subject class
        :param id: id of the subject
        :param name: name of the subject
        :param description: description of the subject
        """
        self.id = id
        self.name = name
        self.description = description


    def getId(self):
        """
        getter of the subject's id
        """
        return self.id

    def getName(self):
        """
        getter of the subject's name
        """
        return self.name

    def getDescription(self):
        """
        getter of the subject's description
        """
        return self.description

