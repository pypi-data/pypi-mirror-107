import requests
import logging

from .endpoints import contacts, project, segment, events, search, person, user, techscopeapi

logger = logging.getLogger(__name__)

class DMSalesAPI(
    project.ProjectEndpoints,
    contacts.ContactsEndpoints,
    segment.SegmentEndpoints,
    events.EventsEndpoints,
    search.SearchEndpoints,
    person.PersonEndpoints,
    user.UserEndpoints,
    techscopeapi.TechScopeApiEndpoints
):
    
    api_host = 'https://app.dmsales.com'

    def __init__(self, api_key: str, test: bool=False):
        '''
        Main class to manipulate DMSales API with all implemented methods

        :param api_key: dmsales api key https://app.dmsales.com/pl/panel/settings-account?settings=api-configuration
        :type api_key: str
        :param test: dmsales api test environment, defaults to False
        :type test: bool, optional
        '''
        self.api_key = api_key

        if test is True:
            self.api_host = 'http://dmsales.test.dmsales.com:8081'

        self.session = requests.Session()
        self.session.headers = {'Authorization': f'Bearer {api_key}'}
