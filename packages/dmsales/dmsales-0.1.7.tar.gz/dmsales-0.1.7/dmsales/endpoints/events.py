import logging
import json
from typing import Optional

from dmsales.api_operations import APIOperations

logger = logging.getLogger(__name__)


class EventsEndpoints(APIOperations):

    def add_custom_event(self, project_id: str, type: str, custom: dict, base_key: str = None,
                         email: str = None, phone: str = None, public_identifier_li: str = None) -> Optional[str]:
        '''
        Adds custom event.
        One arg of (email, base_key, phone, public_identifier_li) is required.

        :param project_id: project id e.g. 123e4567-e89b-12d3-a456-426614174000
        :type project_id: str
        :param type: event type e.g. custom_type
        :type type: str
        :param custom: custom fields and values added to custom event
        :type custom: dict
        :param base_key: contact base key in project e.g. bazaMR_1234567890, defaults to None
        :type base_key: str, optional
        :param email: contact email in project, defaults to None
        :type email: str, optional
        :param phone: contact phone in project, defaults to None
        :type phone: str, optional
        :param public_identifier_li: contact public linkedin identifier in project e.g. imie-nazwisko-123456789, defaults to None
        :type public_identifier_li: str, optional
        :return: message response from endpoint (e.g. "ok" or "Project person not found")
        :rtype: Optional[str]
        '''
        endpoint = '/api/events/add-custom-event'

        data = {
            'project_uuid': project_id,
            'type': type,
            'base_key': base_key,
            'email': email,
            'phone': phone,
            'public_identifier_li': public_identifier_li,
            'custom': custom
        }

        data = {k: v for k, v in data.items() if v}  # exclude None args
        logger.debug('Calling add_custom_event method')
        return super().make_post_request(endpoint, json=data)
