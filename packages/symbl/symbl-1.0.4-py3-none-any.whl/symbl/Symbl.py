from symbl_rest import AuthenticationApi, ConversationsApi, JobsApi, ApiClient, Configuration

from symbl.AsyncApi import AsyncApi


class Symbl():

    '''
        It will return an object of ApiClient with a prefilled token. 
    '''
    def __init__(self, app_id=None, app_secret=None, refresh_token=False):

        if app_id is None or len(app_id) == 0:
            raise ValueError('app_id is required')
        
        if app_secret is None or len(app_secret) == 0:
            raise ValueError('app_secret is required')

        configuration = Configuration()

        body={
            'type': 'application', 
            'appId': app_id, 
            'appSecret': app_secret
            }

        authenticationResponse = AuthenticationApi().generate_token(body)
        configuration.api_key['x-api-key'] = authenticationResponse.access_token

        self.api_client = ApiClient(configuration)
    

    def getAsyncApiClient(self):

        if self.api_client is None:
            raise ValueError('Please initialize sdk with correct app_id and app_secret.')
        
        return AsyncApi(self.api_client)

    def getConversationsApiClient(self):
        
        if self.api_client is None:
            raise ValueError('Please initialize sdk with correct app_id and app_secret.')
        
        return ConversationsApi(self.api_client)

    def getJobsApiClient(self):

        if self.api_client is None:
            raise 'Please initialize sdk with correct app_id and app_secret.'
        
        return JobsApi(self.api_client)