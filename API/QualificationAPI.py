import requests
import json
from API.APIInterface import APIInterface


class QualificationAPI(APIInterface, object):
    """
    A class to hold all the API endpoints for qualification objects
    """

    _instance = None

    def __init__(self, key):
        self.api_key = key
        self.url = "Server is no longer available"
        self.headers = {
            "Authorization": self.api_key
        }


    def getAll(self):
        '''
        Get all qualification in the webservice
        '''
        response = requests.get(self.url, headers=self.headers)
        return response.json()

    def get(self, id):
        '''
        Get a specific qualification using qualificationId
        id: the qualification id of the qualification that is to be accquired
        '''
        url = self.url + "/" + str(id)
        response = requests.get(url, headers=self.headers)

        return response.json()

    def post(self, data):
        '''
        Post a new qualification into the webservice
        data: the data in json that represents the qualification.
        '''
        response = requests.post(self.url, data=json.dumps(data),
                                 headers={"Authorization": self.api_key, 'Content-type': 'application/json'})
        return response.status_code

    def patch(self, id, data):
        '''
        method used to update an object in the webservice with the data provided
        id: the qualification id of the user that needs to be patched
        data: the relevant data in json that needs to be updated. Does not need to represent all of its json object fields, only the ones that need to be updated.
        '''
        url = self.url + "/" + str(id)
        data_json = json.dumps(data)
        response = requests.patch(url, data=data_json,
                                  headers={"Authorization": self.api_key,
                                           'Content-type': 'application/json'})
        return response.status_code

    def delete(self, id):
        '''
        method used to delete a specific qualification from the webservice
        id: the qualification id of the qualification that needs to be deleted
        '''
        url = self.url + "/" + str(id)
        response = requests.delete(url, headers=self.headers)
        return response.status_code

    def put(self, id, data):
        '''
        method used to update an object in the webservice with the data provided
        id: the qualification id of the user that needs to be patched
        data: the relevant data in json that needs to be updated. Does not need to represent all of its json object fields, only the ones that need to be updated.
        '''
        url = self.url + "/" + str(id)
        data_json = json.dumps(data)
        response = requests.put(url, data=data_json,
                                headers={"Authorization": self.api_key, 'Content-type': 'application/json'})
        return response.status_code



