import logging
from typing import Optional

from dmsales.api_operations import APIOperations

logger = logging.getLogger(__name__)


class ContactsEndpoints(APIOperations):

    def persons_list(self, page: int, limit: int, segment_id: str = None,
                     project_id: str = None, sort: str = None, export_date_from: str = None,
                     export_date_to: str = None, paid_leads='true') -> Optional[dict]:
        '''
        This endpoint returns your project's contacts. You can filter by project or profile. 
        Additionaly, you can provide export dates to filter contacts from given period.

        :param page: Page number
        :type page: int
        :param limit: Amount of contacts per page
        :type limit: int
        :param segment_id: Segment ID - returns only contacts matching given profile. One of segment_id or project_id is required.
        :type segment_id: str
        :param project_id: Returns all contacts from given project. One of segment_id or project_id is required.
        :type project_id: str
        :param sort: Define list sorting.
        :type sort: str
        :param export_date_from: Filter contacts by export date (exported after given date).
        :type export_date_from: str
        :param export_date_to: Filter contacts by export date (exported before given date).
        :type export_date_to: str
        :param paid_leads: Display paid leads. (Available values : 'true', 'false', 'all'), defaults to 'true'
        :type paid_leads: str
        '''
        endpoint = '/api/persons/list'
        args_dict = {
            'page': page,
            'limit': limit,
            'segment_id': segment_id,
            'project_id': project_id,
            'sort': sort,
            'export_date_from': export_date_from,
            'export_date_to': export_date_to,
            'paid_leads': paid_leads
        }

        # exclude None args
        args_dict = {k: v for k, v in args_dict.items() if v}
        logger.debug('Calling persons_list method')
        return super().make_get_request(endpoint, params=args_dict)
