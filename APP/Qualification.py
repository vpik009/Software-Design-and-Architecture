class Qualification:
    """
    Class that represents Qualification object and its relevant fields.
    """

    def __init__(self, id, ownerId, title, description, verified=None):
        """
        Constructor of the qualification class.
        :param id: id represents qualification id
        :param ownerId: owner id represents the user id of the qualification holder.
        :param title: title represents a title of a qualification
        :param description: description represents a description of a qualification.
        :param verified: verified is whether the qualification is verified or not.
        """
        self.id = id
        self.title = title
        self.description = description
        self.verified = verified
        self.ownerId = ownerId

    def getId(self, id):
        """
        getter of the id
        :param id: id of a qualification.
        """
        return self.id

    def getTitle(self):
        """
        getter of the id
        :param id: id of a qualification.
        """
        return self.title

    def getDescription(self):
        """
        getter of a description of a qualification
        """
        return self.description

    def getVerified(self):
        """
        getter of the verified attribute
        """
        return self.verified

    def getOwnerId(self):
        """
        getter of the owner id of a qualification
        """
        return self.ownerId
