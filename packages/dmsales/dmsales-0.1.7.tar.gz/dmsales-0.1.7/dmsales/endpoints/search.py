import logging
from typing import List, Dict

from dmsales.api_operations import APIOperations

logger = logging.getLogger(__name__)

class SearchEndpoints(APIOperations):

    def search_list(self, project_id: str) -> List[Dict[str, str]]:
        '''
        This call return profiles and segments from project

        :param project_id: ID from projects' list
        :type project_id: str
        :return: List of dicts with profiles and segments from project
        :rtype: List[Dict[str, str]]
        '''
        return super().make_get_request('/api/search/list', params={'project_id': project_id})
