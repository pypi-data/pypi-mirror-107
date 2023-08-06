import logging
from typing import Union, Dict, List, Optional
try:
    from typing import TypedDict
except ImportError:
    from typing_extensions import TypedDict

from dmsales.api_operations import APIOperations

logger = logging.getLogger(__name__)


class ProjectPerson(TypedDict):
    tags: List[str]
    type: str
    address: Dict[str, str]
    postal_code: str
    street: str
    street_number: str
    local_number: str
    voivodeship: str
    personal_data: Dict[str, str]
    email: Dict[str, str]
    phone: Dict[str, str]
    '''
    Example Dict:
    {
        "id": "bazaMR_0000000000",
        "project_id": "b5faf3c9-2672-4cf0-b0aa-57ce8c2a8a21",
        "project_person": {
            "tags": [
            "tag1",
            "tag2"
            ],
            "type": "b2b",
            "address": {
            "city": "Katowice",
            "county": "Katowice",
            "postal_code": "40-101",
            "street": "Al. Piastów",
            "street_number": "10",
            "local_number": "35",
            "voivodeship": "śląskie"
            },
            "personal_data": {
            "name": "Nowy",
            "surname": "Lead",
            "company_name": "My Very First Company",
            "position": "CEO"
            },
            "email": {
            "raw": "exae-email@test.test"
            },
            "phone": {
            "raw": "+48 123 456 678"
            },
            "sex": "kobieta"
        }
    }
    '''


class PersonEndpoints(APIOperations):

    def add_person(self, id: Optional[str], project_id: str, person_dict: ProjectPerson) -> Optional[dict]:
        '''
        Adds person to project

        :param id: person id
        :type id: Optional[str, None]
        :param project_id: project id where person will be added
        :type project_id: str
        :param person_dict: person data
        :type person_dict: ProjectPerson
        '''
        endpoint = '/api/persons/upsert'
        data = {
            'id': id,
            'project_id': project_id,
            'project_person': person_dict
        }
        return super().make_post_request(endpoint=endpoint, json=data)

    def update_person(self, id: str, project_id: str, person_dict: ProjectPerson) -> Optional[dict]:
        '''
        Updates person in project

        :param id: person id
        :type id: str
        :param project_id: project id where person will be updated
        :type project_id: str
        :param person_dict: person_data
        :type person_dict: ProjectPerson
        '''
        endpoint = '/api/persons/upsert'
        data = {
            'id': id,
            'project_id': project_id,
            'project_person': person_dict
        }
        return super().make_put_request(endpoint=endpoint, json=data)

    def init_call(self, project_id: str, base_key: str) -> Optional[dict]:
        '''
        Initializes call to person from project

        :param project_id: project id
        :type project_id: str
        :param base_key: person's base key
        :type base_key: str
        '''
        params = {'project_id': project_id, 'base_key': base_key}
        return super().make_post_request(endpoint='/api/persons/init-call', params=params)

    def check_call(self, project_id: str, call_id: str) -> Optional[dict]:
        '''
        Checks call status

        :param project_id: project id
        :type project_id: str
        :param call_id: call id which status you want to check
        :type call_id: str
        '''
        params = {'project_id': project_id, 'call_id': call_id}
        return super().make_get_request(endpoint='/api/persons/check-call', params=params)