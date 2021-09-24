from abc import ABC, abstractmethod


class APIInterface(ABC):
    '''
    Interface holds all the common methods among all of the object types in the webservice
    All classes that extend controller need to implement the methods that it possesses
    '''


    @abstractmethod
    def getAll(self):
        '''
        method used to get all objects of the requested type
        '''
        pass

    @abstractmethod
    def get(self, id):
        '''
        method used to get a specific object
        '''
        pass

    @abstractmethod
    def post(self):
        '''
        method used to post an object
        '''
        pass

    @abstractmethod
    def patch(self):
        '''
        method used to update a specific object
        '''
        pass

    @abstractmethod
    def delete(self):
        '''
        method used to delete a specific object
        '''
        pass
