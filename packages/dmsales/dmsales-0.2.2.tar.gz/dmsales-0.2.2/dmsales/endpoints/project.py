import logging
from typing import Optional, List

from dmsales.api_operations import APIOperations

logger = logging.getLogger(__name__)

class ProjectEndpoints(APIOperations):
    
    def project_list(self) -> Optional[List[dict]]:
        '''
        This call returns user's all projects.

        :return: list of project dictionaries
        :rtype: Optional[List[dict]]
        '''
        endpoint = '/api/project/list'
        logger.debug('Calling project_list method')
        return super().make_get_request(endpoint)