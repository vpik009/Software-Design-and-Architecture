
class APIKey(object):
    '''
    This class stores the user's API key to be accessed from across the application
    Uses singleton
    '''

    _instance = None

    def __init__(self, newKey):
        """
        Constructor of the APIkey class
        :newKey: new API key
        """
        self.key = newKey



    @classmethod
    def getInstance(cls, key=None):
        """
        Use of singleton to keep the API key
        :key: api key input in the login form
        """
        if not cls._instance:  # if no instance, create one
            cls._instance = APIKey(key)
        return cls._instance


    def getKey(self):
        """
        obtain APIKey
        """
        return self.key
