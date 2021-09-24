
import requests
import json
from API.APIInterface import APIInterface

#Has to be created ones the user specifies his/her api key
class BidAPI(APIInterface):
    """
    A class to hold all the API endpoints for user objects
    """

    def __init__(self, key):
            self.api_key = key
            self.url = "https://fit3077.com/api/v2/bid"
            self.headers = {
                # 'Content-type': 'application/json',
                'Authorization': self.api_key
            }



    # API ENDPOINTS
    def getAll(self):
        '''
        Get all bids in the webservice
        '''
        response = requests.get(self.url, headers=self.headers)

        return response.json()


    def get(self, id):
        '''
        Get a specific bid using bidId
        id: the bid id of the bid that is to be accquired
        '''
        url = self.url +"/" +str(id)

        response = requests.get(url, headers=self.headers)

        return response.json()

    def post(self, data):
        '''
        Post a new bid into the webservice
        data: the data in json that represents the bid.
        '''

        response = requests.post(self.url, data = json.dumps(data), headers={"Authorization":self.api_key,  'Content-type': 'application/json'})
        return response.json()  # return the posted bid


    def post_closedown(self, id, data):
        url = self.url + "/" + str(id) + "/close-down"
        response = requests.post(url, data=data,headers={"Authorization": self.api_key,  'Content-type': 'application/json'})


    def patch(self ,id ,data):
        '''
        method used to update an object in the webservice with the data provided
        id: the bid id of the user that needs to be patched
        data: the relevant data in json that needs to be updated. Does not need to represent all of its json object fields, only the ones that need to be updated.
        '''
        url = self.url +"/" +str(id)
        data_json = json.dumps(data)
        response = requests.patch(url ,data=data_json, headers={"Authorization":self.api_key,  'Content-type': 'application/json'})
        print(response.status_code)
        return response.json()


    def delete(self ,id):
        '''
        method used to delete a specific bid from the webservice
        id: the bid id of the bid that needs to be deleted
        '''
        url = self.url +"/" +str(id)
        response = requests.delete(url ,headers=self.headers)
        return response.status_code #204 if successfully deleted

