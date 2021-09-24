
import requests
import json
from API.APIInterface import APIInterface

#Has to be created ones the user specifies his/her api key
class UserAPI(APIInterface):
    """
    A class to hold all the API endpoints for user objects
    """

    def __init__(self, key):
            self.api_key = key
            self.url = "https://fit3077.com/api/v2/user"
            self.headers = {
                # 'Content-type': 'application/json',
                'Authorization': self.api_key
            }



    # API ENDPOINTS
    def getAll(self):
        '''
        Get all users in the webservice
        '''
        response = requests.get(self.url, headers=self.headers)

        return response.json()


    def get(self, id):
        '''
        Get a specific user using userId
        id: the user id of the user that is to be accquired
        '''
        url = self.url +"/" +str(id)

        response = requests.get(url, headers=self.headers)

        return response.json()

    def post(self, data):
        '''
        Post a new user into the webservice
        data: the data in json that represents the user. 
            requires all user fields:   givenName, familyName, userName, password, isStudent, isTutor. isStudent and isTutor dont have to be included: defaulted to false
        '''

        response = requests.post(self.url, data = json.dumps(data), headers={"Authorization":self.api_key,  'Content-type': 'application/json'})
        return response.status_code #201 if user successfully created, 409 if username is in use

    def patch(self ,id ,data):
        '''
        method used to update an object in the webservice with the data provided
        id: the user id of the user that needs to be patched
        data: the relevant data in json that needs to be updated. Does not need to represent all of its json object fields, only the ones that need to be updated.
        '''
        url = self.url +"/" +str(id)
        data_json = json.dumps(data)
        response = requests.patch(url ,data=data_json, headers={"Authorization":self.api_key,  'Content-type': 'application/json'})
        return response.json() #200 if successfully updated


    def delete(self ,id):
        '''
        method used to delete a specific user from the webservice
        id: the user id of the user that needs to be deleted
        '''
        url = self.url +"/" +str(id)
        response = requests.delete(url ,headers=self.headers)
        return response.status_code #204 if successfully deleted

    def put(self, id, data):
        '''
        method used to put data into an already existing user object. PUT should only be used if you're replacing a resource in its entirety. Otherwise use Patch
        id: the user id of the user
        data: the relevant data in json that needs to be put into the user with the specifies id
            Requiress user fiels: givenName, familyName, isStudent, isTutor
        '''
        url = self.url +"/" +str(id)
        data_json = json.dumps(data)
        response = requests.put(url ,data=data_json ,headers = {"Authorization":self.api_key,  'Content-type': 'application/json'})
        return response.status_code #200 if successful

    def login(self, data):
        '''
        Verifies the user' credentials
        https://stackoverflow.com/questions/39257168/how-to-fix-response-400-while-make-a-post-in-python
        data: json formatted username and password of the user to be verified
        jwt: optional parameter.
        '''
        url = self.url + "/login"
        response = requests.post(url ,data=data ,headers=self.headers)


        response = requests.post(
                url=url,
                headers=self.headers,
                params={ 'jwt': 'true' }, # Return a JWT so we can use it in Part 5 later.
                data=data
            )

    
        if response.status_code != 200:
            return None #no jwt returned

        return response.json()['jwt'] #return the jwt token

    def verifyToken(self, jwt):
        '''
        Verify the token
        Takes the jwt output directly from the login return
        :return: 200 if jwt is valid
        '''

        url = self.url + "/verify-token"

        response = requests.post(
                url=url,
                headers=self.headers,
                data={
                    'jwt':jwt
                    }

            )


        if response.status_code == 200:
            return True  #return true if valid jwt token
        else:
            return False


