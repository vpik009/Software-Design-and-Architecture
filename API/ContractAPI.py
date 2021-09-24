import requests
import json
from API.APIInterface import APIInterface


# Has to be created ones the user specifies his/her api key
class ContractAPI(APIInterface):
    """
    A class to hold all the API endpoints for contract objects
    """


    def __init__(self, key):
        self.api_key = key
        self.url = "https://fit3077.com/api/v2/contract"
        self.headers = {
            # 'Content-type': 'application/json',
            'Authorization': self.api_key
        }



    # API ENDPOINTS
    def getAll(self):
        '''
        Get all contract in the webservice
        '''
        response = requests.get(self.url, headers=self.headers)

        return response.json()

    def get(self, id):
        '''
        Get a specific contract using contractId
        id: the contract id of the contract that is to be accquired
        '''
        url = self.url + "/" + str(id)

        response = requests.get(url, headers=self.headers)

        return response.json()

    def post(self, data):
        '''
        Post a new contract into the webservice
        data: the data in json that represents the contract.
        '''
        response = requests.post(self.url, data=data,
                                 headers={"Authorization": self.api_key, 'Content-type': 'application/json'})
        return response.json()


    def post_sign(self, id, data):
        url = self.url + "/" + str(id) + "/sign"
        data_json = json.dumps(data)
        response = requests.post(url, data=data_json,
                                 headers={"Authorization": self.api_key, 'Content-type': 'application/json'})


    def patch(self, id, data):
        '''
        method used to update an object in the webservice with the data provided
        id: the contract id of the contract that needs to be patched
        data: the relevant data in json that needs to be updated. Does not need to represent all of its json object fields, only the ones that need to be updated.
        '''
        url = self.url + "/" + str(id)
        data_json = json.dumps(data)
        response = requests.patch(url, data=data_json,
                                  headers={"Authorization": self.api_key, 'Content-type': 'application/json'})
        return response.status_code  # 200 if successfully updated

    def delete(self, id):
        '''
        method used to delete a specific contract from the webservice
        id: the contract id of the contract that needs to be deleted
        '''
        url = self.url + "/" + str(id)
        response = requests.delete(url, headers=self.headers)
        return response.status_code  # 204 if successfully deleted



